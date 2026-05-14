/**
 * Pre-filter for messages that should never reach the LLM.
 * Crisis (suicide, self-harm) gets the helpline copy. Medical, legal,
 * and specific financial requests get a warm redirect.
 *
 * Returns null if the message is fine, or an object describing what to
 * return to the user instead of calling the LLM.
 */

'use strict';

const CRISIS_PATTERNS = [
  /\b(kill|end|hurt|harm)\s+(myself|me)\b/i,
  /\b(suicid|self[\s-]?harm)\b/i,
  /\b(want to die|don'?t want to live|no reason to live|life isn'?t worth)\b/i,
  /\b(planning|thinking of|tried) (to )?(end|kill)\b/i,
];

const MEDICAL_PATTERNS = [
  /\b(diagnos|prescription|medication|dose|dosage|treatment for|cure for|cancer|tumou?r|stroke|heart attack|covid|diabetes|pregnan)\b/i,
];

const LEGAL_PATTERNS = [
  /\b(lawyer|sue|lawsuit|court case|criminal|jail|prison|deport|visa application|legal advice|legal action)\b/i,
];

const FINANCIAL_PATTERNS = [
  /\b(should i (buy|sell|invest)|stock pick|crypto|bitcoin price|loan default|bankruptcy advice)\b/i,
];

const CRISIS_REPLY =
  "What you are carrying sounds heavy, and you do not have to carry it alone. " +
  "Please reach out to someone trained to help right now: " +
  "iCall India 9152987821, AASRA 9820466726, or your local emergency number. " +
  "I am here when you come back.";

const MEDICAL_REPLY =
  "This is one I cannot answer well, please speak with a doctor you trust. " +
  "I can sit with the feeling around it if that helps.";

const LEGAL_REPLY =
  "For anything legal, a qualified lawyer is the right voice, not me. " +
  "If there is something underneath the question, an uncertainty, a worry, I can reflect on that.";

const FINANCIAL_REPLY =
  "Specific money calls are not mine to make. " +
  "If the question underneath is about timing, courage, or fear, I can sit with that.";

function preFilterSafety(message) {
  const m = String(message || '');
  if (!m) return null;

  for (const re of CRISIS_PATTERNS) {
    if (re.test(m)) return { kind: 'crisis', reply: CRISIS_REPLY };
  }
  for (const re of MEDICAL_PATTERNS) {
    if (re.test(m)) return { kind: 'medical', reply: MEDICAL_REPLY };
  }
  for (const re of LEGAL_PATTERNS) {
    if (re.test(m)) return { kind: 'legal', reply: LEGAL_REPLY };
  }
  for (const re of FINANCIAL_PATTERNS) {
    if (re.test(m)) return { kind: 'financial', reply: FINANCIAL_REPLY };
  }
  return null;
}

export { preFilterSafety };
