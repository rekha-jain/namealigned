/**
 * Shared recorder for failed / cancelled payment attempts (Razorpay + PayPal).
 *
 * Sources:
 *   'client'  , browser callbacks (Razorpay payment.failed / ondismiss,
 *                PayPal onCancel / onError), via POST /api/generate-report
 *                { action: 'payment-event' }. Untrusted, size-capped.
 *   'server'  , our own PayPal capture call failed (api/paypal-capture.js)
 *   'webhook' , signed provider webhooks (Razorpay payment.failed,
 *                PayPal PAYMENT.CAPTURE.DENIED)
 *
 * Writes to public.payment_failures (docs/supabase/payment-failures.sql),
 * one row per (provider, reference_id). A trusted source (server/webhook)
 * overwrites an earlier client row for the same reference. Mixpanel
 * 'Payment Failed' / 'Checkout Cancelled' fires only on the first record,
 * so a Razorpay failure reported by both browser and webhook counts once.
 *
 * Never throws: failure tracking must not break checkout.
 */
'use strict';

import { getSupabaseConfig, insertSupabaseRow } from './_supabase.js';
import { buildSupabaseHeaders } from './_supabaseHeaders.js';
import { mpTrack } from './_mixpanel.js';

const TABLE = 'payment_failures';
const PROVIDERS = new Set(['razorpay', 'paypal']);
const KINDS = new Set(['failed', 'cancelled']);
const TRUSTED = new Set(['server', 'webhook']);

function clip(v, n = 300) {
  if (v === undefined || v === null) return null;
  const s = String(v).trim();
  return s ? s.slice(0, n) : null;
}

function toAmount(v) {
  const n = Number(v);
  return Number.isFinite(n) && n >= 0 && n < 1e7 ? n : null;
}

async function findByReference(provider, referenceId) {
  const { url, key } = getSupabaseConfig();
  const res = await fetch(
    `${url}/rest/v1/${TABLE}?provider=eq.${encodeURIComponent(provider)}` +
    `&reference_id=eq.${encodeURIComponent(referenceId)}&select=id,kind,reported_by&limit=1`,
    { headers: buildSupabaseHeaders(key) }
  );
  if (!res.ok) throw new Error(`lookup failed [${res.status}]: ${await res.text()}`);
  const rows = await res.json();
  return Array.isArray(rows) && rows[0] ? rows[0] : null;
}

async function patchRow(id, fields) {
  const { url, key } = getSupabaseConfig();
  const res = await fetch(`${url}/rest/v1/${TABLE}?id=eq.${encodeURIComponent(id)}`, {
    method: 'PATCH',
    headers: buildSupabaseHeaders(key, { 'Content-Type': 'application/json', Prefer: 'return=minimal' }),
    body: JSON.stringify({ ...fields, updated_at: new Date().toISOString() }),
  });
  if (!res.ok) throw new Error(`patch failed [${res.status}]: ${await res.text()}`);
}

/**
 * @returns {Promise<'inserted'|'updated'|'duplicate'|'error'>}
 */
export async function recordPaymentFailure(input) {
  const row = {
    provider:          clip(input.provider, 20),
    kind:              KINDS.has(input.kind) ? input.kind : 'failed',
    reference_id:      clip(input.referenceId || input.paymentId || input.orderId, 100),
    payment_id:        clip(input.paymentId, 100),
    order_id:          clip(input.orderId, 100),
    email:             clip(input.email, 200)?.toLowerCase() || null,
    name:              clip(input.name, 120),
    phone:             clip(input.mobile, 20),
    amount:            toAmount(input.amount),
    currency:          clip(input.currency, 8),
    error_code:        clip(input.errorCode, 100),
    error_description: clip(input.errorDescription, 500),
    error_source:      clip(input.errorSource, 100),
    error_step:        clip(input.errorStep, 100),
    error_reason:      clip(input.errorReason, 200),
    debug_id:          clip(input.debugId, 100),
    reported_by:       input.reportedBy,
    user_agent:        clip(input.userAgent, 300),
    raw:               input.raw && typeof input.raw === 'object' ? input.raw : null,
  };

  if (!PROVIDERS.has(row.provider)) return 'error';

  // Always leave a structured log line, even if the table is missing.
  console.warn(
    `[payment-failure] provider=${row.provider} kind=${row.kind} by=${row.reported_by}` +
    ` ref=${row.reference_id} code=${row.error_code} reason=${row.error_reason}` +
    ` desc=${JSON.stringify(row.error_description)} debug_id=${row.debug_id} email=${row.email}`
  );

  let status = 'error';
  try {
    const existing = row.reference_id ? await findByReference(row.provider, row.reference_id) : null;
    if (existing) {
      const upgradeSource = TRUSTED.has(row.reported_by) && existing.reported_by === 'client';
      const upgradeKind = row.kind === 'failed' && existing.kind === 'cancelled';
      if (upgradeSource || upgradeKind) {
        const fields = Object.fromEntries(Object.entries(row).filter(([, v]) => v !== null));
        await patchRow(existing.id, fields);
        status = 'updated';
      } else {
        status = 'duplicate';
      }
    } else {
      // return=representation: a row back means inserted, null means a
      // concurrent duplicate (409) slipped past the lookup.
      const saved = await insertSupabaseRow(TABLE, row, { duplicateOk: true });
      status = saved ? 'inserted' : 'duplicate';
    }
  } catch (err) {
    console.error('[payment-failure] could not store (is payment_failures created?):', err.message || err);
    status = 'error';
  }

  // Mixpanel once per attempt. If the DB write errored we still track,
  // so the funnel is not blind when the table is missing.
  if (status === 'inserted' || status === 'error') {
    try {
      await mpTrack(row.kind === 'cancelled' ? 'Checkout Cancelled' : 'Payment Failed',
        row.email || row.reference_id || 'unknown', {
          provider:     row.provider,
          reference_id: row.reference_id,
          payment_id:   row.payment_id,
          order_id:     row.order_id,
          amount:       row.amount,
          currency:     row.currency,
          error_code:   row.error_code,
          error_reason: row.error_reason,
          error_source: row.error_source,
          error_step:   row.error_step,
          error_description: row.error_description,
          reported_by:  row.reported_by,
        });
    } catch (mpErr) {
      console.error('[payment-failure] mixpanel failed:', mpErr);
    }
  }
  return status;
}

/**
 * POST /api/generate-report { action: 'payment-event', ... }
 * Browser-side failure / cancel reports. Always answers 200 so the
 * browser never surfaces an error for a tracking call.
 */
export async function handleClientPaymentEvent(req, res) {
  const b = req.body || {};
  if (!PROVIDERS.has(b.provider) || !KINDS.has(b.kind)) {
    return res.status(400).json({ success: false, error: 'Invalid payment event' });
  }
  const email = clip(b.email, 200);
  await recordPaymentFailure({
    provider:         b.provider,
    kind:             b.kind,
    referenceId:      b.referenceId,
    paymentId:        b.paymentId,
    orderId:          b.orderId,
    email:            email && /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) ? email : null,
    name:             b.name,
    mobile:           b.mobile,
    amount:           b.amount,
    currency:         b.currency,
    errorCode:        b.errorCode,
    errorDescription: b.errorDescription,
    errorSource:      b.errorSource,
    errorStep:        b.errorStep,
    errorReason:      b.errorReason,
    reportedBy:       'client',
    userAgent:        req.headers?.['user-agent'],
  });
  return res.status(200).json({ success: true });
}
