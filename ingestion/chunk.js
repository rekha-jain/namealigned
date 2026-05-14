/**
 * Semantic-ish text chunker for source corpora.
 *
 * Strategy: split on blank lines (paragraphs), then pack paragraphs
 * into chunks up to ~2,800 chars (~800 tokens) without breaking mid
 * paragraph. Headings (lines under 60 chars ending with no period)
 * are kept with the following paragraph so context survives.
 *
 * Returns an array of { text, sectionHint } objects.
 */

'use strict';

const MAX_CHARS = 2800;

function isHeading(line) {
  const t = String(line || '').trim();
  if (!t) return false;
  if (t.length > 70) return false;
  if (/[.!?]$/.test(t)) return false;
  // Common heading shapes: ALL CAPS, "Chapter N", "Number 1", etc.
  if (/^[A-Z][A-Z\s\d.,'\-]{2,}$/.test(t)) return true;
  if (/^(chapter|section|part|book|number)\b/i.test(t)) return true;
  return false;
}

function chunkText(rawText) {
  const text = String(rawText || '').replace(/\r\n/g, '\n').trim();
  if (!text) return [];

  // Split into paragraphs on blank lines.
  const paragraphs = text.split(/\n{2,}/).map(p => p.trim()).filter(Boolean);

  const chunks = [];
  let buf = [];
  let bufLen = 0;
  let currentHeading = '';

  function flush() {
    if (!buf.length) return;
    const body = buf.join('\n\n').trim();
    if (body) chunks.push({ text: body, sectionHint: currentHeading });
    buf = [];
    bufLen = 0;
  }

  for (const para of paragraphs) {
    if (isHeading(para)) {
      // Heading attaches to the next paragraph.
      currentHeading = para;
      continue;
    }
    const projected = bufLen + para.length + 2;
    if (projected > MAX_CHARS && buf.length) {
      flush();
    }
    buf.push(para);
    bufLen += para.length + 2;
  }
  flush();

  return chunks;
}

export { chunkText };
