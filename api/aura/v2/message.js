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
import { retrieveSymbols } from './_lib/symbolic.js';
import { sanitizeChunk, finalize, isTimingQuestion } from './_lib/sanitize.js';
import { persistTurn } from './_lib/persistTurn.js';
import { startSSE, sendEvent, endSSE, sseSingleReply } from './_lib/sse.js';
import { insertInto } from './_lib/supabaseAdmin.js';

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

  // 4. RETRIEVE symbolic grounding (Phase C). Best-effort.
  //    Returns [] if the corpus is empty or embedding fails.
  let symbols = [];
  try {
    symbols = await retrieveSymbols(message, { topK: 4 });
  } catch (err) {
    console.warn('[aura/v2/message] retrieve failed:', err && err.message);
  }

  // 5. PROMPT
  const profile = (body.profile && typeof body.profile === 'object') ? body.profile : (session.user.profile || {});
  const system = buildAuraPrompt({
    profile,
    memories: null,   // Phase B
    symbols,
    sky: null,        // Phase B
  });
  const askingTime = isTimingQuestion(message);
  const userText = askingTime
    ? message + '\n\n[INTERNAL: This is a timing question. Your reply MUST contain a specific tentative window, e.g. "in the next 4 to 6 weeks" or "before the year-end". A reply without a window fails the brief.]'
    : message;

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
    // Last-resort fallback so the user never sees an empty bubble.
    assistantText = "The signal is faint just now. Try again in a moment, sometimes the pattern needs a beat to settle.";
    sendEvent(res, 'token', { text: assistantText });
  }
  assistantText = finalize(assistantText, { maxSentences: askingTime ? 3 : 2 });

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
