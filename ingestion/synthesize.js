/**
 * Aura V2 Phase C: synthesised symbol cards for traditions where the
 * primary English translations are still under copyright (Prashna Marga,
 * Lal Kitab, Jungian depth psychology).
 *
 * Strategy: instead of ingesting copyrighted translations verbatim, we
 * ask Gemini to author original symbol cards that draw on the tradition's
 * FRAMEWORK (concepts, system, structural ideas) without quoting any
 * specific translator. This is legally clean (frameworks are not
 * copyrightable; expression is) and lets us cover traditions our
 * audience cares about.
 *
 * Provenance is explicit: every card is stored with
 *   source = '<tradition>_synthesized'
 *   source_ref = 'tradition framework, no direct quote'
 * so any audit shows these are synthesised, not lifted.
 *
 * Same grader applies. Same embed. Same insert.
 *
 * Run:
 *   set -a; source .env.local; set +a
 *   node ingestion/synthesize.js --tradition jungian_archetypes --count 30
 *   node ingestion/synthesize.js --tradition prasna_marga --count 30
 *   node ingestion/synthesize.js --tradition lal_kitab --count 30
 */

'use strict';

import { gradeCard }    from './grader.js';
import { embedTexts }   from './embed.js';

const SUPABASE_URL = (process.env.SUPABASE_URL || '').replace(/\/+$/, '');
const SUPABASE_KEY = process.env.SUPABASE_SERVICE_KEY || '';
const GEMINI_KEY   = process.env.GEMINI_API_KEY || '';

const INTENT_TAGS = [
  'career','relationships','love','marriage','family','health','money',
  'relocation','abroad','identity','purpose','spiritual','creativity',
  'communication','recognition','restructuring','delay','change','timing',
  'conflict','healing',
];
const EMOTIONAL_TAGS = [
  'anxious','hopeful','stuck','restless','grieving','ambivalent','excited',
  'afraid','peaceful','confused','determined','isolated','supported',
  'exhausted','curious','perseverance','isolation','discipline','tenderness','guarded',
];
const CATEGORIES = ['planet_in_house','planetary_aspect','archetype','birth_number','name_number','moon_phase','remedy','general'];

const SCHEMA = {
  type: 'object',
  properties: {
    cards: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          name:           { type: 'string' },
          category:       { type: 'string', enum: CATEGORIES },
          archetype:      { type: 'string' },
          planet:         { type: 'string' },
          house:          { type: 'integer' },
          intent_tags:    { type: 'array', items: { type: 'string' } },
          emotional_tags: { type: 'array', items: { type: 'string' } },
          body:           { type: 'string' },
        },
        required: ['name','category','intent_tags','emotional_tags','body'],
      },
    },
  },
  required: ['cards'],
};

/**
 * Tradition-specific prompts. Each describes the framework Gemini should
 * draw on (which is not copyrightable) and explicitly forbids quoting
 * any specific translation.
 */
