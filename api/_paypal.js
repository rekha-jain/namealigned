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
   Hardcoded ($5.00 USD) so it stays in sync with the rest of the codebase
   even if a stale Vercel env var exists. The frontend (report.html) now
   always sends amount explicitly in createOrder ($5 full, $2.50 with the
   50%-off promo) — this default only kicks in if a future caller forgets
   to pass amount, in which case we want the canonical price, not whatever
   was in env from the old ₹199/$2.99 era. */
export function getDefaultAmount() {
  return {
    value:    '5.00',
    currency: 'USD',
  };
}
