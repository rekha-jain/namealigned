/**
 * Gemini-only streaming router. Cascades across free-tier models so that
 * 429/503/500 on one model falls through to the next, never to the user.
 *
 * Streaming uses Gemini's :streamGenerateContent endpoint with SSE.
 * Each yielded chunk is a plain text fragment ready for the bubble.
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
 * Stream chunks of text from Gemini using the SSE streaming endpoint.
 * Yields plain text fragments. Throws if every model in the cascade
 * returns a retryable error.
 *
 * The caller is responsible for the upstream quota gate, so this
 * function assumes it is allowed to call Gemini.
 */
async function* streamLLM({ system, userText, history }) {
  const apiKey = process.env.GEMINI_API_KEY;
  if (!apiKey) {
    const e = new Error('GEMINI_API_KEY not set'); e.code = 'no_api_key'; throw e;
  }

  // Build contents in Gemini's format.
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
    const url = 'https://generativelanguage.googleapis.com/v1beta/models/'
      + encodeURIComponent(model)
      + ':streamGenerateContent?alt=sse&key=' + encodeURIComponent(apiKey);

    try {
      const ctrl = new AbortController();
      const timer = setTimeout(() => ctrl.abort(), 30000);
      const r = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'text/event-stream' },
        body: JSON.stringify(payload),
        signal: ctrl.signal,
      });

      if (!r.ok) {
        clearTimeout(timer);
        const errText = await r.text().catch(() => '');
        lastErr = Object.assign(new Error('upstream_' + r.status), { status: r.status, body: errText.slice(0, 400), model });
        // Retryable -> cascade. Other errors (401/403/404) -> bail.
        if (r.status === 429 || r.status === 500 || r.status === 503) continue;
        throw lastErr;
      }

      // Stream parser. Gemini SSE emits "data: {json}\n\n" frames.
      const reader = r.body.getReader();
      const decoder = new TextDecoder('utf-8');
      let buf = '';
      let produced = false;
      try {
        while (true) {
          const { value, done } = await reader.read();
          if (done) break;
          buf += decoder.decode(value, { stream: true });
          let nl;
          while ((nl = buf.indexOf('\n\n')) !== -1) {
            const frame = buf.slice(0, nl);
            buf = buf.slice(nl + 2);
            const line = frame.split('\n').find(l => l.startsWith('data: '));
            if (!line) continue;
            const json = line.slice(6).trim();
            if (!json || json === '[DONE]') continue;
            let evt;
            try { evt = JSON.parse(json); } catch { continue; }
            const parts = (((evt.candidates || [])[0] || {}).content || {}).parts || [];
            const text = parts.map(p => (p && p.text) ? p.text : '').join('');
            if (text) { produced = true; yield { text, model }; }
          }
        }
      } finally {
        clearTimeout(timer);
        try { reader.releaseLock(); } catch {}
      }
      if (produced) return;
      // Empty stream, try next model.
      lastErr = Object.assign(new Error('empty_stream'), { model });
      continue;
    } catch (err) {
      if (err && err.name === 'AbortError') {
        lastErr = Object.assign(new Error('timeout'), { model });
        continue;
      }
      lastErr = err;
      // Don't blindly cascade on programmer errors.
      if (err && err.status && (err.status === 401 || err.status === 403 || err.status === 404)) throw err;
      continue;
    }
  }

  throw lastErr || new Error('all_models_failed');
}

export { streamLLM, FREE_CASCADE };
