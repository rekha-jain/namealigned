/**
 * Gemini-only LLM router. Cascades across free-tier models, returning
 * the full reply as one chunk. The frontend typewriter creates the
 * streaming feel.
 *
 * We previously used :streamGenerateContent with SSE, but it was
 * fragile on the free tier (intermittent empty streams). The legacy
 * /api/aura endpoint uses :generateContent reliably; we mirror that.
 *
 * The async-generator shape is preserved so the orchestrator code in
 * message.js does not change.
 */

'use strict';

const FREE_CASCADE = ['gemini-flash-latest', 'gemini-2.5-flash', 'gemini-2.5-flash-lite'];

function buildPayload({ system, contents }) {
  return {
    systemInstruction: { parts: [{ text: system }] },
    contents,
    generationConfig: {
      temperature: 0.8,
      topP: 0.95,
      maxOutputTokens: 220,
      // Gemini 2.5 burns "thinking" tokens against this budget; disable
      // so replies are fast and full.
      thinkingConfig: { thinkingBudget: 0 },
    },
    safetySettings: [
      { category: 'HARM_CATEGORY_HARASSMENT',        threshold: 'BLOCK_ONLY_HIGH' },
      { category: 'HARM_CATEGORY_HATE_SPEECH',       threshold: 'BLOCK_ONLY_HIGH' },
      { category: 'HARM_CATEGORY_SEXUALLY_EXPLICIT', threshold: 'BLOCK_ONLY_HIGH' },
      { category: 'HARM_CATEGORY_DANGEROUS_CONTENT', threshold: 'BLOCK_ONLY_HIGH' },
    ],
  };
}

/**
 * Call one model. Returns the assistant text or throws.
 */
async function callModel(model, payload, apiKey) {
  const url = 'https://generativelanguage.googleapis.com/v1beta/models/'
    + encodeURIComponent(model)
    + ':generateContent?key=' + encodeURIComponent(apiKey);

  const ctrl = new AbortController();
  const timer = setTimeout(() => ctrl.abort(), 20000);
  try {
    const r = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
      signal: ctrl.signal,
    });

    if (!r.ok) {
      const errText = await r.text().catch(() => '');
      const err = Object.assign(new Error('upstream_' + r.status), {
        status: r.status, body: errText.slice(0, 400), model,
      });
      throw err;
    }

    const data = await r.json();
    const parts = (((data.candidates || [])[0] || {}).content || {}).parts || [];
    const text = parts.map(p => (p && p.text) ? p.text : '').join('').trim();
    if (!text) {
      const finish = ((data.candidates || [])[0] || {}).finishReason || 'unknown';
      throw Object.assign(new Error('empty_reply'), { model, finish, status: 502 });
    }
    return text;
  } finally {
    clearTimeout(timer);
  }
}

/**
 * Async generator wrapper. Yields a single { text, model } chunk on
 * success. Throws after every model in the cascade fails.
 */
async function* streamLLM({ system, userText, history }) {
  const apiKey = process.env.GEMINI_API_KEY;
  if (!apiKey) {
    const e = new Error('GEMINI_API_KEY not set'); e.code = 'no_api_key'; throw e;
  }

  // Build Gemini-format contents from chat history + latest user turn.
  const contents = [];
  for (const m of history || []) {
    if (!m || !m.content) continue;
    if (m.role === 'user' || m.role === 'assistant') {
      contents.push({
        role: m.role === 'assistant' ? 'model' : 'user',
        parts: [{ text: String(m.content) }],
      });
    }
  }
  contents.push({ role: 'user', parts: [{ text: String(userText) }] });

  const payload = buildPayload({ system, contents });

  let lastErr;
  for (const model of FREE_CASCADE) {
    try {
      const text = await callModel(model, payload, apiKey);
      yield { text, model };
      return;
    } catch (err) {
      lastErr = err;
      const status = err && err.status;
      // Retryable -> cascade. Programmer errors (401/403/404) bail.
      if (status === 401 || status === 403 || status === 404) {
        console.error('[aura/llmRouter] non-retryable on model=' + model, status, err && err.body);
        throw err;
      }
      console.error('[aura/llmRouter] model=' + model + ' failed:', err && err.message, err && err.body);
      continue;
    }
  }
  throw lastErr || new Error('all_models_failed');
}

export { streamLLM, FREE_CASCADE };
