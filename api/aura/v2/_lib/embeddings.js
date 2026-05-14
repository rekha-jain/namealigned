/**
 * Runtime Gemini text-embedding-004 wrapper.
 * Used by symbolic retrieval and (later) memory recall.
 *
 * Same model as ingestion/embed.js, kept separate so the server bundle
 * does not depend on local ingestion code.
 */

'use strict';

const MODEL = 'gemini-embedding-001';
const OUT_DIM = 768;

async function embedQuery(text) {
  const apiKey = process.env.GEMINI_API_KEY;
  if (!apiKey) throw new Error('GEMINI_API_KEY not set');

  const url = 'https://generativelanguage.googleapis.com/v1beta/models/'
    + MODEL + ':embedContent?key=' + encodeURIComponent(apiKey);
  const body = {
    model: 'models/' + MODEL,
    content: { parts: [{ text: String(text).slice(0, 4000) }] },
    taskType: 'RETRIEVAL_QUERY',
    outputDimensionality: OUT_DIM,
  };

  const ctrl = new AbortController();
  const t = setTimeout(() => ctrl.abort(), 8000);
  try {
    const r = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
      signal: ctrl.signal,
    });
    if (!r.ok) {
      const errText = await r.text().catch(() => '');
      throw Object.assign(new Error('embed_failed_' + r.status), { body: errText.slice(0, 300) });
    }
    const data = await r.json();
    return (data.embedding && data.embedding.values) || [];
  } finally {
    clearTimeout(t);
  }
}

export { embedQuery };
