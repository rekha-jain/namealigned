/**
 * Aura V2 Phase C ingestion pipeline.
 *
 * Reads ingestion/corpus/<source>.txt files, chunks them, asks Gemini
 * to extract symbol cards in the AURA_SYMBOL_SCHEMA shape, runs each
 * card through the deterministic grader, embeds the passing ones with
 * text-embedding-004, and writes them to Supabase.
 *
 * Run locally:
 *   GEMINI_API_KEY=...  \
 *   SUPABASE_URL=...    \
 *   SUPABASE_SERVICE_KEY=... \
 *   node ingestion/ingest.js --source cheiro_book_of_numbers
 *
 * Or via npm script:
 *   npm run aura:ingest -- --source cheiro_book_of_numbers
 *
 * Idempotent-ish: rerunning the same source will re-extract and append.
 * Use --reset to delete all existing rows for that source before inserting.
 */

'use strict';

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

import { chunkText }      from './chunk.js';
import { extractCards }   from './extract.js';
import { gradeCard }      from './grader.js';
import { embedTexts }     from './embed.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const SUPABASE_URL = (process.env.SUPABASE_URL || '').replace(/\/+$/, '');
const SUPABASE_KEY = process.env.SUPABASE_SERVICE_KEY || '';
const GEMINI_KEY   = process.env.GEMINI_API_KEY || '';

// ---------- args ----------
function parseArgs(argv) {
  const out = { source: '', reset: false, dryRun: false, maxChunks: 0 };
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--source')       out.source    = argv[++i];
    else if (a === '--reset')   out.reset     = true;
    else if (a === '--dry-run') out.dryRun    = true;
    else if (a === '--max')     out.maxChunks = Number(argv[++i] || 0);
  }
  return out;
}

// ---------- supabase helpers ----------
function supabaseHeaders() {
  return {
    apikey: SUPABASE_KEY,
    Authorization: 'Bearer ' + SUPABASE_KEY,
    'Content-Type': 'application/json',
  };
}
async function supabaseInsert(table, rows) {
  if (!rows.length) return;
  const r = await fetch(SUPABASE_URL + '/rest/v1/' + table, {
    method: 'POST',
    headers: Object.assign(supabaseHeaders(), { Prefer: 'return=minimal' }),
    body: JSON.stringify(rows),
  });
  if (!r.ok) {
    const t = await r.text().catch(() => '');
    throw new Error('insert ' + table + ' ' + r.status + ' ' + t.slice(0, 300));
  }
}
async function supabaseDeleteBySource(table, source) {
  const r = await fetch(SUPABASE_URL + '/rest/v1/' + table + '?source=eq.' + encodeURIComponent(source), {
    method: 'DELETE',
    headers: supabaseHeaders(),
  });
  if (!r.ok && r.status !== 404) {
    const t = await r.text().catch(() => '');
    throw new Error('delete ' + table + ' ' + r.status + ' ' + t.slice(0, 300));
  }
}

// ---------- rate-limit helpers ----------
const sleep = ms => new Promise(r => setTimeout(r, ms));

async function withRetry(fn, label) {
  let lastErr;
  for (let attempt = 1; attempt <= 4; attempt++) {
    try { return await fn(); }
    catch (err) {
      lastErr = err;
      const msg = err && err.message || '';
      // 429 / 503 / 500 -> back off.
      if (/_(429|500|503)/.test(msg) || /quota/i.test(msg)) {
        const wait = 4000 * attempt;
        console.warn('[' + label + '] retry ' + attempt + ' after ' + wait + 'ms (' + msg + ')');
        await sleep(wait);
        continue;
      }
      throw err;
    }
  }
  throw lastErr;
}

