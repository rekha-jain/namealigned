/**
 * Post-LLM sanitization. Strips markdown, theatrical openers, and the
 * site-wide unicode-dash ban. Also caps to N sentences when used on the
 * final accumulated text. Streaming chunks are passed through verbatim;
 * we only enforce the strict shape on the final assembled reply via
 * `finalize`.
 */

'use strict';

function stripMarkdown(s) {
  let out = String(s || '');
  out = out.replace(/\*\*([^*]+)\*\*/g, '$1');
  out = out.replace(/\*([^*]+)\*/g, '$1');
  out = out.replace(/__([^_]+)__/g, '$1');
  out = out.replace(/_([^_]+)_/g, '$1');
  out = out.replace(/`([^`]+)`/g, '$1');
  out = out.replace(/^\s*#{1,6}\s+/gm, '');
  out = out.replace(/^\s*[-*•]\s+/gm, '');
  out = out.replace(/^\s*\d+\.\s+/gm, '');
  return out;
}

// Site-wide rule: never em-dash or en-dash. Replace with ", " when it
// reads like a clause break, otherwise a hyphen.
function stripUnicodeDashes(s) {
  return String(s || '')
    .replace(/\s*[—–]\s*/g, ', ')  // em-dash, en-dash to ", "
    .replace(/−/g, '-');                // minus to hyphen
}

function stripTheatricalOpeners(s) {
  return String(s || '').replace(/^(Ah|Oh|Beloved|Dear one|My dear|Listen|I sense)[,!.]\s+/i, '');
}

function capSentences(s, max) {
  const out = String(s || '').trim();
  if (!out) return '';
  const sentences = out.match(/[^.!?]+[.!?]+/g);
  if (!sentences || sentences.length <= max) return out;
  return sentences.slice(0, max).join('').trim();
}

/**
 * Run on each streaming chunk. We strip markdown and unicode dashes
 * so they never reach the user's screen, but we don't try to cap
 * sentences mid-stream.
 */
function sanitizeChunk(chunk) {
  return stripUnicodeDashes(stripMarkdown(chunk));
}

/**
 * Run once on the final, complete reply before persisting.
 * Enforces the 2-sentence shape (3 for timing questions).
 */
function finalize(text, { maxSentences = 2 } = {}) {
  let out = String(text || '');
  out = stripMarkdown(out);
  out = stripUnicodeDashes(out);
  out = stripTheatricalOpeners(out);
  out = out.replace(/\s+/g, ' ').trim();
  out = capSentences(out, maxSentences);
  return out;
}

function isTimingQuestion(text) {
  if (!text) return false;
  return /\b(when|how long|how soon|by when|in what time|time frame|timeframe|how many (days|weeks|months|years)|soon|deadline)\b/i.test(text);
}

export { sanitizeChunk, finalize, isTimingQuestion };
