/**
 * Gemini text-embedding-004 wrapper.
 * Returns a Float32 array of length 768 per input string.
 *
 * Shared with runtime retrieval (api/aura/v2/_lib/embeddings.js wraps
 * this same endpoint for online queries).
 */

'use strict';

const MODEL = 'gemini-embedding-001';
const OUT_DIM = 768;

async function embedTexts(texts, apiKey) {
  if (!apiKey) throw new Error('GEMINI_API_KEY not set');
  if (!Array.isArray(texts) || !texts.length) return [];

  // Batch endpoint: batchEmbedContents
  const url = 'https://generativelanguage.googleapis.com/v1beta/models/'
    + MODEL + ':batchEmbedContents?key=' + encodeURIComponent(apiKey);
  const body = {
    requests: texts.map(t => ({
      model: 'models/' + MODEL,
      content: { parts: [{ text: String(t).slice(0, 8000) }] },
      taskType: 'RETRIEVAL_DOCUMENT',
      outputDimensionality: OUT_DIM,
    })),
  };

  const r = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  if (!r.ok) {
    const t = await r.text().catch(() => '');
    throw Object.assign(new Error('embed_failed_' + r.status), { body: t.slice(0, 400) });
  }
  const data = await r.json();
  const out  = (data.embeddings || []).map(e => (e && e.values) || []);
  return out;
}

async function embedText(text, apiKey, taskType = 'RETRIEVAL_QUERY') {
  if (!apiKey) throw new Error('GEMINI_API_KEY not set');
  const url = 'https://generativelanguage.googleapis.com/v1beta/models/'
    + MODEL + ':embedContent?key=' + encodeURIComponent(apiKey);
  const body = {
    model: 'models/' + MODEL,
    content: { parts: [{ text: String(text).slice(0, 8000) }] },
    taskType,
    outputDimensionality: OUT_DIM,
  };
  const r = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  if (!r.ok) {
    const t = await r.text().catch(() => '');
    throw Object.assign(new Error('embed_failed_' + r.status), { body: t.slice(0, 400) });
  }
  const data = await r.json();
  return (data.embedding && data.embedding.values) || [];
}

export { embedTexts, embedText };