// ---------- main ----------
async function main() {
  const args = parseArgs(process.argv);
  if (!args.source) { console.error('Usage: node ingestion/ingest.js --source <key> [--reset] [--dry-run] [--max N]'); process.exit(1); }
  if (!GEMINI_KEY)  { console.error('GEMINI_API_KEY missing');         process.exit(1); }
  if (!args.dryRun && (!SUPABASE_URL || !SUPABASE_KEY)) { console.error('SUPABASE_URL / SUPABASE_SERVICE_KEY missing'); process.exit(1); }

  const file = path.join(__dirname, 'corpus', args.source + '.txt');
  if (!fs.existsSync(file)) {
    console.error('Source file not found: ' + file);
    console.error('Drop the cleaned plain-text version at that path and re-run.');
    process.exit(1);
  }
  const raw = fs.readFileSync(file, 'utf8');
  const chunks = chunkText(raw);
  const work = args.maxChunks > 0 ? chunks.slice(0, args.maxChunks) : chunks;
  console.log('[ingest] source=' + args.source + ' total_chunks=' + chunks.length + ' processing=' + work.length);

  if (args.reset && !args.dryRun) {
    console.log('[ingest] resetting existing rows for source=' + args.source);
    await supabaseDeleteBySource('aura_symbols',          args.source);
    await supabaseDeleteBySource('aura_symbols_rejected', args.source);
  }

  let totals = { extracted: 0, passed: 0, rejected: 0, embedded: 0, inserted: 0 };

  for (let i = 0; i < work.length; i++) {
    const c = work[i];
    console.log('\n[chunk ' + (i + 1) + '/' + work.length + '] section="' + (c.sectionHint || '').slice(0, 60) + '"');
    let cards = [];
    try {
      cards = await withRetry(() => extractCards({
        chunk: c.text, source: args.source, sourceRef: c.sectionHint || '', sectionHint: c.sectionHint || '',
        apiKey: GEMINI_KEY,
      }), 'extract');
    } catch (err) {
      console.warn('  extract failed, skipping chunk:', err && err.message);
      continue;
    }
    totals.extracted += cards.length;
    if (!cards.length) { console.log('  no cards'); continue; }

    const passing = [];
    const rejecting = [];
    for (const card of cards) {
      const grade = gradeCard(card);
      if (grade.passed) passing.push(card);
      else rejecting.push({ card, grade });
    }
    totals.passed   += passing.length;
    totals.rejected += rejecting.length;
    console.log('  extracted=' + cards.length + ' passed=' + passing.length + ' rejected=' + rejecting.length);

    if (rejecting.length && !args.dryRun) {
      const rows = rejecting.map(({ card, grade }) => ({
        source: args.source,
        source_ref: card.source_ref,
        body: card.body,
        card,
        scores: grade.scores,
        reasons: grade.reasons,
      }));
      try { await supabaseInsert('aura_symbols_rejected', rows); }
      catch (err) { console.warn('  rejected-insert failed:', err && err.message); }
    }

    if (!passing.length) continue;

    let embeddings = [];
    try {
      embeddings = await withRetry(
        () => embedTexts(passing.map(p => p.name + '. ' + p.body), GEMINI_KEY),
        'embed',
      );
      totals.embedded += embeddings.length;
    } catch (err) {
      console.warn('  embed failed, skipping chunk insert:', err && err.message);
      continue;
    }

    const rows = passing.map((p, idx) => ({
      name: p.name,
      category: p.category,
      archetype: p.archetype,
      planet: p.planet,
      house: p.house,
      intent_tags: p.intent_tags,
      emotional_tags: p.emotional_tags,
      body: p.body,
      source: args.source,
      source_ref: p.source_ref,
      embedding: embeddings[idx] && embeddings[idx].length === 768 ? embeddings[idx] : null,
    })).filter(r => r.embedding);

    if (!rows.length) { console.warn('  no rows with valid embeddings'); continue; }

    if (args.dryRun) {
      console.log('  [dry-run] would insert ' + rows.length + ' cards');
      console.log('    sample:', rows[0].name, '|', rows[0].body.slice(0, 80) + '...');
    } else {
      try {
        await supabaseInsert('aura_symbols', rows);
        totals.inserted += rows.length;
        console.log('  inserted ' + rows.length);
      } catch (err) {
        console.warn('  insert failed:', err && err.message);
      }
    }

    // Gentle pacing to stay well under per-minute limits.
    await sleep(800);
  }

  console.log('\n[ingest] done. totals=' + JSON.stringify(totals));
}

main().catch(err => { console.error('[ingest] fatal:', err); process.exit(1); });
