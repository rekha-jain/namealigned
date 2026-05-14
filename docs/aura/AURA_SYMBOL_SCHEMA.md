# Aura Symbol Schema (Ingestion Contract)

The shape every "symbol card" written into `aura_symbols` must follow. This
is the contract for the Gemini ingestion pipeline that turns source texts
(Cheiro, Prashna Marga, Lal Kitab, etc.) into retrievable interpretation
units.

## 1. The unit

One row = one symbolic interpretation that can stand alone in a reply
context. Not a paragraph from a book, not a chapter, not a planet. One
self-contained idea like "Saturn in the 10th house" or "Birth number 8
under Saturn's mature phase."

## 2. JSON shape

```json
{
  "name": "Saturn in 10th house",
  "category": "planet_in_house",
  "archetype": "authority_through_endurance",
  "planet": "saturn",
  "house": 10,
  "intent_tags": ["career", "recognition", "restructuring", "delay"],
  "emotional_tags": ["perseverance", "isolation", "discipline"],
  "body": "Saturn in the tenth house tends to delay recognition while quietly building the foundation that makes it durable. The seeker often feels behind in their twenties and emerges into authority through their thirties, with the structure they built holding longer than peers who arrived faster.",
  "source": "cheiro_book_of_numbers",
  "source_ref": "ch.7 p.114"
}
```

## 3. Fields

| Field | Type | Required | Notes |
|---|---|---|---|
| name | string | yes | Short, descriptive. "Saturn in 10th house", not "Saturn." |
| category | enum | yes | `planet_in_house` \| `planetary_aspect` \| `archetype` \| `birth_number` \| `name_number` \| `moon_phase` \| `remedy` \| `general` |
| archetype | string | optional | Snake_case archetype label, used for clustering |
| planet | enum | optional | `sun` \| `moon` \| `mars` \| `mercury` \| `jupiter` \| `venus` \| `saturn` \| `rahu` \| `ketu` |
| house | int | optional | 1 to 12 |
| intent_tags | string[] | yes | Min 1, max 6. Lowercase snake_case. Drawn from the intent vocab below. |
| emotional_tags | string[] | yes | Min 1, max 6. Lowercase snake_case. |
| body | string | yes | 40 to 80 words. Plain English. NO markdown. NO unicode dashes. Reads like a sentence in a real conversation. |
| source | string | yes | Lowercase snake_case identifier of the source corpus. See source registry below. |
| source_ref | string | yes | Citation reference. "ch.7 p.114" or "v.2 ch.3 verse 41". Specific enough that a human can verify. |

## 4. Intent vocab (closed set)

Use only these. Add new ones with a PR.

- career
- relationships
- love
- marriage
- family
- health
- money
- relocation
- abroad
- identity
- purpose
- spiritual
- creativity
- communication
- recognition
- restructuring
- delay
- change
- timing
- conflict
- healing

## 5. Emotional vocab (closed set)

- anxious
- hopeful
- stuck
- restless
- grieving
- ambivalent
- excited
- afraid
- peaceful
- confused
- determined
- isolated
- supported
- exhausted
- curious
- perseverance
- isolation
- discipline
- tenderness
- guarded

## 6. Source registry

| Source key | Full name | License notes |
|---|---|---|
| cheiro_book_of_numbers | Cheiro, Book of Numbers | Public domain |
| cheiro_language_of_hand | Cheiro, Language of the Hand | Public domain |
| prasna_marga | Prasna Marga (translated) | Translation source must be cited |
| prashna_tantra | Prashna Tantra (translated) | Translation source must be cited |
| lal_kitab | Lal Kitab (translated) | Translation source must be cited |
| christian_astrology | William Lilly, Christian Astrology | Public domain |
| hermetic_symbolism | General Hermetic tradition | Public domain |
| internal_authored | Authored by the Aura team | New material |

## 7. Body rules

The `body` field is what the LLM weaves into a response. Write it like the
reply itself: warm, plain, grounded.

DO:
- Write in third person ("the seeker", "the native"), not "you".
- Stay in patterns and tendencies, never "will" or "definitely".
- Keep it 40 to 80 words.
- Use plain English.

DO NOT:
- Use markdown of any kind.
- Use em-dash or en-dash. Comma + space, or regular hyphen.
- Quote source text verbatim. Paraphrase.
- Make absolute claims.
- Include remedies that involve buying objects, gemstones, or rituals
  that could be construed as fortune-telling fraud.

## 8. Example: bad to good

BAD (verbatim from source, theatrical):
> "O seeker! When Lord Shani sits in the tenth bhava, success shall be
> denied until the thirty-sixth year, and then bestowed in full measure!"

GOOD (paraphrased, grounded):
> "Saturn in the tenth house tends to delay recognition while quietly
> building the foundation that makes it durable. The seeker often feels
> behind in their twenties and emerges into authority through their
> thirties, with the structure they built holding longer than peers who
> arrived faster."

## 9. Quality bar

Before a symbol row goes live, a human editor reviews:
1. Body reads naturally.
2. Tags match the intent and emotional vocab.
3. Source ref is verifiable.
4. No absolute claims.
5. No prohibited language (medical, legal, financial certainty).

## 10. Changelog

- v1.0 (today): Initial schema.
