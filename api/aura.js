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
    'WHEN THEY ASK ABOUT TIMING / WHEN / HOW LONG:',
    '- Always offer a specific tentative window — for example: "in the next 4 to 6 weeks", "around the end of this season", "between now and August", "within 2 to 3 months".',
    "- Never refuse to give a timeframe. Even a soft window (\"sometime this autumn\") is more useful than \"in time\".",
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
  const contents     = toGeminiContents(history, message);

  // Model cascade — gemini-2.5-flash is the flagship but its free tier
  // gets 503-overloaded; lite has more headroom. Try in order until
  // one succeeds.
  const MODELS = ['gemini-2.5-flash-lite', 'gemini-2.5-flash', 'gemini-flash-latest'];
  const payload = {
    systemInstruction: { parts: [{ text: systemPrompt }] },
    contents: contents,
    generationConfig: {
      temperature: 0.8,
      topP: 0.95,
      maxOutputTokens: 180,
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
      const text = sanitizeReply(raw);

      if (!text) {
        lastStatus = 502;
        lastDetail = 'empty';
        console.error('[aura] empty reply model=' + model, JSON.stringify(data).slice(0, 300));
        continue;
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
