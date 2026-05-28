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
 * Detect when the user explicitly asked for a prashna / horary reading.
 * Matches: prashna kundali, prashna marga, prasna, horary, horary reading,
 * horary chart, kundali reading (for the moment).
 */
function isPrashnaRequest(message) {
  const m = String(message || '').toLowerCase();
  return /\b(pra[s]?h?na(\s+(kundali|marga|tantra|chart|reading))?|horary(\s+(reading|chart))?|kundali\s+(reading|for\s+this))\b/i.test(m);
}

/**
 * Detect any reading-mode request (tarot OR prashna), looking at the
 * current message FIRST and falling back to the most recent prior user
 * message in history. This handles the conversation pattern:
 *   user: "Can you do prashna kundali?"
 *   aura: "What clarity do you need?"
 *   user: "will I get my salary by Friday?"   <-- this is the prashna question
 * Without history-awareness, that last message would classify as practical
 * and skip the reading entirely.
 *
 * Returns one of: 'tarot' | 'prashna' | null.
 */
function detectReadingMode(message, history) {
  if (isTarotRequest(message))   return 'tarot';
  if (isPrashnaRequest(message)) return 'prashna';

  // Look at the most recent prior user message. If it requested a reading
  // mode AND the message in between is short/clarifying (assistant asking
  // "what is your question"), the current message is the reading subject.
  if (!Array.isArray(history) || !history.length) return null;
  const userTurns = history.filter(m => m && m.role === 'user').slice(-2);
  for (const t of userTurns) {
    const txt = String(t.content || '');
    // Skip if the prior user message ALSO had a clear, full question (then
    // the reading-mode request was probably standalone, not paired).
    if (isTarotRequest(txt)   && txt.length < 40) return 'tarot';
    if (isPrashnaRequest(txt) && txt.length < 60) return 'prashna';
  }
  return null;
}

/**
 * Retrieve top-K symbol cards relevant to the user's message.
 * Returns: [ { id, name, body, planet, source, source_ref, intent_tags, similarity } ]
 *
 * Options:
 *   topK            (number, default 4)
 *   tarotMode       (bool, default false)  if true, pulls 3 tarot cards only
 *   prashnaMode     (bool, default false)  if true, pulls 3 horary cards only
 *                                          (prasna_marga_synthesized + christian_astrology)
 *   excludeSources  (array, optional) sources to filter out of results
 *
 * Best-effort: any failure returns [] and logs.
 */
async function retrieveSymbols(message, opts = {}) {
  const { topK = 4, tarotMode = false, prashnaMode = false, excludeSources = [] } = opts;
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

  // ── PRASHNA MODE ─────────────────────────────────────────────
  // When user explicitly asked for prashna kundali / horary reading,
  // pull only from the horary traditions (Prashna Marga + William Lilly).
  // Return 3 cards interpreted as Significator / Cusp / Timing.
  if (prashnaMode) {
    const horarySources = new Set(['prasna_marga_synthesized', 'christian_astrology']);
    const horaryCards = rows
      .filter(r => horarySources.has(r.source))
      .slice(0, Math.max(3, topK));
    if (horaryCards.length >= 1) return horaryCards.slice(0, 3);
    // graceful degradation: fall through if no horary cards available
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

export {
  retrieveSymbols,
  inferIntentTags,
  isTarotRequest,
  isPrashnaRequest,
  detectReadingMode,
};
