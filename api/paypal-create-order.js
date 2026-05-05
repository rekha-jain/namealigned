/**
 * Vercel Serverless Function, POST /api/paypal-create-order
 *
 * Browser calls this to start a PayPal checkout. Returns the PayPal order id
 * which the JS SDK then uses to render the approval flow on PayPal's domain.
 *
 * Body (optional):
 *   { amount: '2.99', currency: 'USD', name: '...', email: '...', dob: '...' }
 *
 * Returns: { id: 'PAYPAL_ORDER_ID' }
 */
'use strict';

import { getPaypalConfig, getAccessToken, getDefaultAmount } from './_paypal.js';

const CORS_HEADERS = {
  'Access-Control-Allow-Origin':  '*',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
};

function sendJSON(res, status, payload) { res.status(status).json(payload); }

export default async function handler(req, res) {
  Object.entries(CORS_HEADERS).forEach(([k, v]) => res.setHeader(k, v));
  if (req.method === 'OPTIONS') return res.status(204).end();
  if (req.method !== 'POST') return sendJSON(res, 405, { success: false, error: 'Method not allowed' });

  try {
    const { amount: bodyAmount, currency: bodyCurrency, name, email, dob, mobile } = req.body || {};
    const def = getDefaultAmount();
    const amount   = bodyAmount   || def.value;
    const currency = bodyCurrency || def.currency;

    const { baseUrl } = getPaypalConfig();
    const token = await getAccessToken();

    const orderBody = {
      intent: 'CAPTURE',
      purchase_units: [{
        amount: { currency_code: currency, value: String(amount) },
        description: '5-Year Chaldean Destiny Report',
        // We stash buyer info into custom_id so it's available on capture
        // even if the browser dies between approve and capture.
        custom_id: JSON.stringify({
          name:   name   || '',
          email:  email  || '',
          dob:    dob    || '',
          mobile: mobile || '',
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
    console.log(`[paypal] order created id=${data.id} amount=${amount} ${currency}`);
    return sendJSON(res, 200, { success: true, id: data.id });
  } catch (err) {
    console.error('[paypal] create-order threw:', err);
    return sendJSON(res, 500, { success: false, error: err.message || 'Internal error' });
  }
}
