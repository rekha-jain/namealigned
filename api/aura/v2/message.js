/**
 * POST /api/aura/v2/message
 * The Aura V2 chat endpoint. Server-Sent Events stream.
 *
 * Phase A: Gemini-only cascade, global daily quota gate, safety pre-filter,
 * Supabase-backed session + history persistence. No celestial, no symbol
 * retrieval, no memory yet, those plug in later through buildAuraPrompt.
 *
 * Request body (JSON):
 *   {
 *     conversationId?: string,
 *     message: string,
 *     profile?: { firstName?, birthNum? }
 *   }
 *
 * Headers:
 *   x-aura-anon: <signed anon token>   (optional; minted on first call)
 *
 * SSE events emitted:
 *   started   { conversationId, messageId, anonToken? }
 *   thinking  { stage }
 *   token     { text }
 *   done      { kind, model, latencyMs }
 *   error     { code, message }
 */

'use strict';

import { loadSession } from './_lib/session.js';
import { preFilterSafety } from './_lib/safety.js';
import { reserveQuota, AURA_RESTING_MESSAGE } from './_lib/quota.js';
import { buildAuraPrompt } from './_lib/prompt.js';
import { streamLLM } from './_lib/llmRouter.js';
import { retrieveSymbols, detectReadingMode } from './_lib/symbolic.js';
import { sanitizeChunk, finalize, isTimingQuestion } from './_lib/sanitize.js';
import { persistTurn } from './_lib/persistTurn.js';
import { startSSE, sendEvent, endSSE, sseSingleReply } from './_lib/sse.js';
import { insertInto } from './_lib/supabaseAdmin.js';

/**
 * Cheap regex-based register classifier. No Gemini call.
 * Returns 'casual' | 'practical' | 'reflective'.
 *
 *   casual:     greetings, thanks, very short social messages
 *   practical:  everyday logic, decisions, weather, advice, recommendations
 *   reflective: life direction, identity, love, career, purpose, symbolic, timing
 */
function classifyRegister(message) {
  const m = String(message || '').trim().toLowerCase();
  if (!m) return 'reflective';

  // Very short greeting-style messages.
  if (m.length <= 25 && /^(hi|hello|hey|yo|namaste|good (morning|evening|night|afternoon)|how are you|thanks?|thank you|ok|okay|cool|nice|got it|bye|aura\??)$/i.test(m)) {
    return 'casual';
  }

  // Practical "should I", "is it safe", weather/temperature, "what should I",
  // "where", "when (logistically)", "how do I", everyday recommendation requests.
  const practicalPatterns = [
    /\b(should i|is it (safe|smart|wise|worth)|can i|will it|do i need|how do i|what should i (eat|wear|do|buy|cook|say)|where (can|should) i|how much|how many|how long does)\b/i,
    /\b(temperature|weather|degree|degrees|rainy|sunny|hot|cold|humid|monsoon|traffic|metro|cab|uber|ola|flight|train|delivery|restaurant|food)\b/i,
    /\b(tomorrow|today|tonight|this evening|this morning|this afternoon|right now|currently)\b.*\b(should|safe|good|okay|ok|smart|worth)\b/i,
    /\b(was it (right|wrong|a good idea|smart)|did i (do|make) the right|in retrospect)\b/i,
    /\b(recommend|suggestion|advise|advice|tip)\b/i,
    // Real-world money / employer / payment timing. Salary from a specific
    // company is a PRACTICAL question (talk to HR), not a karmic-family
    // reflection. Catching this here stops retrieval from pulling Lal
    // Kitab "Mother's Lineage and Financial Flow" type cards onto a
    // simple "when does my salary come" question.
    /\b(salary|paycheck|pay\s*check|wages|payment|reimbursement|invoice|payout|payroll|stipend|appraisal|increment|bonus|paid|pay\s*day|pay\s*date|credit(ed)?|got\s*paid|hr\s*department|hr\s*team)\b/i,
    // Tarot requests are tarot-mode (handled in retrieval), but they get
    // the reflective register because the reply needs the symbolic voice.
    // EXCEPT when the underlying question is a real-world practical one
    // ("do a tarot to check when my Beem salary comes") which the salary
    // pattern above will already catch.
  ];
  if (practicalPatterns.some(re => re.test(m))) return 'practical';

  // Default: reflective (life / love / purpose / identity / timing / symbolic).
  return 'reflective';
}

