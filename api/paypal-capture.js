/**
 * Vercel Serverless Function, POST /api/paypal-capture
 *
 * Browser calls this from the PayPal SDK's onApprove() callback. We:
 *   1. Capture the order against PayPal (server-side, with the OAuth token).
 *   2. Verify status === 'COMPLETED'.
 *   3. Insert into Supabase orders (same shape as Razorpay path, payment_status:'paid').
 *   4. Fire Mixpanel 'Payment Completed' + 'Order Created' (server-side).
 *   5. Send the report delivery email via Brevo.
 *   6. Return success so the browser can redirect to /generate-report.
 *
 * Body:
 *   { orderID: 'PAYPAL_ORDER_ID', name, dob, email, mobile, birthNum, destNum, nameNum }
 */
'use strict';

import { getPaypalConfig, getAccessToken } from './_paypal.js';
import { insertSupabaseRow, findLeadIdByEmail } from './_supabase.js';
import { mpTrack } from './_mixpanel.js';

const CORS_HEADERS = {
  'Access-Control-Allow-Origin':  '*',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
};

function sendJSON(res, status, payload) { res.status(status).json(payload); }

function escapeHtml(s) {
  return String(s || '')
    .replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')
    .replace(/"/g,'&quot;').replace(/'/g,'&#039;');
}

async function saveOrderToSupabase({ paypalOrderId, paypalCaptureId, name, email, dob, mobile, birthNum, destNum, nameNum, amount, currency }) {
  let lead_id = null;
  try { lead_id = await findLeadIdByEmail(email); }
  catch (e) { console.error('[orders/paypal] lead_id lookup error (continuing with null):', e); }

  return await insertSupabaseRow('orders', {
    lead_id,
    name,
    dob: dob || null,
    payment_status: 'paid',
    razorpay_payment_id: null,
    paypal_order_id:    paypalOrderId,
    paypal_capture_id:  paypalCaptureId,
    payment_provider:   'paypal',
    payment_amount:     amount  || null,
    payment_currency:   currency || null,
    email,
    phone: mobile || null,
    moolank:     birthNum ?? null,
    bhagyank:    destNum ?? null,
    name_number: nameNum ?? null,
    created_at:  new Date().toISOString(),
  }, { duplicateOk: true });
}

async function sendDeliveryEmail({ paypalOrderId, name, email, dob, mobile, birthNum, destNum, nameNum }) {
  const reportUrl =
    `https://namealigned.com/generate-report` +
    `?paymentId=${encodeURIComponent('PP-' + paypalOrderId)}` +
    `&name=${encodeURIComponent(name || '')}` +
    `&dob=${encodeURIComponent(dob || '')}` +
    `&email=${encodeURIComponent(email || '')}` +
    (mobile ? `&mobile=${encodeURIComponent(mobile)}` : '') +
    `&birthNum=${encodeURIComponent(birthNum ?? '')}` +
    `&destNum=${encodeURIComponent(destNum ?? '')}` +
    `&nameNum=${encodeURIComponent(nameNum ?? '')}`;

  const html = `<!DOCTYPE html><html><body style="margin:0;padding:0;background:#f5f0eb;font-family:Georgia,serif;">
<table width="100%" cellpadding="0" cellspacing="0" style="background:#f5f0eb;padding:40px 0;"><tr><td align="center">
<table width="600" style="background:#fff;border-radius:12px;overflow:hidden;max-width:600px;width:100%;box-shadow:0 4px 24px rgba(0,0,0,.08);">
<tr><td style="background:linear-gradient(135deg,#071e2d 0%,#0c3347 100%);padding:40px 48px;text-align:center;">
<p style="margin:0 0 8px;font-size:13px;letter-spacing:3px;text-transform:uppercase;color:#06b6d4;">NameAligned.com</p>
<h1 style="margin:0;font-size:28px;font-weight:normal;color:#fff;line-height:1.3;">Your Numerology Report<br>is Ready ✨</h1></td></tr>
<tr><td style="padding:40px 48px 24px;">
<p style="margin:0 0 16px;font-size:16px;color:#374151;line-height:1.7;">Dear <strong>${escapeHtml(name)}</strong>,</p>
<p style="margin:0;font-size:15px;color:#6b7280;line-height:1.7;">Thank you for your purchase. Your complete Chaldean numerology report is ready, click below to access it anytime.</p>
</td></tr>
<tr><td style="padding:0 48px 48px;text-align:center;">
<a href="${reportUrl}" style="display:inline-block;padding:18px 48px;background:linear-gradient(135deg,#f0b429,#f5d060);color:#1a0533;text-decoration:none;border-radius:8px;font-size:17px;font-weight:700;">Open My Full Report →</a>
<p style="margin:16px 0 0;font-size:12px;color:#9ca3af;font-family:Arial,sans-serif;">This link is unique to your reading. Please keep it safe.</p>
</td></tr>
<tr><td style="background:#f9fafb;padding:24px 48px;text-align:center;border-top:1px solid #e5e7eb;">
<p style="margin:0;font-size:12px;color:#9ca3af;line-height:1.6;font-family:Arial,sans-serif;">
Questions? <a href="mailto:hello@namealigned.com" style="color:#0e7490;">hello@namealigned.com</a><br>
© ${new Date().getFullYear()} NameAligned.com</p></td></tr>
</table></td></tr></table></body></html>`;

  const r = await fetch('https://api.brevo.com/v3/smtp/email', {
    method: 'POST',
    headers: { 'api-key': process.env.BREVO_API_KEY, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      sender: { name: 'NameAligned', email: 'support@namealigned.com' },
      to: [{ email, name: name || email }],
      subject: 'Your numerology report is ready 🌟',
      htmlContent: html,
    }),
  });
  if (!r.ok) console.error(`[paypal/brevo] email failed [${r.status}]: ${await r.text()}`);
}

