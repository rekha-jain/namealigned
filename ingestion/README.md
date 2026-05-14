# Aura V2 Symbol Corpus Ingestion

This pipeline turns classical source texts (Cheiro, Lal Kitab, Prashna
Marga, etc.) into the `aura_symbols` retrieval corpus that grounds
Aura's replies.

Runs **locally on your machine**, not deployed. Free Gemini quota only,
zero ongoing cost.

## Quick start

### 1. Prereqs

- Node 20+
- An `.env.local` file at the repo root with:
  ```
  GEMINI_API_KEY=...
  SUPABASE_URL=https://<project>.supabase.co
  SUPABASE_SERVICE_KEY=...   # service role, NOT anon
  ```
- The Phase A migration applied (`docs/supabase/aura-v2-migration.sql`)
- The Phase C followup migration applied (`docs/supabase/aura-v2-symbols-rejected.sql`)

### 2. Drop a source text into the corpus folder

Plain text. UTF-8. One file per source. Filename = the `source` key
that will be stored on every card.

```
ingestion/corpus/cheiro_book_of_numbers.txt
ingestion/corpus/lal_kitab.txt
ingestion/corpus/prasna_marga.txt
```

#### Where to get Cheiro, Book of Numbers (public domain)

- Project Gutenberg or archive.org. Search "Cheiro Book of Numbers".
- Strip the Gutenberg header/footer.
- Save as plain UTF-8 text. No markdown, no HTML.
- Preserve paragraph breaks (blank line between paragraphs).

### 3. Dry-run first

Always sanity-check on 2-3 chunks before letting it loose on the whole book.

```
set -a; source .env.local; set +a
node ingestion/ingest.js --source cheiro_book_of_numbers --dry-run --max 3
```

This will:
- chunk the file
- extract cards with Gemini
- grade each card
- print what would be inserted (no DB writes)

If the printed cards look sensible (40 to 80 words, grounded language,
specific citations), proceed.

### 4. Full ingest

```
node ingestion/ingest.js --source cheiro_book_of_numbers
```

For a typical 200-page book this runs 30 to 60 minutes (rate-limited
gently). It pauses 800 ms between chunks and backs off on 429/503.

Run progress logs look like:
```
[chunk 12/124] section="THE NUMBER 1"
  extracted=3 passed=2 rejected=1
  inserted 2
```

### 5. Verify in Supabase

```sql
select source, count(*) as cards, avg(length(body)) as avg_body_chars
from aura_symbols
group by source;

select reasons, count(*)
from aura_symbols_rejected
group by reasons
order by count(*) desc;
```

### 6. Re-ingesting

If you want to wipe and redo for one source:

```
node ingestion/ingest.js --source cheiro_book_of_numbers --reset
```

This deletes all rows in `aura_symbols` and `aura_symbols_rejected`
where `source = 'cheiro_book_of_numbers'`, then re-runs.

## What the grader rejects

Five axes, all heuristic, no LLM:

| Axis | Rejects |
|---|---|
| no_absolute_claims | "will happen", "definitely", "must", "always", "never" |
| no_prescriptions | gemstone advice, ritual prescriptions, medical/financial certainty |
| specific_citation | source_ref of "n/a", empty, or under 4 chars |
| correct_length | body under 30 or over 100 words |
| no_markdown | asterisks, em-dashes, en-dashes, headers, bullets |

A card passes if it fails at most 1 of the **non-safety** axes
(citation / length / markdown). Safety axes (absolute claims,
prescriptions) are blocking, any failure rejects.

Rejected cards are logged to `aura_symbols_rejected` with the reason,
so you can periodically review patterns and tune.

## Source registry, multi-tradition

The corpus is deliberately syncretic. Aura is not a numerology-only
companion; the symbol library should span all the traditions named in
the brief: Chaldean numerology, Prashna Marga horary, Prashna Tantra,
Lal Kitab, Western horary (William Lilly), Hermetic symbolism, and
Jungian archetypes.

Recommended ingestion order (start at the top, add as you have time):

| Source key | Tradition | Availability |
|---|---|---|
| `cheiro_book_of_numbers` | Chaldean numerology | Public domain. Project Gutenberg / archive.org. |
| `cheiro_language_of_hand` | Palmistry / numerology adjunct | Public domain. archive.org. |
| `christian_astrology` | Western horary (William Lilly, 1647) | Public domain. archive.org has scans + transcripts. |
| `prasna_marga` | Indic horary (Prashna) | Translations exist; verify license. Try Sastri's English translation (older, often public domain). |
| `prashna_tantra` | Indic horary | Translations exist; verify license. |
| `lal_kitab` | Lal Kitab interpretation | English translations vary in quality and license; choose one carefully. |
| `hermetic_symbolism` | Hermetic / Western esoteric | Compile from public-domain sources (Three Initiates, *Kybalion*, etc.). |
| `jungian_archetypes` | Depth psychology | Authored summary, no direct quoting. Pull from *Man and His Symbols* (still in copyright; paraphrase only). |
| `internal_authored` | New material you write | Author yourself or with a freelance editor. |

The pipeline does not care which tradition a `.txt` file represents.
It chunks, asks Gemini to extract cards in the AURA_SYMBOL_SCHEMA
shape (categories like `planet_in_house`, `birth_number`, `archetype`,
`general` cover every tradition), grades for safety / length / claims,
embeds, inserts. Retrieval at runtime is tradition-agnostic with
diversity capped at 2 cards per source so no single tradition
dominates a reply.

When adding a new tradition, just:
1. Save the text as `ingestion/corpus/<source_key>.txt`
2. `npm run aura:ingest -- --source <source_key> --dry-run --max 3`
3. If sample cards look good, run the full ingest.

The persona prompt (`api/aura/v2/_lib/prompt.js`) already invites
Aura to move between traditions naturally without name-dropping them.

## Cost

Per chunk: 1 extract call + 1 batch embed call. Roughly 100 to 300
chunks per source. Well under the 1,500 calls/day Gemini free tier
even on a full book in one sitting.

Embeddings (`text-embedding-004`) have a separate generous free quota,
no separate billing.

## Failure modes seen in practice

| Symptom | Likely cause | Fix |
|---|---|---|
| Many chunks produce 0 cards | Source has lots of front-matter / TOC / index | Pre-trim the text file, or accept it |
| `extract_failed_429` | Gemini rate-limit | Pipeline already retries with backoff; if persistent, drop concurrency |
| All cards rejected on `weak_citation` | Source has no internal headings | Pre-process to insert chapter markers, or relax grader temporarily |
| `embed_failed_403` | Wrong API key, embedding not enabled on the project | Verify key has access to `text-embedding-004` |
