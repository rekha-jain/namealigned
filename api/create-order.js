/**
 * Vercel Serverless Function, POST /api/create-order
 *
 * Creates a Razorpay order server-side and returns the order_id.
 * The frontend uses this order_id when opening the Razorpay checkout,
 * which is required for live payments and enables signature verification.
 *
 * Required environment variables:
 *   RAZORPAY_KEY_ID   , Razorpay live key ID
 *   RAZORPAY_KEY_SECRET, Razorpay live key secret
 */

'use strict';

const CORS_HEADERS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
};

// New pricing: ₹499 full, ₹249 (50% off). Legacy ₹199/₹99 kept temporarily
// so any in-flight pre-price-change orders still validate; remove once
// confirmed no traffic on the old amounts.
const FULL_AMOUNT_PAISE = 49900;
const SALE_AMOUNT_PAISE = 24900;
const ALLOWED_AMOUNTS_PAISE = [FULL_AMOUNT_PAISE, SALE_AMOUNT_PAISE, 19900, 9900];

function resolveAmount(body) {
  const promo = Number(body && body.promo_discount) || 0;
  // Server is authoritative for sale pricing — never trust a full-price
  // amount when the client says the 50% promo is active.
  if (promo === 50) return SALE_AMOUNT_PAISE;

  const amount = Number(body && body.amount);
  if (ALLOWED_AMOUNTS_PAISE.includes(amount)) return amount;

  // Default launch checkout to the sale price when amount is omitted.
  if (body && (body.amount === undefined || body.amount === null || body.amount === '')) {
    return SALE_AMOUNT_PAISE;
  }
  return null;
}

export default async function handler(req, res) {
  Object.entries(CORS_HEADERS).forEach(([k, v]) => res.setHeader(k, v));

  if (req.method === 'OPTIONS') return res.status(204).end();
  if (req.method !== 'POST') {
    return res.status(405).json({ success: false, error: 'Method not allowed' });
  }

  try {
    const amount = resolveAmount(req.body || {});

    if (amount === null) {
      return res.status(400).json({ success: false, error: 'Invalid amount' });
    }

    const credentials = Buffer.from(
      `${process.env.RAZORPAY_KEY_ID}:${process.env.RAZORPAY_KEY_SECRET}`
    ).toString('base64');

    const response = await fetch('https://api.razorpay.com/v1/orders', {
      method: 'POST',
      headers: {
        Authorization: `Basic ${credentials}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        amount,
        currency: 'INR',
        receipt: `rcpt_${Date.now()}`,
        payment_capture: 1,
        notes: {
          promo_discount: String((req.body && req.body.promo_discount) || 0),
        },
      }),
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error(`Razorpay create-order error [${response.status}]: ${errorText}`);
      return res.status(502).json({ success: false, error: 'Failed to create payment order' });
    }

    const order = await response.json();
    console.log(`[razorpay] order created id=${order.id} amount=${order.amount} paise`);

    return res.status(200).json({
      success: true,
      orderId: order.id,
      keyId: process.env.RAZORPAY_KEY_ID,   // return the key used, so frontend never mismatches
      amount: order.amount,
      currency: order.currency,
    });
  } catch (err) {
    console.error('Unhandled error in create-order:', err);
    return res.status(500).json({ success: false, error: 'Internal server error' });
  }
}
