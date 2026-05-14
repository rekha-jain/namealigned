/**
 * Server-Sent Events helpers for Vercel Node serverless functions.
 * We use the classic Node res object (not Web Streams) because the
 * rest of the codebase is on @vercel/node serverless functions.
 */

'use strict';

function startSSE(res) {
  res.setHeader('Content-Type', 'text/event-stream; charset=utf-8');
  res.setHeader('Cache-Control', 'no-cache, no-transform');
  res.setHeader('Connection', 'keep-alive');
  res.setHeader('X-Accel-Buffering', 'no');
  // CORS: same-origin in production, but allow * for diagnostics
  res.setHeader('Access-Control-Allow-Origin', '*');
  // Flush headers immediately so the client opens the EventSource.
  if (typeof res.flushHeaders === 'function') res.flushHeaders();
}

function sendEvent(res, event, data) {
  // Spec: each event is "event: <name>\ndata: <json>\n\n"
  res.write('event: ' + event + '\n');
  res.write('data: ' + JSON.stringify(data == null ? {} : data) + '\n\n');
}

function endSSE(res) {
  try { res.end(); } catch { /* noop */ }
}

/**
 * Convenience: send a single non-streaming reply over SSE.
 * Used for safety blocks and quota-exhausted messages.
 */
function sseSingleReply(res, { conversationId, messageId, text, kind }) {
  startSSE(res);
  sendEvent(res, 'started',  { conversationId: conversationId || null, messageId: messageId || null });
  sendEvent(res, 'token',    { text: String(text || '') });
  sendEvent(res, 'done',     { kind: kind || 'ok', latencyMs: 0 });
  endSSE(res);
}

export { startSSE, sendEvent, endSSE, sseSingleReply };
