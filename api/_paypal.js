/**
 * PayPal helper, shared by api/paypal-create-order.js and api/paypal-capture.js.
 *
 * Required env on Vercel:
 *   PAYPAL_ENV       'sandbox' or 'live'  (defaults to 'sandbox')
 *   PAYPAL_CLIENT_ID public client id (also embedded in report.html JS SDK)
 *   PAYPAL_SECRET    server secret, never exposed to the browser
 *
 * Optional:
 *   PAYPAL_AMOUNT    default order amount (string, default '2.99')
 *   PAYPAL_CURRENCY  default order currency (default 'USD')
 */
'use strict';

export function getPaypalConfig() {
  const env       = (process.env.PAYPAL_ENV || 'sandbox').toLowerCase();
  const clientId  = process.env.PAYPAL_CLIENT_ID || '';
  const secret    = process.env.PAYPAL_SECRET    || '';
  const baseUrl   = env === 'live'
    ? 'https://api-m.paypal.com'
    : 'https://api-m.sandbox.paypal.com';

  if (!clientId || !secret) {
    throw new Error('PAYPAL_CLIENT_ID / PAYPAL_SECRET not configured on the server.');
  }
  return { env, clientId, secret, baseUrl };
}

/**
 * Fetch a short-lived OAuth access token. Cached for the lifetime of the
 * lambda invocation only (cold-start safe; no cross-invoke cache).
 */
let _cachedToken = null;
let _cachedExpiry = 0;

export async function getAccessToken() {
  // Re-use within the same warm invocation if it's still valid for >60s.
  if (_cachedToken && Date.now() < _cachedExpiry - 60_000) {
    return _cachedToken;
  }

  const { baseUrl, clientId, secret } = getPaypalConfig();
  const auth = Buffer.from(`${clientId}:${secret}`).toString('base64');

  const res = await fetch(`${baseUrl}/v1/oauth2/token`, {
    method: 'POST',
    headers: {
      Authorization: `Basic ${auth}`,
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: 'grant_type=client_credentials',
  });

  if (!res.ok) {
    const body = await res.text();
    throw new Error(`PayPal token fetch failed [${res.status}]: ${body}`);
  }

  const data = await res.json();
  _cachedToken  = data.access_token;
  _cachedExpiry = Date.now() + (data.expires_in * 1000);
  return _cachedToken;
}

/** Default order amount + currency.
   Hardcoded ($2.50 USD sale price) so it stays in sync with the launch
   PROMO50 default even if a stale Vercel env var exists. The frontend
   (report.html) sends amount + promo_discount explicitly; this default
   only kicks in if a future caller forgets to pass amount. */
export function getDefaultAmount() {
  return {
    value:    '2.50',
    currency: 'USD',
  };
}

// ---------------------------------------------------------------------------
// Buyer info round-trip through purchase_units[0].custom_id (127 char cap).
// Short keys, and the name is trimmed to fit, so the JSON never gets cut
// mid-string (the old full-key JSON was sliced and often unparseable).
// ---------------------------------------------------------------------------
export function buildCustomId({ name = '', email = '', dob = '', mobile = '', promo_discount = 0 } = {}) {
  const base = { e: String(email || ''), d: String(dob || ''), m: String(mobile || ''), p: Number(promo_discount) || 0 };
  let n = String(name || '');
  let out = JSON.stringify({ ...base, n });
  while (out.length > 127 && n.length) {
    n = n.slice(0, -1);
    out = JSON.stringify({ ...base, n });
  }
  if (out.length > 127) out = JSON.stringify({ e: base.e.slice(0, 115) });
  return out;
}

export function parseCustomId(raw) {
  if (!raw) return {};
  try {
    const o = JSON.parse(raw);
    return {
      name:   o.n ?? o.name ?? '',
      email:  o.e ?? o.email ?? '',
      dob:    o.d ?? o.dob ?? '',
      mobile: o.m ?? o.mobile ?? '',
      promo_discount: Number(o.p ?? o.promo_discount) || 0,
    };
  } catch {
    // Legacy truncated JSON: salvage the email if present.
    const m = /"email":"([^"]+)"/.exec(String(raw));
    return m ? { email: m[1] } : {};
  }
}

/** Pull PayPal's decline / error detail out of an API error body. */
export function paypalErrorDetails(data) {
  const d = (data && Array.isArray(data.details) && data.details[0]) || {};
  return {
    issue:       d.issue || (data && data.name) || null,
    description: d.description || (data && data.message) || null,
    debugId:     (data && data.debug_id) || null,
  };
}