const TRADITIONS = {
  jungian_archetypes: {
    label: 'Jungian depth psychology',
    framework: [
      'Carl Jung\'s archetypal psychology. Core archetypes: the Self,',
      'the Shadow, the Anima, the Animus, the Persona, the Wise Old Man/Woman,',
      'the Hero, the Wounded Healer, the Trickster, the Mother, the Father,',
      'the Maiden, the Senex, the Puer Aeternus. Concepts: individuation,',
      'the collective unconscious, synchronicity, projection, complexes,',
      'the shadow as disowned material, integration of opposites.',
      'NEVER quote Jung directly. NEVER reproduce specific case examples',
      'from Man and His Symbols, Memories Dreams Reflections, or any other Jung text.',
      'Speak in original language about the archetypal pattern itself.',
    ].join(' '),
    topic_seeds: [
      'the shadow showing up in mid-career', 'the wounded healer pattern in caregivers',
      'puer aeternus reluctance to commit', 'the senex archetype in late-life rigidity',
      'anima projection in early romantic relationships', 'animus projection in driven women',
      'the hero archetype and burnout', 'the trickster as creative disruptor',
      'mother complex in adult relationships', 'father complex and authority',
      'individuation through midlife crisis', 'synchronicity as inner-outer resonance',
      'the persona becoming a prison', 'integration of disowned anger',
      'the maiden archetype and self-discovery', 'the wise old woman in mentorship',
      'collective unconscious patterns in dreams', 'the wounded healer attracting clients',
      'shadow integration through art', 'the hero refusing the call',
    ],
  },
  prasna_marga: {
    label: 'Prashna Marga (Indic horary tradition)',
    framework: [
      'Indic horary astrology (prashna). Core concepts:',
      'the question chart cast at the moment a question is asked,',
      'the lagna (ascendant of the moment), significators,',
      'planetary lords of the houses, aspects between significators,',
      'the moon as primary indicator of the seeker\'s state,',
      'timing through nakshatras, dasha periods, planetary speed.',
      'House meanings: 1st self, 2nd wealth/family, 3rd siblings/effort,',
      '4th home/mother, 5th creativity/children, 6th obstacles/work, 7th partnership,',
      '8th transformation, 9th dharma/long journeys, 10th career, 11th gains, 12th loss.',
      'NEVER quote Suryanarain Rau, B.V. Raman, or any specific English translator.',
      'NEVER quote specific Sanskrit verses verbatim. Speak in original language about',
      'the SYSTEM (which is not copyrightable) of horary judgment.',
    ].join(' '),
    topic_seeds: [
      'a question about a job offer with weak 10th lord', 'travel question with strong 9th house',
      'marriage prashna timing through 7th lord', 'health question with 6th house affliction',
      'inheritance question with 8th house signals', 'partnership question moon-mercury linkage',
      'foreign settlement question rahu in 12th', 'business question 2nd-11th house linkage',
      'real estate question 4th lord strength', 'lost object question 4th house',
      'pregnancy timing through 5th house', 'litigation question 6th-7th tension',
      'spiritual practice question 9th-12th flow', 'reconciliation question moon waxing',
      'study abroad question 9th-rahu',
    ],
  },
  lal_kitab: {
    label: 'Lal Kitab interpretation',
    framework: [
      'Lal Kitab tradition. Core concepts:',
      'planets as karmic actors, "rishtas" or interpersonal planetary relationships,',
      'the chart read as a karmic story with cause-and-effect through generations,',
      'the importance of the mother (Moon) and father (Sun) houses,',
      'past-life patterns repeating in current life, often through family,',
      'the slow karmic seeding of present circumstances.',
      'NEVER quote any specific English translator of Lal Kitab.',
      'NEVER prescribe gemstones, rituals, or remedies that involve buying things.',
      'Speak in original language about the karmic-pattern framework itself.',
    ].join(' '),
    topic_seeds: [
      'father-line karma replaying in current career', 'mother-line wealth patterns',
      'sibling karma and resource sharing', 'past-life debt to a parent showing up as caregiving',
      'inherited family pattern of late marriage', 'karmic stuck-loop in relationships',
      'ancestral pattern of self-sacrifice', 'business cycle echoing father\'s history',
      'health pattern carrying from grandparent', 'foreign-settlement pull as karmic resolution',
      'creative-block pattern from suppressed lineage gift', 'wealth pattern delayed by elder-care',
      'partnership-choice mirroring parent\'s marriage', 'rebirth-pattern of unfinished work',
      'forgiveness-cycle with estranged sibling',
    ],
  },
};

const sleep = ms => new Promise(r => setTimeout(r, ms));

function parseArgs(argv) {
  const o = { tradition: '', count: 30, dryRun: false };
  for (let i = 2; i < argv.length; i++) {
    if (argv[i] === '--tradition')  o.tradition = argv[++i];
    else if (argv[i] === '--count') o.count = Number(argv[++i] || 30);
    else if (argv[i] === '--dry-run') o.dryRun = true;
  }
  return o;
}

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

const CASCADE = ['gemini-2.5-flash-lite', 'gemini-2.5-flash', 'gemini-flash-latest'];

async function callModel(model, prompt) {
  const url = 'https://generativelanguage.googleapis.com/v1beta/models/'
    + model + ':generateContent?key=' + encodeURIComponent(GEMINI_KEY);
  const body = {
    contents: [{ role: 'user', parts: [{ text: prompt }] }],
    generationConfig: {
      temperature: 0.65,
      maxOutputTokens: 1800,
      responseMimeType: 'application/json',
      responseSchema: SCHEMA,
      thinkingConfig: { thinkingBudget: 0 },
    },
  };
  const r = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  if (!r.ok) {
    const t = await r.text().catch(() => '');
    throw Object.assign(new Error('synth_failed_' + r.status), { body: t.slice(0, 300), status: r.status });
  }
  const data = await r.json();
  const parts = (((data.candidates || [])[0] || {}).content || {}).parts || [];
  return parts.map(p => p.text || '').join('');
}

