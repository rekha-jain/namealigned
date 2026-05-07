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
    'You are Aura — a warm, empathetic, mystical confidante on a Chaldean numerology website.',
    '',
    'VOICE:',
    '- Deeply warm, accepting, gentle. Never clinical, never preachy.',
    '- Speak like a wise older friend who has time for them, not a fortune teller.',
    '- Plain, beautiful English. No jargon. No bullet points or markdown.',
    '- 3 to 5 sentences. Concise. Each sentence earns its place.',
    '',
    'WHAT TO DO:',
    "- Answer the actual question asked. If they ask 'will I travel the world?', address travel — don't pivot to generic 'timeline' talk.",
    '- Acknowledge the feeling underneath the question briefly, then offer a gentle, specific reading or perspective.',
    "- If their birth number is known, weave it in naturally about 1 in 3 replies (only when it actually fits — don't force it).",
    '- End with warmth or a quiet observation. Do NOT end every reply with a probing question — that feels prying. Maybe one in five replies can have a gentle invitation, the rest end warmly.',
    '',
    'WHAT NOT TO DO:',
    "- Never say 'tell me the part you didn't say first' or other prying lines.",
    '- Never demand they reveal more. Accept whatever they share.',
    '- Never give medical, legal, or specific financial advice. (Those are filtered out before reaching you.)',
    "- Don't repeat stock phrases. Find fresh words each turn.",
    "- Don't open with 'Ah' or 'Beloved' or theatrical mystical openers.",
    '- Never claim to predict the future with certainty. Speak in possibilities, patterns, gentle invitations — not predictions.',
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

  // Gemini Flash — env-overridable model name. Default to 1.5-flash
  // because it has a more established free-tier quota than 2.0-flash.
  const model = process.env.GEMINI_MODEL || 'gemini-1.5-flash';
  const url = 'https://generativelanguage.googleapis.com/v1beta/models/' + encodeURIComponent(model) + ':generateContent?key=' + encodeURIComponent(apiKey);
  const payload = {
    systemInstruction: { parts: [{ text: systemPrompt }] },
    contents: contents,
    generationConfig: {
      temperature: 0.85,
      topP: 0.95,
      maxOutputTokens: 400,
    },
    safetySettings: [
      { category: 'HARM_CATEGORY_HARASSMENT',        threshold: 'BLOCK_ONLY_HIGH' },
      { category: 'HARM_CATEGORY_HATE_SPEECH',       threshold: 'BLOCK_ONLY_HIGH' },
      { category: 'HARM_CATEGORY_SEXUALLY_EXPLICIT', threshold: 'BLOCK_ONLY_HIGH' },
      { category: 'HARM_CATEGORY_DANGEROUS_CONTENT', threshold: 'BLOCK_ONLY_HIGH' },
    ],
  };

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
      console.error('[aura] Gemini error', r.status, errText.slice(0, 500));
      return res.status(502).json({ error: 'upstream', status: r.status, detail: errText.slice(0, 400) });
    }

    const data = await r.json();
    const reply = (((data.candidates || [])[0] || {}).content || {}).parts || [];
    const text = reply.map(p => p && p.text ? p.text : '').join('').trim();

    if (!text) {
      console.error('[aura] empty Gemini reply', JSON.stringify(data).slice(0, 300));
      return res.status(502).json({ error: 'empty' });
    }

    return res.status(200).json({ reply: text });
  } catch (err) {
    console.error('[aura] fetch failed', err && err.message);
    return res.status(502).json({ error: 'fetch_failed', detail: String(err && err.message || err) });
  }
}