export default async function handler(req, res) {
  // CORS preflight
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, X-Aura-Anon');
  if (req.method === 'OPTIONS') return res.status(204).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'method_not_allowed' });

  const t0 = Date.now();
  let body = req.body;
  if (typeof body === 'string') { try { body = JSON.parse(body); } catch { body = {}; } }
  body = body || {};

  const message = String(body.message || '').slice(0, 1500).trim();
  if (!message) return res.status(400).json({ error: 'message required' });

  // 1. SAFETY pre-filter, never reaches the LLM.
  const safety = preFilterSafety(message);

  // 2. SESSION: resolve user, conversation, history.
  let session;
  try {
    session = await loadSession(req, body);
  } catch (err) {
    console.error('[aura/v2/message] session load failed:', err && err.message, err && err.body);
    return res.status(500).json({ error: 'session_failed' });
  }

  // If safety blocked, reply in-character and persist the user turn only.
  if (safety) {
    sseSingleReply(res, {
      conversationId: session.conversation.id,
      messageId: null,
      text: safety.reply,
      kind: 'safety_' + safety.kind,
    });
    persistTurn({
      user: session.user, conversation: session.conversation,
      userText: message, assistantText: safety.reply,
      model: 'safety_filter', latencyMs: Date.now() - t0,
    }).catch(() => {});
    return;
  }

  // 3. QUOTA: reserve a slot in the global daily counter.
  const quota = await reserveQuota();
  if (!quota.ok) {
    sseSingleReply(res, {
      conversationId: session.conversation.id,
      messageId: null,
      text: AURA_RESTING_MESSAGE,
      kind: 'quota_exhausted',
    });
    persistTurn({
      user: session.user, conversation: session.conversation,
      userText: message, assistantText: AURA_RESTING_MESSAGE,
      model: 'quota_gate', latencyMs: Date.now() - t0,
    }).catch(() => {});
    return;
  }

  // 4. CLASSIFY register + detect reading mode.
  //    Reading mode (tarot / prashna) is detected from the current
  //    message AND the recent history. This handles the pattern:
  //      user: "Can you do prashna kundali?"
  //      aura: "What clarity do you need?"
  //      user: "will my salary come Friday?" <-- this is the prashna question
  //    Without history-awareness, that last message classifies as practical
  //    (because "salary") and skips the reading entirely.
  const register = classifyRegister(message);
  const readingMode = detectReadingMode(message, session.history);  // 'tarot' | 'prashna' | null

  // 5. RETRIEVE symbolic grounding.
  //    - readingMode === 'tarot':   pull 3 tarot cards (Past/Present/Future)
  //    - readingMode === 'prashna': pull 3 horary cards (Significator/Cusp/Timing)
  //    - reflective: regular cross-tradition retrieval (4 cards, max 1 per source)
  //    - practical / casual (without reading mode): skip retrieval entirely
  let symbols = [];
  if (readingMode === 'tarot') {
    try {
      symbols = await retrieveSymbols(message, { topK: 3, tarotMode: true });
    } catch (err) {
      console.warn('[aura/v2/message] tarot retrieve failed:', err && err.message);
    }
  } else if (readingMode === 'prashna') {
    try {
      symbols = await retrieveSymbols(message, { topK: 3, prashnaMode: true });
    } catch (err) {
      console.warn('[aura/v2/message] prashna retrieve failed:', err && err.message);
    }
  } else if (register === 'reflective') {
    try {
      symbols = await retrieveSymbols(message, { topK: 4 });
    } catch (err) {
      console.warn('[aura/v2/message] retrieve failed:', err && err.message);
    }
  }

  // 5. PROMPT (with register hint so Gemini knows which voice to use)
  const profile = (body.profile && typeof body.profile === 'object') ? body.profile : (session.user.profile || {});
  const system = buildAuraPrompt({
    profile,
    memories: null,   // Phase B
    symbols,
    sky: null,        // Phase B
  });
  const askingTime = isTimingQuestion(message);

  // Build an internal hint that locks Gemini into the right register,
  // so the regex classifier's call wins even if Gemini would have
  // classified the message differently.
  let registerHint;

  if (readingMode === 'tarot' && symbols.length >= 1) {
    // Tarot reading mode: structured Past / Present / Future with named cards.
    const labels = ['Past', 'Present', 'Future'];
    const cardList = symbols.slice(0, 3).map((s, i) =>
      `  ${labels[i] || 'Card ' + (i + 1)}: "${s.name}" — ${s.body.slice(0, 180)}`
    ).join('\n');
    registerHint = [
      '[INTERNAL: TAROT READING MODE.',
      'The user explicitly asked for a tarot reading. Do a structured 3-card reading.',
      'The cards drawn (in order Past, Present, Future):',
      cardList,
      '',
      'STRUCTURE OF YOUR REPLY:',
      '1. Name all three cards by their actual names in one short opener.',
      '2. Then for EACH card (Past, Present, Future), write 1-2 sentences interpreting it',
      '   IN THE SPECIFIC CONTEXT of the user\'s exact question.',
      '3. End with a short, grounded summary line.',
      '',
      'CRITICAL: anchor every interpretation in the SPECIFIC subject the user named',
      '(employer, company name, salary, partner name, the exact decision, etc.).',
      'Do NOT drift into abstract themes. If the user asked about salary from a named',
      'company, the reading is about the salary from that company, NOT about family karma.]',
    ].join('\n');

  } else if (readingMode === 'prashna' && symbols.length >= 1) {
    // Prashna kundali (horary) mode: structured Significator / Cusp / Timing.
    const labels = ['Significator', 'Cusp Reading', 'Timing'];
    const cardList = symbols.slice(0, 3).map((s, i) =>
      `  ${labels[i] || 'Element ' + (i + 1)}: "${s.name}" — ${s.body.slice(0, 200)}`
    ).join('\n');
    registerHint = [
      '[INTERNAL: PRASHNA KUNDALI / HORARY READING MODE.',
      'The user explicitly asked for a prashna (horary) reading. This is the Indic and',
      'Western horary tradition of reading the chart of the MOMENT the question was asked.',
      'The horary cards drawn:',
      cardList,
      '',
      'STRUCTURE OF YOUR REPLY:',
      '1. Open by naming this as a prashna reading on the user\'s specific question.',
      '2. Significator: 1-2 sentences on who/what represents the matter (the asker,',
      '   the company, the salary, the partner, the situation). Use plain everyday',
      '   English, NOT jargon like "10th lord" or "lagna".',
      '3. Cusp Reading: 1-2 sentences on the current state of the matter, with a CLEAR',
      '   yes / leaning yes / leaning no / no signal.',
      '4. Timing: 1-2 sentences giving a specific tentative future window for resolution',
      '   (e.g. "within the next 7 to 10 days", "before the second week of June").',
      '   The window MUST be in the future relative to today.',
      '5. End with a single sentence of grounded human guidance.',
      '',
      'CRITICAL:',
      '- Anchor in the SPECIFIC subject (employer name, person, decision) the user named.',
      '- NEVER use horary jargon ("malefic", "10th house", "rashi", "nakshatra").',
      '- Translate the symbolic reading into plain English the user can act on.',
      '- For "will I get my Beem April salary in June first week" type questions, give a',
      '  clear directional answer: leaning yes (first week likely), leaning no (delayed,',
      '  expect second/third week), or yes (looks well-aspected for first week).]',
    ].join('\n');

  } else {
    registerHint =
      register === 'casual'    ? '[INTERNAL: This is a CASUAL message. Reply with ONE warm sentence. No numerology. No symbolic framing.]' :
      register === 'practical' ? '[INTERNAL: This is a PRACTICAL everyday question. Reply like a thoughtful friend, 2 to 4 sentences, lead with a clear useful answer. Do NOT force numerology, planets, or symbolic framing. If the user named a specific company, person, or thing, your reply MUST stay anchored on THAT specific subject, not drift into general themes.]' :
                                 '[INTERNAL: This is a REFLECTIVE question. 1 to 2 sentences, warm and grounded, drawing on the cards if they fit. Anchor your reply in the SPECIFIC subject the user named (their job, their partner, their company, their decision), not abstract themes.]';
  }

  const userText = (
    message + '\n\n' + registerHint +
    (askingTime ? '\n\n[INTERNAL: This is also a timing question. Include a specific tentative future window like "in the next 4 to 6 weeks" or "before the year-end". The window MUST be in the future relative to today.]' : '')
  );

  // 6. STREAM
  startSSE(res);
  // Optimistic insert of the user message so it's persisted even if the
  // stream is cut mid-reply. We persist the assistant turn at the end.
  let userMessageId = null;
  try {
    const row = await insertInto('aura_messages', {
      conversation_id: session.conversation.id,
      user_id: session.user.id,
      role: 'user',
      content: message,
    });
    userMessageId = row && row.id || null;
  } catch (err) {
    console.error('[aura/v2/message] user-message insert failed:', err && err.message);
  }

  sendEvent(res, 'started', {
    conversationId: session.conversation.id,
    messageId: userMessageId,
    anonToken: session.anonToken || undefined,
  });
  sendEvent(res, 'thinking', { stage: 'composing' });

  let modelUsed = null;
  const collected = [];
  let streamError = null;

  try {
    for await (const chunk of streamLLM({ system, userText, history: session.history })) {
      const safe = sanitizeChunk(chunk.text || '');
      if (!safe) continue;
      modelUsed = chunk.model || modelUsed;
      collected.push(safe);
      sendEvent(res, 'token', { text: safe });
    }
  } catch (err) {
    streamError = err;
    console.error('[aura/v2/message] stream failed:', err && err.message, err && err.body);
  }

  let assistantText = collected.join('');
  if (!assistantText) {
    // Pick a clearer fallback based on what actually failed.
    // 429 / rate-limited: tell the user to wait a moment.
    // Anything else: generic try-again.
    const status = streamError && streamError.status;
    const body   = (streamError && String(streamError.body || streamError.message || '')) || '';
    const isRateLimit = status === 429 || /quota|rate.?limit|exceeded|too many/i.test(body);
    if (isRateLimit) {
      assistantText = "Aura is briefly catching her breath, this happens when many people are asking at once. Please try again in about a minute.";
    } else {
      assistantText = "Aura could not reach the line just now. Please try sending that again, and if it keeps happening, refresh the page.";
    }
    sendEvent(res, 'token', { text: assistantText });
  }
  // Sentence cap depends on register.
  // Tarot reading (opener + 3 cards × 2 sentences + closer) = 9.
  // Prashna reading (significator + cusp + timing + closer + framing) = 9.
  // Practical questions: 4. Casual: 1. Reflective default: 2.
  const readingActive = (readingMode === 'tarot' || readingMode === 'prashna') && symbols.length >= 1;
  const maxSentences =
    readingActive            ? 9 :
    register === 'practical' ? 4 :
    askingTime               ? 3 :
    register === 'casual'    ? 1 :
                               2;
  assistantText = finalize(assistantText, { maxSentences });

  sendEvent(res, 'done', {
    kind: streamError ? 'partial' : 'ok',
    model: modelUsed || 'fallback',
    latencyMs: Date.now() - t0,
    quotaCount: quota.count,
    quotaCap: quota.cap,
  });
  endSSE(res);

  // 7. PERSIST (async)
  // We already wrote the user message above; only persist the assistant turn now.
  insertInto('aura_messages', {
    conversation_id: session.conversation.id,
    user_id: session.user.id,
    role: 'assistant',
    content: assistantText,
    model_used: modelUsed || (streamError ? 'fallback_error' : 'unknown'),
    latency_ms: Date.now() - t0,
    symbol_ids: (symbols || []).map(s => s.id).filter(Boolean),
  }).catch(err => console.error('[aura/v2/message] assistant-message insert failed:', err && err.message));
}