async function synthesize(tradition, topic) {
  const t = TRADITIONS[tradition];
  if (!t) throw new Error('Unknown tradition: ' + tradition);

  const prompt = [
    'You are authoring ORIGINAL symbol cards for an emotionally intelligent conversational',
    'companion called Aura. Each card is a self-contained interpretation rooted in the',
    t.label + ' framework.',
    '',
    'TRADITION FRAMEWORK:',
    t.framework,
    '',
    'CARD FORMAT (strict):',
    '- 1 to 3 cards per request',
    '- name: short, descriptive (max 60 chars)',
    '- category: one of ' + CATEGORIES.join(', '),
    '- archetype: a snake_case label (optional)',
    '- intent_tags: 1 to 6, from this closed list: ' + INTENT_TAGS.join(', '),
    '- emotional_tags: 1 to 6, from this closed list: ' + EMOTIONAL_TAGS.join(', '),
    '- body: 40 to 80 words, third-person ("the seeker"), patterns not absolutes,',
    '  NO markdown, NO em-dashes / en-dashes (use comma plus space), NO "will" / "must" /',
    '  "definitely". NEVER quote any source text directly. Speak in original language.',
    '',
    'TOPIC SEED for this request: ' + topic,
    '',
    'Return ONLY JSON: { "cards": [ ... ] }. No prose.',
  ].join('\n');

  let raw = '';
  let lastErr;
  for (const model of CASCADE) {
    try {
      raw = await callModel(model, prompt);
      if (raw) break;
    } catch (err) {
      lastErr = err;
      if (err.status === 401 || err.status === 403 || err.status === 404) throw err;
      continue;
    }
  }
  if (!raw) throw lastErr || new Error('synth_all_failed');

  let parsed;
  try { parsed = JSON.parse(raw); } catch { return []; }
  const cards = Array.isArray(parsed && parsed.cards) ? parsed.cards : [];

  return cards.map(c => ({
    name: String(c.name || '').slice(0, 200),
    category: c.category || 'archetype',
    archetype: c.archetype || null,
    planet: (c.planet || '').toLowerCase() || null,
    house: Number.isInteger(c.house) ? c.house : null,
    intent_tags: Array.isArray(c.intent_tags) ? c.intent_tags.filter(t => INTENT_TAGS.includes(t)) : [],
    emotional_tags: Array.isArray(c.emotional_tags) ? c.emotional_tags.filter(t => EMOTIONAL_TAGS.includes(t)) : [],
    body: String(c.body || '').trim(),
    source: tradition + '_synthesized',
    source_ref: 'tradition framework, no direct quote',
  })).filter(c => c.name && c.body);
}

async function main() {
  const args = parseArgs(process.argv);
  if (!args.tradition) { console.error('Usage: node ingestion/synthesize.js --tradition <key> [--count N] [--dry-run]'); process.exit(1); }
  if (!TRADITIONS[args.tradition]) {
    console.error('Unknown tradition. Available: ' + Object.keys(TRADITIONS).join(', '));
    process.exit(1);
  }
  if (!GEMINI_KEY) { console.error('GEMINI_API_KEY missing'); process.exit(1); }
  if (!args.dryRun && (!SUPABASE_URL || !SUPABASE_KEY)) { console.error('Supabase env missing'); process.exit(1); }

  const t = TRADITIONS[args.tradition];
  const totals = { extracted: 0, passed: 0, rejected: 0, inserted: 0 };

  // Pick topic seeds, cycling through if count > seeds.
  const seeds = t.topic_seeds;
  const requests = [];
  for (let i = 0; i < args.count; i++) requests.push(seeds[i % seeds.length]);

  console.log(`[synth] tradition=${args.tradition} requests=${requests.length}`);

  for (let i = 0; i < requests.length; i++) {
    const topic = requests[i];
    console.log(`\n[req ${i+1}/${requests.length}] topic="${topic}"`);

    let cards;
    try {
      cards = await synthesize(args.tradition, topic);
    } catch (err) {
      console.warn('  synth failed:', err && err.message);
      await sleep(8000);
      continue;
    }
    totals.extracted += cards.length;
    if (!cards.length) { console.log('  no cards'); continue; }

    const passing = [];
    const rejecting = [];
    for (const card of cards) {
      const g = gradeCard(card);
      if (g.passed) passing.push(card);
      else rejecting.push({ card, grade: g });
    }
    totals.passed   += passing.length;
    totals.rejected += rejecting.length;
    console.log(`  extracted=${cards.length} passed=${passing.length} rejected=${rejecting.length}`);

    if (rejecting.length && !args.dryRun) {
      try {
        await supabaseInsert('aura_symbols_rejected', rejecting.map(({ card, grade }) => ({
          source: card.source, source_ref: card.source_ref, body: card.body,
          card, scores: grade.scores, reasons: grade.reasons,
        })));
      } catch (err) { console.warn('  rejected-insert failed:', err && err.message); }
    }

    if (!passing.length) { await sleep(4500); continue; }

    let embeddings;
    try {
      embeddings = await embedTexts(passing.map(p => p.name + '. ' + p.body), GEMINI_KEY);
    } catch (err) {
      console.warn('  embed failed:', err && err.message);
      await sleep(4500);
      continue;
    }

    const rows = passing.map((p, idx) => ({
      ...p,
      embedding: embeddings[idx] && embeddings[idx].length === 768 ? embeddings[idx] : null,
    })).filter(r => r.embedding);

    if (args.dryRun) {
      console.log(`  [dry-run] would insert ${rows.length}`);
      rows.slice(0, 2).forEach(r => console.log(`    + ${r.name}: ${r.body.slice(0, 100)}...`));
    } else {
      try {
        await supabaseInsert('aura_symbols', rows);
        totals.inserted += rows.length;
        console.log(`  inserted ${rows.length}`);
      } catch (err) { console.warn('  insert failed:', err && err.message); }
    }

    // Pacing for rate limits.
    await sleep(4500);
  }

  console.log(`\n[synth] done. totals=${JSON.stringify(totals)}`);
}

main().catch(err => { console.error('[synth] fatal:', err); process.exit(1); });
