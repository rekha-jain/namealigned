/**
 * Vercel Serverless Function, POST /api/aura
 *
 * The Aura conversational backend. Receives a user message + optional
 * Chaldean numerology profile + recent chat history, calls Google
 * Gemini 2.0 Flash with a warm empathetic system prompt, and returns
 * the reply as plain text.
 *
 * Required environment variable:
 *   GEMINI_API_KEY — free tier key from https://aistudio.google.com/app/apikey
 */

'use strict';

const CORS_HEADERS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
};

const PLANET_BY_NUM = ['', 'Sun', 'Moon', 'Jupiter', 'Rahu', 'Mercury', 'Venus', 'Ketu', 'Saturn', 'Mars'];
const NUM_TRAITS = {
  1: 'Sun-led — leadership without permission, visibility that finds them.',
  2: 'Moon-led — emotionally porous, partnership-oriented, deeply intuitive.',
  3: 'Jupiter-led — expressive, expansive, drawn to teaching and abundance.',
  4: 'Rahu-led — unconventional, ahead of consensus, often misread before understood.',
  5: 'Mercury-led — fast, adaptive, communicative, hard to confine.',
  6: 'Venus-led — relational, aesthetic, devoted, emotionally fluent.',
  7: 'Ketu-led — depth-oriented, contemplative, comfortable with questions over answers.',
  8: 'Saturn-led — disciplined, long-game, authority earned through endurance.',
  9: 'Mars-led — courageous, decisive, energy that runs hot and protective.',
};

function buildSystemPrompt(profile) {
  const planet = profile && profile.birthNum ? PLANET_BY_NUM[profile.birthNum] : '';
  const trait  = profile && profile.birthNum ? NUM_TRAITS[profile.birthNum]   : '';
  const namePart = profile && profile.firstName ? `The seeker's name is ${profile.firstName}.` : '';
  const numPart  = profile && profile.birthNum
    ? `Their Chaldean Birth Number is ${profile.birthNum} (ruling planet: ${planet}). Trait: ${trait}`
    : '';
  return [
    'You are Aura — a warm, mystical, slightly playful confidante on a Chaldean numerology website.',
    'Imagine a wise older friend who is also a little bit witch, a little bit storyteller. Mystical without being heavy.',
    '',
    'LENGTH:',
    '- 2 to 3 sentences. Max ~50 words. This is a chat bubble, not an essay.',
    '- If a 1-sentence answer is enough, give that.',
    '',
    'VOICE:',
    '- Warm, accepting, gently mystical. Hints of mystery, a touch of fun, never preachy.',
    '- Plain English. NO markdown — never use **bold**, *italics*, bullets, headers, or asterisks of any kind.',
    "- Never start with 'Ah,' 'Oh,' 'Beloved,' 'Dear one,' or theatrical mystical openers. Begin naturally.",
    '',
    'TIMING WINDOWS — ONLY WHEN THE USER EXPLICITLY ASKS ABOUT TIMING:',
    '- DO NOT volunteer a timeframe in regular replies. If the user did not ask about "when", "how long", "how soon", "by when", or a similar timing phrase, your reply should NOT contain a specific window. Just answer warmly without dates or windows.',
    '- ONLY when the user is explicitly asking about timing/when/how-long, your reply MUST contain a tentative window.',
    '- Match the SCALE of the window to the kind of question, and VARY it from reply to reply. Do NOT default to "4 to 6 months" every time.',
    '- Scales to draw from based on context:',
    '   • Small, immediate things (a conversation, a meeting, a sign): "within the next 2 to 3 weeks", "in the coming 10 to 14 days", "before the next new moon".',
    '   • Mid-term shifts (jobs, relationships clarifying): "in the next 6 to 9 weeks", "around 2 to 3 months from now", "before the season turns".',
    '   • Larger cycles (business success, deep transformations, big moves): "across the next 6 to 12 months", "by the time we reach early next year", "in the coming 9 to 14 months", "within the next personal-year cycle".',
    '   • Long-arc spiritual/identity shifts: "over the next 2 to 3 years", "across this current Saturn cycle".',
    "- You can also use mystical markers: 'by the next full moon', 'before your next birthday', 'as the year-end approaches'.",
    "- Frame it gently (\"the patterns suggest…\", \"the timing feels like…\") — never a guarantee, always a tentative read.",
    "- Vary your windows turn-to-turn. Repeating the same range across questions feels lazy and formulaic.",
    '',
    'KEEPING IT INTERESTING:',
    "- It's okay (about 1 in 3 turns) to end with a SOFT mystical or playful question — something that invites them deeper but never pries. Examples: \"Have you noticed any small signs lately?\" / \"Does the number 7 feel familiar to you right now?\" / \"What part of this surprises you?\"",
    "- Never ask invasive questions like 'tell me the part you didn't say' or 'what conversation are you avoiding'. Soft, curious, fun — not therapist-style.",
    '- The other 2 in 3 turns, end warmly without a question.',
    '',
    'WHAT TO DO:',
    "- Answer the actual question. Travel question → talk about travel. Love question → talk about love.",
    '- Use birth-number / planet context only when it genuinely fits — never as filler.',
    '',
    'WHAT NOT TO DO:',
    "- Never use markdown formatting of any kind.",
    "- Never demand they reveal more. Accept whatever they share.",
    '- Never give medical, legal, or specific financial advice.',
    "- Never claim to predict the future with certainty. Speak in patterns and possibilities.",
    '',
    'SEEKER CONTEXT:',
    namePart,
    numPart,
    '',
    'Respond now to their next message with warmth and specificity.',
  ].filter(Boolean).join('\n');
}