export async function getPaypalOrder(orderID) {
  const { baseUrl } = getPaypalConfig();
  const token = await getAccessToken();
  const r = await fetch(`${baseUrl}/v2/checkout/orders/${encodeURIComponent(orderID)}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  const data = await r.json().catch(() => ({}));
  return { ok: r.ok, status: r.status, data };
}

const sleep = (ms) => new Promise(r => setTimeout(r, ms));

/**
 * Capture an order, idempotently. Both the browser (onApprove) and the
 * CHECKOUT.ORDER.APPROVED webhook may call this for the same order, so:
 *   - PayPal-Request-Id makes a repeat capture return the first result.
 *   - If PayPal still says it is already captured / in progress, we read
 *     the order and treat status COMPLETED as success.
 *
 * Returns { ok, data, capture, issue, description, debugId, httpStatus }.
 * `data` is order-shaped (purchase_units[0].payments.captures[0]).
 */
export async function capturePaypalOrder(orderID) {
  const { baseUrl } = getPaypalConfig();
  const token = await getAccessToken();
  const r = await fetch(`${baseUrl}/v2/checkout/orders/${encodeURIComponent(orderID)}/capture`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json',
      'PayPal-Request-Id': `capture-${orderID}`,
    },
  });
  let data = await r.json().catch(() => ({}));
  let httpStatus = r.status;

  if (!r.ok) {
    const err = paypalErrorDetails(data);
    const recoverable = ['ORDER_ALREADY_CAPTURED', 'PREVIOUS_REQUEST_IN_PROGRESS', 'DUPLICATE_REQUEST_ID']
      .includes(err.issue) || r.status === 409;
    if (!recoverable) return { ok: false, data, httpStatus, ...err };
    for (let i = 0; i < 3; i++) {
      const o = await getPaypalOrder(orderID);
      if (o.ok && o.data.status === 'COMPLETED') { data = o.data; httpStatus = 200; break; }
      if (i < 2) await sleep(1500);
      else return { ok: false, data, httpStatus, ...err };
    }
  }

  const capture = data?.purchase_units?.[0]?.payments?.captures?.[0] || null;
  const captureStatus = capture?.status || null;
  if (data.status !== 'COMPLETED' || captureStatus === 'DECLINED' || captureStatus === 'FAILED') {
    return {
      ok: false, data, capture, httpStatus,
      issue: captureStatus === 'DECLINED' || captureStatus === 'FAILED'
        ? (capture?.status_details?.reason || `CAPTURE_${captureStatus}`)
        : `ORDER_${data.status || 'UNKNOWN'}`,
      description: `Order status ${data.status || 'unknown'}, capture status ${captureStatus || 'none'}`,
      debugId: data.debug_id || null,
    };
  }
  if (captureStatus === 'PENDING') {
    console.warn(`[paypal] capture PENDING order=${orderID} reason=${capture?.status_details?.reason}`);
  }
  return { ok: true, data, capture, httpStatus };
}

/**
 * Verify a PayPal webhook via PayPal's verify-webhook-signature API.
 * Needs PAYPAL_WEBHOOK_ID (Developer Dashboard → your app → Webhooks).
 */
export async function verifyPaypalWebhook(headers, event) {
  const webhookId = process.env.PAYPAL_WEBHOOK_ID || '';
  if (!webhookId) {
    console.error('[paypal/webhook] PAYPAL_WEBHOOK_ID not set, rejecting webhook');
    return false;
  }
  const h = (k) => headers[k] || headers[k.toLowerCase()] || '';
  const { baseUrl } = getPaypalConfig();
  const token = await getAccessToken();
  const r = await fetch(`${baseUrl}/v1/notifications/verify-webhook-signature`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      auth_algo:         h('paypal-auth-algo'),
      cert_url:          h('paypal-cert-url'),
      transmission_id:   h('paypal-transmission-id'),
      transmission_sig:  h('paypal-transmission-sig'),
      transmission_time: h('paypal-transmission-time'),
      webhook_id:        webhookId,
      webhook_event:     event,
    }),
  });
  const data = await r.json().catch(() => ({}));
  if (!r.ok || data.verification_status !== 'SUCCESS') {
    console.warn(`[paypal/webhook] verification failed http=${r.status} status=${data.verification_status}`);
    return false;
  }
  return true;
}