export default async function handler(req, res) {
  Object.entries(CORS_HEADERS).forEach(([k, v]) => res.setHeader(k, v));
  if (req.method === 'OPTIONS') return res.status(204).end();
  if (req.method !== 'POST')    return sendJSON(res, 405, { success: false, error: 'Method not allowed' });

  try {
    const { orderID, name, dob, email, mobile, birthNum, destNum, nameNum } = req.body || {};
    if (!orderID) return sendJSON(res, 400, { success: false, error: 'orderID is required' });
    if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(String(email).trim())) {
      return sendJSON(res, 400, { success: false, error: 'A valid email is required' });
    }

    const cleanEmail = email.trim().toLowerCase();
    const cleanName  = (name || '').trim();

    const { baseUrl } = getPaypalConfig();
    const token = await getAccessToken();

    // 1. Capture the order
    const captureRes = await fetch(`${baseUrl}/v2/checkout/orders/${orderID}/capture`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
    });
    const captureData = await captureRes.json();

    if (!captureRes.ok || captureData.status !== 'COMPLETED') {
      console.warn(`[paypal] capture not completed status=${captureRes.status} paypalStatus=${captureData.status}`);
      return sendJSON(res, 402, { success: false, verified: false, error: `Payment not completed (status: ${captureData.status || 'unknown'})` });
    }

    const captureId = captureData?.purchase_units?.[0]?.payments?.captures?.[0]?.id || null;
    const captureAmount = captureData?.purchase_units?.[0]?.payments?.captures?.[0]?.amount?.value || null;
    const captureCurrency = captureData?.purchase_units?.[0]?.payments?.captures?.[0]?.amount?.currency_code || null;

    console.log(`[paypal] captured order=${orderID} capture=${captureId} amount=${captureAmount} ${captureCurrency}`);

    // 2. Save to Supabase
    let orderInserted = true;
    try {
      const saved = await saveOrderToSupabase({
        paypalOrderId:   orderID,
        paypalCaptureId: captureId,
        name:     cleanName,
        email:    cleanEmail,
        dob:      dob || null,
        mobile:   mobile || null,
        birthNum: birthNum ?? null,
        destNum:  destNum  ?? null,
        nameNum:  nameNum  ?? null,
        amount:   captureAmount,
        currency: captureCurrency,
      });
      orderInserted = saved !== null;
      console.log(`[orders/paypal] saved order=${orderID} email=${cleanEmail} inserted=${orderInserted}`);
    } catch (dbErr) {
      console.error('[orders/paypal] CRITICAL save failed:', dbErr);
      return sendJSON(res, 500, { success: false, verified: true, error: 'Payment captured but order could not be saved. Support has been alerted.' });
    }

    // 3. Mixpanel events (only on a fresh insert, dedup with Razorpay path)
    if (orderInserted) {
      try {
        const eventProps = {
          payment_id:    'PP-' + orderID,
          paypal_order:  orderID,
          paypal_capture: captureId,
          name:          cleanName,
          dob:           dob || null,
          mobile:        mobile || null,
          moolank:       birthNum ?? null,
          bhagyank:      destNum  ?? null,
          name_number:   nameNum  ?? null,
          amount:        captureAmount,
          currency:      captureCurrency,
          provider:      'paypal',
        };
        await mpTrack('Payment Completed', cleanEmail, eventProps);
        await mpTrack('Order Created',     cleanEmail, eventProps);
      } catch (mpErr) {
        console.error('[paypal/mixpanel] events failed:', mpErr);
      }
    }

    // 4. Email delivery (best-effort)
    try {
      await sendDeliveryEmail({
        paypalOrderId: orderID,
        name:     cleanName,
        email:    cleanEmail,
        dob:      dob || '',
        mobile:   mobile || '',
        birthNum, destNum, nameNum,
      });
    } catch (emailErr) {
      console.error('[paypal/brevo] unexpected error:', emailErr);
    }

    return sendJSON(res, 200, { success: true, verified: true, paymentId: 'PP-' + orderID });
  } catch (err) {
    console.error('[paypal] capture handler threw:', err);
    return sendJSON(res, 500, { success: false, error: err.message || 'Internal error' });
  }
}
