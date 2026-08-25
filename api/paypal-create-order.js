/**
 * Vercel Serverless Function, POST /api/paypal-create-order
 *
 * Browser calls this to start a PayPal checkout. Returns the PayPal order id
 * which the JS SDK then uses to render the approval flow on PayPal's domain.
 *
 * Body (optional):
 *   { amount: '5.00', currency: 'USD', promo_discount: 50, name, email, dob }
 *   amount '2.50' for 50%-off promo
 *
 * Returns: { id: 'PAYPAL_ORDER_ID' }
 */
'use strict';

import { getPaypalConfig, getAccessToken, getDefaultAmount } from './_paypal.js';

const CORS_HEADERS = {
  'Access-Control-Allow-Origin':  '*',
  'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
};

const FULL_AMOUNT_USD = '5.00';
const SALE_AMOUNT_USD = '2.50';
const TEST95_AMOUNT_USD = '0.25'; // $0.25 = 95% off $5
const ALLOWED_AMOUNTS_USD = new Set([FULL_AMOUNT_USD, SALE_AMOUNT_USD, TEST95_AMOUNT_USD]);

function sendJSON(res, status, payload) { res.status(status).json(payload); }

function resolveAmount(body) {
  const promo = Number(body && body.promo_discount) || 0;
  // Server is authoritative for promo pricing.
  if (promo === 95) return TEST95_AMOUNT_USD;
  if (promo === 50) return SALE_AMOUNT_USD;

  const raw = body && body.amount != null ? String(body.amount).trim() : '';
  if (ALLOWED_AMOUNTS_USD.has(raw)) return raw;

  // Default launch checkout to the sale price when amount is omitted.
  if (!raw) return SALE_AMOUNT_USD;
  return null;
}

export default async function handler(req, res) {
  Object.entries(CORS_HEADERS).forEach(([k, v]) => res.setHeader(k, v));
  if (req.method === 'OPTIONS') return res.status(204).end();

  // GET returns the public Client ID so report.html can load the PayPal SDK
  // with the exact same credentials used by create/capture (no extra function).
  if (req.method === 'GET') {
    try {
      const { env, clientId } = getPaypalConfig();
      const def = getDefaultAmount();
      return sendJSON(res, 200, {
        success: true,
        env,
        clientId,
        currency: def.currency || 'USD',
      });
    } catch (err) {
      console.error('[paypal] config GET failed:', err.message || err);
      return sendJSON(res, 503, { success: false, error: err.message || 'PayPal not configured' });
    }
  }

  if (req.method !== 'POST') return sendJSON(res, 405, { success: false, error: 'Method not allowed' });

  try {
    const { currency: bodyCurrency, name, email, dob, mobile, promo_discount } = req.body || {};
    const def = getDefaultAmount();
    const amount = resolveAmount(req.body || {});
    const currency = bodyCurrency || def.currency;

    if (!amount) {
      return sendJSON(res, 400, { success: false, error: 'Invalid amount' });
    }

    const { baseUrl } = getPaypalConfig();
    const token = await getAccessToken();

    const orderBody = {
      intent: 'CAPTURE',
      purchase_units: [{
        amount: { currency_code: currency, value: String(amount) },
        description: Number(promo_discount) === 95
          ? '5-Year Chaldean Destiny Report (95% off test)'
          : Number(promo_discount) === 50
          ? '5-Year Chaldean Destiny Report (50% off)'
          : '5-Year Chaldean Destiny Report',
        // We stash buyer info into custom_id so it's available on capture
        // even if the browser dies between approve and capture.
        custom_id: JSON.stringify({
          name:   name   || '',
          email:  email  || '',
          dob:    dob    || '',
          mobile: mobile || '',
          promo_discount: Number(promo_discount) || 0,
        }).slice(0, 127), // PayPal limit
      }],
      application_context: {
        brand_name:  'NameAligned.com',
        user_action: 'PAY_NOW',
        shipping_preference: 'NO_SHIPPING',
      },
    };

    const r = await fetch(`${baseUrl}/v2/checkout/orders`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(orderBody),
    });

    if (!r.ok) {
      const body = await r.text();
      console.error(`[paypal] create-order failed status=${r.status} body=${body}`);
      return sendJSON(res, 502, { success: false, error: 'Could not create PayPal order' });
    }

    const data = await r.json();
    console.log(`[paypal] order created id=${data.id} amount=${amount} ${currency} promo=${Number(promo_discount)||0}`);
    return sendJSON(res, 200, { success: true, id: data.id, amount, currency });
  } catch (err) {
    console.error('[paypal] create-order threw:', err);
    return sendJSON(res, 500, { success: false, error: err.message || 'Internal error' });
  }
}
