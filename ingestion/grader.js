/**
 * Quality grader for extracted symbol cards.
 *
 * Five binary axes:
 *   1. no_absolute_claims       no "will", "definitely", "guaranteed", "must"
 *   2. no_prescriptions         no gemstone/ritual/purchase advice, no medical/legal/financial certainty
 *   3. specific_citation        source_ref is not "n/a" / empty / generic
 *   4. correct_length           body is 30-100 words, plain English
 *   5. no_markdown              no asterisks, em-dashes, en-dashes, headers, bullets
 *
 * A card passes if it fails at most 1 axis. Failures of axis 1 or 2
 * (the safety axes) always reject regardless of others.
 *
 * Pure heuristics: no LLM call. The grader is the cheap, deterministic
 * filter after Gemini extraction.
 */

'use strict';

const ABSOLUTE_PATTERNS = [
  /\bwill\s+(?:happen|come|find|get|be|bring|gain|lose|fail|succeed)/i,
  /\bdefinitely\b/i,
  /\bguaranteed\b/i,
  /\bcertainly\b/i,
  /\bmust\b/i,
  /\bshall\b/i,
  /\balways\b/i,
  /\bnever\b/i,
];

const PRESCRIPTION_PATTERNS = [
  /\b(gemstone|gem|ruby|emerald|sapphire|pearl|coral|diamond|topaz|yellow sapphire|blue sapphire)\b/i,
  /\b(wear|don)\s+(a|the|this)?\s*(ring|stone|amulet|talisman|yantra)/i,
  /\b(perform|conduct|recite|chant)\s+(a|the)?\s*(puja|yagna|homa|ritual|mantra)/i,
  /\b\d+\s*times\b/i,
  /\b(cure|heal|treat)\s+(your|the)\s+(disease|illness|cancer|diabetes)/i,
  /\b(invest|buy|sell)\s+(in|the)\s+(stock|crypto|bitcoin|property)/i,
];

const MARKDOWN_PATTERNS = [
  /\*\*[^*]+\*\*/,
  /(^|\s)\*[^*\s][^*]*\*(\s|$)/,
  /^#{1,6}\s/m,
  /^\s*[-*•]\s/m,
  /—|–/,        // em-dash, en-dash
];

function countWords(s) {
  return String(s || '').trim().split(/\s+/).filter(Boolean).length;
}

function graderUnspecificRef(ref) {
  const r = String(ref || '').trim().toLowerCase();
  if (!r || r === 'n/a' || r === 'unknown' || r === 'unspecified') return true;
  if (r.length < 4) return true;
  return false;
}

function gradeCard(card) {
  const body = String(card.body || '');
  const reasons = [];
  const scores = {
    no_absolute_claims: true,
    no_prescriptions:   true,
    specific_citation:  true,
    correct_length:     true,
    no_markdown:        true,
  };

  for (const re of ABSOLUTE_PATTERNS) {
    if (re.test(body)) { scores.no_absolute_claims = false; reasons.push('absolute_claim'); break; }
  }
  for (const re of PRESCRIPTION_PATTERNS) {
    if (re.test(body)) { scores.no_prescriptions = false; reasons.push('prescription_or_certainty'); break; }
  }
  if (graderUnspecificRef(card.source_ref)) {
    scores.specific_citation = false;
    reasons.push('weak_citation');
  }
  const wc = countWords(body);
  if (wc < 30 || wc > 100) {
    scores.correct_length = false;
    reasons.push('length_' + wc);
  }
  for (const re of MARKDOWN_PATTERNS) {
    if (re.test(body)) { scores.no_markdown = false; reasons.push('markdown_or_dashes'); break; }
  }

  // Safety axes are blocking. Other axes allow 1 failure.
  const safetyFail = !scores.no_absolute_claims || !scores.no_prescriptions;
  const otherFails = [scores.specific_citation, scores.correct_length, scores.no_markdown]
    .filter(v => v === false).length;

  const passed = !safetyFail && otherFails <= 1;
  return { passed, scores, reasons };
}

export { gradeCard };
