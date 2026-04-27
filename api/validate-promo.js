/**
 * POST /api/validate-promo
 *
 * Validates a promo code and returns the discount type.
 * For 100% off, generates a short-lived HMAC-signed token
 * that generate-report.js will accept in place of a Razorpay payment ID.
 *
 * Env vars (set in Vercel dashboard):
 *   PROMO_50_CODES   — comma-separated list of 50%-off codes
 *   PROMO_100_CODES  — comma-separated list of 100%-off codes
 *   PROMO_SECRET     — random secret for HMAC signing (generate once, keep private)
 *
 * Example codes you can set:
 *   PROMO_50_CODES  = NA50JYOTI,ALIGNED50,CHALDEAN50XK
 *   PROMO_100_CODES = NA100NAKSH,COSMOS100FREE,ALIGNED100ZP
 */

'use strict';

import crypto from 'crypto';

const CORS_HEADERS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
};

function sendJSON(res, status, payload) {
  res.status(status).json(payload);
}

/** Parse a comma-separated env var into a normalised Set of uppercase codes. */
function parseCodes(envValue) {
  if (!envValue) return new Set();
  return new Set(
    envValue.split(',').map(c => c.trim().toUpperCase()).filter(Boolean)
  );
}

/**
 * Generate a signed token for 100%-off redemptions.
 * Format: PROMO100_<24-hex-hmac>_<unix-seconds>
 * Expires in 2 hours.
 */
function makePromoToken(email, secret) {
  const ts   = Math.floor(Date.now() / 1000);
  const hmac = crypto
    .createHmac('sha256', secret)
    .update(`${email.toLowerCase()}:${ts}`)
    .digest('hex')
    .slice(0, 24);
  return `PROMO100_${hmac}_${ts}`;
}

export default async function handler(req, res) {
  Object.entries(CORS_HEADERS).forEach(([k, v]) => res.setHeader(k, v));

  if (req.method === 'OPTIONS') return res.status(204).end();
  if (req.method !== 'POST')
    return sendJSON(res, 405, { success: false, error: 'Method not allowed' });

  const { code, email } = req.body || {};

  if (!code || typeof code !== 'string' || !code.trim()) {
    return sendJSON(res, 400, { valid: false, error: 'Promo code is required' });
  }

  const normalised = code.trim().toUpperCase();
  const codes50    = parseCodes(process.env.PROMO_50_CODES);
  const codes100   = parseCodes(process.env.PROMO_100_CODES);
  const secret     = process.env.PROMO_SECRET || 'changeme-set-PROMO_SECRET-in-vercel';

  if (codes50.has(normalised)) {
    return sendJSON(res, 200, { valid: true, discount: 50 });
  }

  if (codes100.has(normalised)) {
    // Need email to sign the token
    if (!email || typeof email !== 'string' || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.trim())) {
      return sendJSON(res, 400, {
        valid: true,
        discount: 100,
        needEmail: true,
        error: 'Please enter your email before applying a 100%-off code.',
      });
    }
    const promoToken = makePromoToken(email.trim().toLowerCase(), secret);
    return sendJSON(res, 200, { valid: true, discount: 100, promoToken });
  }

  return sendJSON(res, 200, { valid: false, error: 'Invalid promo code' });
}
