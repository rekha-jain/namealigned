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
 * Detect when the user explicitly asked for a tarot reading.
 * Matches: tarot, tarrot (common misspelling), pull cards, do a reading,
 * card reading, draw a card.
 */
function isTarotRequest(message) {
  const m = String(message || '').toLowerCase();
  return /\b(tarr?ot|pull\s+(?:a\s+)?cards?|do\s+a\s+(?:tarr?ot\s+)?reading|card\s+reading|draw\s+(?:a|the)?\s*cards?)\b/i.test(m);
}

/**
 * Retrieve top-K symbol cards relevant to the user's message.
 * Returns: [ { id, name, body, planet, source, source_ref, intent_tags, similarity } ]
 *
 * Options:
 *   topK            (number, default 4)
 *   tarotMode       (bool, default false)  if true, pulls 3 tarot cards only
 *   excludeSources  (array, optional) sources to filter out of results
 *
 * Best-effort: any failure returns [] and logs.
 */
async function retrieveSymbols(message, opts = {}) {
  const { topK = 4, tarotMode = false, excludeSources = [] } = opts;
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
      match_count: 40,
    });
  } catch (err) {
    console.warn('[aura/symbolic] rpc failed, skipping retrieval:', err && err.message);
    return [];
  }
  if (!Array.isArray(rows) || !rows.length) return [];

  // ── TAROT MODE ───────────────────────────────────────────────
  // When user explicitly asked for tarot, only pull from the tarot
  // corpus and return 3 distinct cards (for Past / Present / Future).
  // Forced source-diversity becomes irrelevant; the entire reading is
  // one tradition, which is the actual user expectation.
  if (tarotMode) {
    const tarotCards = rows
      .filter(r => r.source === 'tarot_major_arcana_synthesized')
      .slice(0, Math.max(3, topK));
    if (tarotCards.length >= 1) return tarotCards.slice(0, 3);
    // No tarot cards available, fall through to normal flow as graceful
    // degradation (better to return SOMETHING than nothing).
  }

  // Per-source weight. Synthesized cards translate gracefully into
  // replies; Lilly's Christian Astrology has 17th-century mechanical
  // imagery that paraphrases badly. Tarot is bumped a touch for
  // accessibility.
  const SOURCE_WEIGHTS = {
    jungian_archetypes_synthesized: 1.10,
    lal_kitab_synthesized:          1.05,  // was 1.10, lowered: it
                                            //   over-pulls on any "money"
                                            //   query into family-karma
                                            //   framing
    prasna_marga_synthesized:       1.05,
    tarot_major_arcana_synthesized: 1.05,
    cheiro_book_of_numbers:         0.90,
    christian_astrology:            0.65,
  };

  // Skip excluded sources entirely.
  const excludeSet = new Set(excludeSources);
  const filtered = rows.filter(r => !excludeSet.has(r.source));

  const intentTags = inferIntentTags(text);
  const scored = filtered.map(r => {
    const overlap = Array.isArray(r.intent_tags)
      ? r.intent_tags.filter(t => intentTags.includes(t)).length
      : 0;
    const weight = SOURCE_WEIGHTS[r.source] || 1.0;
    return Object.assign({}, r, {
      score: ((r.similarity || 0) + 0.05 * overlap) * weight,
    });
  });
  scored.sort((a, b) => b.score - a.score);

  // Take top-K with source diversity: max 1 from any single source.
  // Forces tradition diversity across every reply.
  const out = [];
  const perSource = {};
  for (const r of scored) {
    const src = r.source || 'unknown';
    if ((perSource[src] || 0) >= 1) continue;
    out.push(r);
    perSource[src] = (perSource[src] || 0) + 1;
    if (out.length >= topK) break;
  }
  return out;
}

export { retrieveSymbols, inferIntentTags, isTarotRequest };