// Convert OpenAI-style chat history to Gemini's `contents` format.
// Gemini uses role: 'user' | 'model' and parts: [{text}].
// Strip markdown formatting and cap to 2 sentences for the chat-bubble UI.
function sanitizeReply(text) {
  if (!text) return '';
  let out = String(text);
  // Strip bold/italic/code markdown
  out = out.replace(/\*\*([^*]+)\*\*/g, '$1');
  out = out.replace(/\*([^*]+)\*/g, '$1');
  out = out.replace(/__([^_]+)__/g, '$1');
  out = out.replace(/_([^_]+)_/g, '$1');
  out = out.replace(/`([^`]+)`/g, '$1');
  // Strip bullet/list markers and headers
  out = out.replace(/^\s*#{1,6}\s+/gm, '');
  out = out.replace(/^\s*[-*•]\s+/gm, '');
  out = out.replace(/^\s*\d+\.\s+/gm, '');
  // Strip theatrical openers
  out = out.replace(/^(Ah|Oh|Beloved|Dear one|My dear)[,!.]\s+/i, '');
  // Collapse whitespace
  out = out.replace(/\s+/g, ' ').trim();
  // Cap at 3 sentences
  const sentences = out.match(/[^.!?]+[.!?]+/g) || [out];
  if (sentences.length > 3) {
    out = sentences.slice(0, 3).join('').trim();
  }
  return out;
}

// Did the user ask a timing/when question?
function isTimingQuestion(text) {
  if (!text) return false;
  const t = text.toLowerCase();
  return /\b(when|how long|how soon|by when|in what time|time frame|timeframe|how many (days|weeks|months|years)|days|weeks|months|years|soon|deadline|by which time|in how much time)\b/.test(t);
}

// Pick a fallback timeframe sentence sized to the topic of the question.
// Used only as a last-resort safety net when the model dodges entirely.
function fallbackWindow(text, history) {
  const all = [text || '', ...((history || []).map(h => h && h.content || ''))].join(' ').toLowerCase();
  const pickFrom = (arr) => arr[Math.floor(Math.random() * arr.length)];

  // Career / business / money — longer cycles
  if (/\b(business|venture|career|promotion|job|salary|raise|startup|founder|client|company|launch|investor|deal|profit|revenue|wealth|rich)\b/.test(all)) {
    return pickFrom([
      'The patterns suggest meaningful traction across the next 6 to 9 months, with the clearer turn around the second half.',
      'A tentative read: the real momentum builds in the coming 8 to 12 months, gathering pace as the year matures.',
      'My sense is that the visible breakthrough lands somewhere between 4 and 7 months from now.',
      'The arc here is closer to a year — expect the meaningful shift in the next 9 to 14 months.',
    ]);
  }

  // Love / relationship — weeks to a few months
  if (/\b(love|relationship|partner|marriage|marry|wife|husband|boyfriend|girlfriend|crush|soulmate|dating|breakup|ex|romance|heart)\b/.test(all)) {
    return pickFrom([
      'The pattern softens within the next 6 to 10 weeks — clarity arrives sooner than the asking suggests.',
      'My read: the meaningful turn lands in the coming 2 to 3 months.',
      'A gentle window — between now and the next new moon, something will move.',
      'Expect the picture to clarify across the next 8 to 12 weeks.',
    ]);
  }

  // Travel — seasonal
  if (/\b(travel|trip|abroad|move|relocat|country|visa|migrat)\b/.test(all)) {
    return pickFrom([
      'The pattern points to movement across the next 4 to 8 months, often through an unexpected channel.',
      'A soft window — somewhere between this season and the one after, doors open.',
      'My sense: 5 to 9 months ahead, the road begins to lay itself out.',
    ]);
  }

  // Health / energy — shorter
  if (/\b(health|tired|exhaust|burnout|anxi|sleep|illness|recover|heal)\b/.test(all)) {
    return pickFrom([
      'The body asks for 3 to 5 weeks of gentler rhythm before the shift becomes visible.',
      'Expect noticeable improvement across the next 4 to 8 weeks if you honour the rest.',
      'A soft window — by the time the next month closes, something steadies.',
    ]);
  }

  // Self / identity / purpose — long arc
  if (/\b(purpose|meaning|self|identity|lost|stuck|direction|who am i|why am i)\b/.test(all)) {
    return pickFrom([
      'The recalibration sits across the next 6 to 10 weeks; the clarity arrives in pieces.',
      'A longer read here — the new self lands across the next 2 to 4 months, gradually.',
      'Expect the meaning to settle in the coming season or two, not all at once.',
    ]);
  }

  // Generic — varied
  return pickFrom([
    'The pattern points to a meaningful shift in the coming 6 to 10 weeks.',
    'A tentative window — between now and the close of the next season.',
    'My read: the turn lands somewhere in the next 3 to 5 months.',
    'A soft window: across the next 2 to 4 months, the picture sharpens.',
    'The patterns suggest movement before this year quietly closes.',
    'Expect the shift to crystallise within the next 90 to 120 days.',
  ]);
}

// Does the reply contain a tentative time window?
function hasTimeWindow(text) {
  if (!text) return false;
  return /\b(\d+\s*(?:to|–|-)\s*\d+\s*(week|month|year|day|quarter)s?|within (?:the )?next \d|next \d+\s*(week|month|year|day|quarter)|by (?:the end of |mid-)?(?:january|february|march|april|may|june|july|august|september|october|november|december|spring|summer|autumn|fall|winter|this season|next season|this year|next year|year-end)|\bthis (?:season|year|quarter|month)|\bnext (?:season|year|quarter|month)|by (?:the next )?(?:full moon|new moon|moon cycle)|before (?:this|the) (?:year|season|quarter) (?:closes|ends)|in the coming (?:weeks|months)|over the next \d|\b\d+\s*(week|month|year)s?\b)/i.test(text);
}

function toGeminiContents(history, userMessage) {
  const out = [];
  for (const m of history || []) {
    if (!m || !m.content) continue;
    if (m.role === 'user' || m.role === 'assistant') {
      out.push({
        role: m.role === 'assistant' ? 'model' : 'user',
        parts: [{ text: String(m.content) }],
      });
    }
  }
  out.push({ role: 'user', parts: [{ text: String(userMessage) }] });
  return out;
}

export default async function handler(req, res) {
  // CORS
  Object.entries(CORS_HEADERS).forEach(([k, v]) => res.setHeader(k, v));
  if (req.method === 'OPTIONS') return res.status(204).end();
  if (req.method !== 'POST')   return res.status(405).json({ error: 'Method Not Allowed' });

  const apiKey = process.env.GEMINI_API_KEY;
  if (!apiKey) {
    return res.status(500).json({ error: 'GEMINI_API_KEY not configured' });
  }

  let body = req.body;
  if (typeof body === 'string') {
    try { body = JSON.parse(body); } catch { body = {}; }
  }
  body = body || {};

  const message = String(body.message || '').slice(0, 1500).trim();
  const profile = body.profile || {};
  const history = Array.isArray(body.history) ? body.history.slice(-8) : [];

  if (!message) return res.status(400).json({ error: 'message required' });

  const systemPrompt = buildSystemPrompt(profile);
  const askingTime   = isTimingQuestion(message);
  // If they asked about timing, prefix the user message with a hard
  // reminder so the model can't slip past the rule.
  const effectiveMessage = askingTime
    ? message + '\n\n[INTERNAL REMINDER — DO NOT REPEAT TO USER: This is a timing question. Your reply MUST contain a specific tentative window like "within the next 4 to 6 months" or "before this year closes" or "in 2 to 3 quarters". A reply without such a window is a failed reply.]'
    : message;
  const contents     = toGeminiContents(history, effectiveMessage);

  // Model cascade — gemini-2.5-flash is the flagship but its free tier
  // gets 503-overloaded; lite has more headroom. Try in order until
  // one succeeds.
  const MODELS = ['gemini-flash-latest', 'gemini-2.5-flash', 'gemini-2.5-flash-lite'];
  const payload = {
    systemInstruction: { parts: [{ text: systemPrompt }] },
    contents: contents,
    generationConfig: {
      temperature: 0.8,
      topP: 0.95,
      maxOutputTokens: 600,
      // Gemini 2.5 burns "thinking" tokens silently against this
      // budget — disable to keep replies fast and full.
      thinkingConfig: { thinkingBudget: 0 },
    },
    safetySettings: [
      { category: 'HARM_CATEGORY_HARASSMENT',        threshold: 'BLOCK_ONLY_HIGH' },
      { category: 'HARM_CATEGORY_HATE_SPEECH',       threshold: 'BLOCK_ONLY_HIGH' },
      { category: 'HARM_CATEGORY_SEXUALLY_EXPLICIT', threshold: 'BLOCK_ONLY_HIGH' },
      { category: 'HARM_CATEGORY_DANGEROUS_CONTENT', threshold: 'BLOCK_ONLY_HIGH' },
    ],
  };

  let lastStatus = 0, lastDetail = '';
  for (const model of MODELS) {
    const url = 'https://generativelanguage.googleapis.com/v1beta/models/' + encodeURIComponent(model) + ':generateContent?key=' + encodeURIComponent(apiKey);
    try {
      const ctrl = new AbortController();
      const t = setTimeout(() => ctrl.abort(), 15000);
      const r = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
        signal: ctrl.signal,
      });
      clearTimeout(t);

      if (!r.ok) {
        const errText = await r.text().catch(() => '');
        lastStatus = r.status;
        lastDetail = errText.slice(0, 400);
        console.error('[aura] Gemini error model=' + model, r.status, errText.slice(0, 300));
        // 503 / 429 / 500 → try next model. Other errors (404, 401, 403) → bail.
        if (r.status === 503 || r.status === 429 || r.status === 500) continue;
        return res.status(502).json({ error: 'upstream', status: r.status, detail: lastDetail, model });
      }

      const data = await r.json();
      const parts = (((data.candidates || [])[0] || {}).content || {}).parts || [];
      const raw = parts.map(p => p && p.text ? p.text : '').join('').trim();
      let text = sanitizeReply(raw);

      if (!text) {
        lastStatus = 502;
        lastDetail = 'empty';
        console.error('[aura] empty reply model=' + model, JSON.stringify(data).slice(0, 300));
        continue;
      }

      // If the user asked about timing but the model dodged it,
      // append a topic-aware tentative window so they never get a
      // non-answer. Window varies by question topic + a random pick
      // so it doesn't feel formulaic across turns.
      if (askingTime && !hasTimeWindow(text)) {
        text = (text + ' ' + fallbackWindow(message, history)).trim();
        text = sanitizeReply(text);
      }

      return res.status(200).json({ reply: text, model });
    } catch (err) {
      lastStatus = 502;
      lastDetail = String(err && err.message || err);
      console.error('[aura] fetch failed model=' + model, err && err.message);
      continue;
    }
  }

  return res.status(502).json({ error: 'all_models_failed', status: lastStatus, detail: lastDetail });
}
