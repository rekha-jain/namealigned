/**
 * GET /api/paypal-config
 *
 * Public PayPal settings for the browser SDK. Client ID is meant to be
 * public (it is already embedded in the JS SDK URL). Never returns the secret.
 *
 * Used by report.html so the on-page SDK always matches the credentials
 * used by /api/paypal-create-order and /api/paypal-capture.
 */
'use strict';

import { getPaypalConfig, getDefaultAmount } from './_paypal.js';

const CORS_HEADERS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
};

export default async function handler(req, res) {
  Object.entries(CORS_HEADERS).forEach(([k, v]) => res.setHeader(k, v));
  if (req.method === 'OPTIONS') return res.status(204).end();
  if (req.method !== 'GET') {
    return res.status(405).json({ success: false, error: 'Method not allowed' });
  }

  try {
    const { env, clientId } = getPaypalConfig();
    const amount = getDefaultAmount();
    if (!clientId) {
      return res.status(503).json({ success: false, error: 'PayPal not configured' });
    }
    return res.status(200).json({
      success: true,
      env,
      clientId,
      currency: amount.currency || 'USD',
    });
  } catch (err) {
    console.error('[paypal-config]', err.message || err);
    return res.status(503).json({
      success: false,
      error: err.message || 'PayPal not configured',
    });
  }
}
