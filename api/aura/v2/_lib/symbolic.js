/**
 * Symbolic retrieval. pgvector cosine search across aura_symbols
 * (Cheiro, Prashna Marga, Lal Kitab, Lilly horary, Hermetic, etc.),
 * then a lightweight in-process re-rank to favour cards whose intent
 * tags match the user's question category.
 *
 * Returns top-K cards or [] if the corpus is empty / retrieval fails.
 * Never throws to the caller, retrieval is a best-effort enrichment.
 */

'use strict';

import { embedQuery } from './embeddings.js';
import { rpc } from './supabaseAdmin.js';

// Same closed-set tag vocab as ingestion/extract.js. Used for cheap
// keyword-to-tag mapping when we don't yet have a classifier.
const KEYWORD_TO_TAGS = {
  job:        ['career'],
  career:     ['career','recognition'],
  work:       ['career'],
  promotion:  ['career','recognition'],
  business:   ['career','money'],
  money:      ['money'],
  rich:       ['money'],
  love:       ['love','relationships'],
  partner:    ['relationships','love'],
  marriage:   ['marriage','relationships'],
  marry:      ['marriage'],
  family:     ['family','relationships'],
  health:     ['health','healing'],
  heal:       ['healing'],
  abroad:     ['abroad','relocation'],
  travel:     ['abroad','relocation'],
  move:       ['relocation'],
  relocate:   ['relocation'],
  purpose:    ['purpose','identity','spiritual'],
  meaning:    ['purpose','spiritual'],
  stuck:      ['delay','change'],
  blocked:    ['delay'],
  when:       ['timing'],
  conflict:   ['conflict'],
  fight:      ['conflict'],
};

function inferIntentTags(message) {
  const m = String(message || '').toLowerCase();
  const tags = new Set();
  for (const [k, vs] of Object.entries(KEYWORD_TO_TAGS)) {
    if (m.includes(k)) vs.forEach(v => tags.add(v));
  }
  return Array.from(tags);
}

/**
 * Retrieve top-K symbol cards relevant to the user's message.
 * Returns: [ { id, name, body, planet, source, source_ref, intent_tags, similarity } ]
 *
 * Behaviour:
 *   - Embed the user message (RETRIEVAL_QUERY task type)
 *   - pgvector cosine top-20 from aura_symbols
 *   - Re-rank: similarity + 0.05 per matching intent tag
 *   - Return top topK
 *
 * Best-effort: any failure returns [] and logs.
 */
async function retrieveSymbols(message, { topK = 4 } = {}) {
  const text = String(message || '').trim();
  if (!text) return [];

  let qEmb;
  try {
    qEmb = await embedQuery(text);
  } catch (err) {
    console.warn('[aura/symbolic] embed failed, skipping retrieval:', err && err.message);
    return [];
  }
  if (!Array.isArray(qEmb) || qEmb.length !== 768) return [];

  let rows = [];
  try {
    rows = await rpc('match_aura_symbols', {
      query_embedding: qEmb,
      match_count: 20,
    });
  } catch (err) {
    console.warn('[aura/symbolic] rpc failed, skipping retrieval:', err && err.message);
    return [];
  }
  if (!Array.isArray(rows) || !rows.length) return [];

  const intentTags = inferIntentTags(text);
  const scored = rows.map(r => {
    const overlap = Array.isArray(r.intent_tags)
      ? r.intent_tags.filter(t => intentTags.includes(t)).length
      : 0;
    return Object.assign({}, r, { score: (r.similarity || 0) + 0.05 * overlap });
  });
  scored.sort((a, b) => b.score - a.score);

  // Take top-K but ensure source diversity: max 2 from the same source.
  const out = [];
  const perSource = {};
  for (const r of scored) {
    const src = r.source || 'unknown';
    if ((perSource[src] || 0) >= 2) continue;
    out.push(r);
    perSource[src] = (perSource[src] || 0) + 1;
    if (out.length >= topK) break;
  }
  return out;
}

export { retrieveSymbols, inferIntentTags };
