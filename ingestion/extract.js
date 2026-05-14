/**
 * Gemini-backed symbol-card extractor.
 *
 * Takes a text chunk + provenance, asks Gemini to emit 0..N symbol
 * cards conforming to AURA_SYMBOL_SCHEMA.md. Uses JSON mode with
 * responseSchema so the model can't drift the shape.
 *
 * Returns an array of card objects (no embeddings yet; that's grader/embed).
 */

'use strict';

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
const CATEGORIES = [
  'planet_in_house','planetary_aspect','archetype','birth_number',
  'name_number','moon_phase','remedy','general',
];

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
          source_ref:     { type: 'string' },
        },
        required: ['name','category','intent_tags','emotional_tags','body','source_ref'],
      },
    },
  },
  required: ['cards'],
};

function buildPrompt({ chunk, source, sourceRef, sectionHint }) {
  return [
    'You are extracting "symbol cards" from a classical numerology / astrology source text.',
    'Each card is ONE self-contained interpretation that can stand alone in a reply.',
    '',
    'STRICT RULES:',
    '- Emit 0 to 4 cards from this chunk. Quality over quantity. If the chunk has nothing card-worthy, emit zero cards.',
    '- name: short descriptive label (e.g. "Saturn in 10th house", "Birth number 8 under Saturn").',
    '- category: one of: ' + CATEGORIES.join(', '),
    '- intent_tags: pick 1 to 6 from this CLOSED list, lowercase: ' + INTENT_TAGS.join(', '),
    '- emotional_tags: pick 1 to 6 from this CLOSED list, lowercase: ' + EMOTIONAL_TAGS.join(', '),
    '- body: 40 to 80 words. Plain English. Third-person ("the seeker", "the native"). NO markdown.',
    '  NO em-dashes or en-dashes (use comma plus space, or hyphen). Speak in patterns, never absolutes.',
    '  Never use "will", "definitely", "guaranteed", "must". Paraphrase, do NOT quote verbatim.',
    '- source_ref: a verifiable citation from the chunk (e.g. "ch.7 p.114" or "section heading"). If unclear, use the section hint or "n/a".',
    '- Do NOT include remedies that prescribe buying gemstones, conducting rituals, or paying for services.',
    '- Do NOT include cards that make health, legal, or financial guarantees.',
    '',
    'SOURCE: ' + (source || 'unknown'),
    'SOURCE_REF_HINT: ' + (sourceRef || 'n/a'),
    'SECTION_HINT: ' + (sectionHint || 'n/a'),
    '',
    'TEXT CHUNK:',
    '"""',
    String(chunk || '').slice(0, 4000),
    '"""',
    '',
    'Return ONLY a JSON object: { "cards": [ ... ] }. No prose.',
  ].join('\n');
}

// Cascade order: lite first because it has the highest RPM/RPD on the free
// tier (1000 RPD, 15 RPM), then 2.5-flash, then flash-latest. Lite quality
// is plenty for symbol-card extraction (it is structured JSON in / out).
const EXTRACT_CASCADE = ['gemini-2.5-flash-lite', 'gemini-2.5-flash', 'gemini-flash-latest'];

async function callExtractModel(model, prompt, apiKey) {
  const url = 'https://generativelanguage.googleapis.com/v1beta/models/'
    + encodeURIComponent(model)
    + ':generateContent?key=' + encodeURIComponent(apiKey);
  const body = {
    contents: [{ role: 'user', parts: [{ text: prompt }] }],
    generationConfig: {
      temperature: 0.2,
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
    throw Object.assign(new Error('extract_failed_' + r.status), { body: t.slice(0, 400), status: r.status, model });
  }
  const data = await r.json();
  const text = (((data.candidates || [])[0] || {}).content || {}).parts || [];
  return text.map(p => p.text || '').join('').trim();
}

async function extractCards({ chunk, source, sourceRef, sectionHint, apiKey }) {
  if (!apiKey) throw new Error('GEMINI_API_KEY not set');
  const prompt = buildPrompt({ chunk, source, sourceRef, sectionHint });

  let raw = '';
  let lastErr;
  for (const model of EXTRACT_CASCADE) {
    try {
      raw = await callExtractModel(model, prompt, apiKey);
      break;
    } catch (err) {
      lastErr = err;
      const status = err && err.status;
      // 429 (rate-limit) or 503 (overloaded) -> cascade to next model.
      // 401/403/404 -> bail, not retryable.
      if (status === 401 || status === 403 || status === 404) throw err;
      continue;
    }
  }
  if (!raw) throw lastErr || new Error('extract_failed_all_models');

  let parsed;
  try { parsed = JSON.parse(raw); } catch { return []; }
  const cards = Array.isArray(parsed && parsed.cards) ? parsed.cards : [];

  // Attach source. source_ref may have been auto-filled by Gemini.
  return cards.map(c => ({
    name: c.name,
    category: c.category,
    archetype: c.archetype || null,
    planet: (c.planet || '').toLowerCase() || null,
    house: Number.isInteger(c.house) ? c.house : null,
    intent_tags: Array.isArray(c.intent_tags) ? c.intent_tags.filter(t => INTENT_TAGS.includes(t)) : [],
    emotional_tags: Array.isArray(c.emotional_tags) ? c.emotional_tags.filter(t => EMOTIONAL_TAGS.includes(t)) : [],
    body: String(c.body || '').trim(),
    source,
    source_ref: String(c.source_ref || sourceRef || sectionHint || 'n/a'),
  })).filter(c => c.name && c.body);
}

export { extractCards, INTENT_TAGS, EMOTIONAL_TAGS, CATEGORIES };
