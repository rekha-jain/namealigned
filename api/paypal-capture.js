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
 *
 * On a failed capture we store PayPal's issue (e.g. INSTRUMENT_DECLINED) and
 * debug_id in payment_failures and return { issue } so the browser can call
 * actions.restart() and let the buyer pick another funding source.
 *
 * Also serves PayPal webhooks (POST /api/paypal-webhook, rewritten here to
 * stay under the Vercel function cap). Requests carrying a
 * paypal-transmission-id header are verified with PAYPAL_WEBHOOK_ID, then:
 *   CHECKOUT.ORDER.APPROVED   , capture if the browser never did, deliver
 *   PAYMENT.CAPTURE.COMPLETED , deliver if no order row exists yet
 *   PAYMENT.CAPTURE.DENIED / DECLINED , record in payment_failures
 * Subscribe those 4 events in the PayPal Developer Dashboard.
 */
'use strict';

import { capturePaypalOrder, getPaypalOrder, parseCustomId, verifyPaypalWebhook } from './_paypal.js';
import { insertSupabaseRow, findLeadIdByEmail, findOrderByPaypalOrderId, markReportSent } from './_supabase.js';
import { sendBrevoEmail as deliverViaBrevo } from './_brevo.js';
import { mpTrack } from './_mixpanel.js';
import { normaliseIndianMobile } from './_phone.js';
import { recordPaymentFailure } from './_paymentFailures.js';

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
  const existing = await findOrderByPaypalOrderId(paypalOrderId);
  if (existing) {
    console.log(`[orders/paypal] ${paypalOrderId} already exists id=${existing.id} (skip insert)`);
    return null;
  }

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

export async function sendDeliveryEmail({ paypalOrderId, name, email, dob, mobile, birthNum, destNum, nameNum }) {
  const reportUrl =
    `https://www.namealigned.com/generate-report` +
    `?paymentId=${encodeURIComponent('PP-' + paypalOrderId)}`;

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

  const result = await deliverViaBrevo({
    to: email,
    toName: name || email,
    subject: 'Your numerology report is ready 🌟',
    htmlContent: html,
    tags: ['report-delivery', 'paypal'],
  });
  if (!result.ok) console.error('[paypal/brevo] email failed:', result.error);
  return result.ok;
}

/**
 * Save + track + email for a captured order. Idempotent: a second call
 * for the same PayPal order finds the row and skips Mixpanel/email.
 */
async function fulfilPaypalOrder({ orderID, orderData, buyer, sourceHandler }) {
  const capture = orderData?.purchase_units?.[0]?.payments?.captures?.[0] || {};
  const captureId       = capture.id || null;
  const captureAmount   = capture.amount?.value || null;
  const captureCurrency = capture.amount?.currency_code || null;
  const { name, email, dob, mobile, birthNum, destNum, nameNum } = buyer;

  console.log(`[paypal] captured order=${orderID} capture=${captureId} amount=${captureAmount} ${captureCurrency} via=${sourceHandler}`);

  // 'inserted' | 'duplicate' | 'failed'
  let orderSaveStatus = 'failed';
  let savedOrderId = null;
  try {
    const saved = await saveOrderToSupabase({
      paypalOrderId:   orderID,
      paypalCaptureId: captureId,
      name, email, dob: dob || null, mobile: mobile || null,
      birthNum: birthNum ?? null, destNum: destNum ?? null, nameNum: nameNum ?? null,
      amount: captureAmount, currency: captureCurrency,
    });
    orderSaveStatus = saved !== null ? 'inserted' : 'duplicate';
    savedOrderId = saved?.id || null;
    console.log(`[orders/paypal] saved order=${orderID} email=${email} status=${orderSaveStatus}`);
  } catch (dbErr) {
    // Payment is already captured at PayPal, never fail the buyer for a DB
    // hiccup. Log loudly so we can reconcile from PayPal.
    console.error('[orders/paypal] CRITICAL save failed (continuing to deliver report):', dbErr);
  }

  if (orderSaveStatus === 'inserted') {
    try {
      const eventProps = {
        payment_id:    'PP-' + orderID,
        paypal_order:  orderID,
        paypal_capture: captureId,
        name, dob: dob || null, mobile: mobile || null,
        moolank: birthNum ?? null, bhagyank: destNum ?? null, name_number: nameNum ?? null,
        amount: captureAmount, currency: captureCurrency,
        provider: 'paypal',
        source_handler: sourceHandler,
      };
      await mpTrack('Payment Completed', email || orderID, eventProps);
      await mpTrack('Order Created',     email || orderID, eventProps);
    } catch (mpErr) {
      console.error('[paypal/mixpanel] events failed:', mpErr);
    }
  }

  // Email on first success. Skip clean duplicates (retries). If the DB
  // failed after capture, still email: the buyer already paid.
  if (orderSaveStatus !== 'duplicate' && email) {
    try {
      const sent = await sendDeliveryEmail({
        paypalOrderId: orderID, name, email, dob: dob || '', mobile: mobile || '',
        birthNum, destNum, nameNum,
      });
      if (sent) await markReportSent(savedOrderId);
    } catch (emailErr) {
      console.error('[paypal/brevo] unexpected error:', emailErr);
    }
  } else if (!email) {
    console.error(`[paypal] CRITICAL no buyer email for order=${orderID}, report not emailed`);
  } else {
    console.log(`[orders/paypal] skip duplicate delivery email order=${orderID}`);
  }
  return orderSaveStatus;
}

/** Buyer details from a PayPal order (custom_id first, payer as fallback). */
function buyerFromOrder(orderData) {
  const pu = orderData?.purchase_units?.[0] || {};
  const cap = pu.payments?.captures?.[0] || {};
  const c = parseCustomId(pu.custom_id || cap.custom_id);
  const payer = orderData?.payer || {};
  const payerName = [payer.name?.given_name, payer.name?.surname].filter(Boolean).join(' ');
  return {
    name:   (c.name || payerName || '').trim(),
    email:  String(c.email || payer.email_address || '').trim().toLowerCase(),
    dob:    c.dob || '',
    mobile: normaliseIndianMobile(c.mobile || ''),
  };
}

const sleep = (ms) => new Promise(r => setTimeout(r, ms));

async function handlePaypalWebhook(req, res) {
  const event = req.body || {};
  if (!(await verifyPaypalWebhook(req.headers || {}, event))) {
    return sendJSON(res, 400, { error: 'Invalid webhook signature' });
  }
  const type = event.event_type;
  const resource = event.resource || {};
  console.log(`[paypal/webhook] ${type} id=${event.id} resource=${resource.id}`);

  try {
    if (type === 'CHECKOUT.ORDER.APPROVED') {
      const orderID = resource.id;
      // Give the browser's onApprove capture a head start; only step in if
      // the order is still sitting in APPROVED (tab closed, network died).
      await sleep(5000);
      if (await findOrderByPaypalOrderId(orderID)) return sendJSON(res, 200, { received: true, handled: 'already-fulfilled' });
      const o = await getPaypalOrder(orderID);
      if (!o.ok) throw new Error(`order lookup failed [${o.status}]`);
      if (o.data.status === 'COMPLETED') {
        // Browser captured; it (or PAYMENT.CAPTURE.COMPLETED) delivers.
        return sendJSON(res, 200, { received: true, handled: 'captured-elsewhere' });
      }
      if (o.data.status !== 'APPROVED') return sendJSON(res, 200, { received: true, handled: false });

      const cap = await capturePaypalOrder(orderID);
      const buyer = buyerFromOrder(cap.ok ? cap.data : o.data);
      if (!cap.ok) {
        await recordPaymentFailure({
          provider: 'paypal', kind: 'failed', referenceId: orderID, orderId: orderID,
          email: buyer.email, name: buyer.name, mobile: buyer.mobile,
          amount: o.data?.purchase_units?.[0]?.amount?.value,
          currency: o.data?.purchase_units?.[0]?.amount?.currency_code,
          errorCode: cap.issue, errorDescription: cap.description, debugId: cap.debugId,
          errorSource: 'webhook_capture', reportedBy: 'webhook',
        });
        return sendJSON(res, 200, { received: true, handled: 'capture-failed' });
      }
      await fulfilPaypalOrder({ orderID, orderData: cap.data, buyer, sourceHandler: 'paypal-webhook-approved' });
      return sendJSON(res, 200, { received: true, handled: true });
    }

    if (type === 'PAYMENT.CAPTURE.COMPLETED') {
      const orderID = resource.supplementary_data?.related_ids?.order_id;
      if (!orderID) return sendJSON(res, 200, { received: true, handled: false });
      // Usually fires while the browser's capture call is still saving the
      // row; wait so we only step in when that path actually died.
      await sleep(5000);
      if (await findOrderByPaypalOrderId(orderID)) return sendJSON(res, 200, { received: true, handled: 'already-fulfilled' });
      const o = await getPaypalOrder(orderID);
      if (!o.ok) throw new Error(`order lookup failed [${o.status}]`);
      await fulfilPaypalOrder({ orderID, orderData: o.data, buyer: buyerFromOrder(o.data), sourceHandler: 'paypal-webhook-capture' });
      return sendJSON(res, 200, { received: true, handled: true });
    }

    if (type === 'PAYMENT.CAPTURE.DENIED' || type === 'PAYMENT.CAPTURE.DECLINED') {
      const orderID = resource.supplementary_data?.related_ids?.order_id || null;
      const c = parseCustomId(resource.custom_id);
      await recordPaymentFailure({
        provider: 'paypal', kind: 'failed',
        referenceId: orderID || resource.id, orderId: orderID, paymentId: resource.id,
        email: c.email, name: c.name, mobile: c.mobile,
        amount: resource.amount?.value, currency: resource.amount?.currency_code,
        errorCode: resource.status_details?.reason || type,
        errorDescription: `${type} (capture status ${resource.status || 'unknown'})`,
        errorSource: 'paypal_webhook', reportedBy: 'webhook',
        raw: { event_id: event.id, event_type: type, capture_status: resource.status || null },
      });
      return sendJSON(res, 200, { received: true, handled: true });
    }

    return sendJSON(res, 200, { received: true, handled: false });
  } catch (err) {
    // Non-2xx makes PayPal retry; fulfilment is idempotent.
    console.error(`[paypal/webhook] ${type} handler failed:`, err);
    return sendJSON(res, 500, { error: 'Webhook processing failed' });
  }
}

export default async function handler(req, res) {
  Object.entries(CORS_HEADERS).forEach(([k, v]) => res.setHeader(k, v));
  if (req.method === 'OPTIONS') return res.status(204).end();
  if (req.method !== 'POST')    return sendJSON(res, 405, { success: false, error: 'Method not allowed' });

  if (req.headers && req.headers['paypal-transmission-id']) return handlePaypalWebhook(req, res);

  try {
    const { orderID, name, dob, email, mobile, birthNum, destNum, nameNum } = req.body || {};
    if (!orderID) return sendJSON(res, 400, { success: false, error: 'orderID is required' });
    if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(String(email).trim())) {
      return sendJSON(res, 400, { success: false, error: 'A valid email is required' });
    }

    const buyer = {
      name:   (name || '').trim(),
      email:  email.trim().toLowerCase(),
      dob:    dob || null,
      mobile: normaliseIndianMobile(mobile) || null,
      birthNum, destNum, nameNum,
    };

    const cap = await capturePaypalOrder(orderID);
    if (!cap.ok) {
      console.warn(`[paypal] capture failed order=${orderID} http=${cap.httpStatus} issue=${cap.issue} debug_id=${cap.debugId} desc=${cap.description}`);
      const pu = cap.data?.purchase_units?.[0];
      await recordPaymentFailure({
        provider: 'paypal', kind: 'failed', referenceId: orderID, orderId: orderID,
        email: buyer.email, name: buyer.name, mobile: buyer.mobile,
        amount: pu?.amount?.value, currency: pu?.amount?.currency_code,
        errorCode: cap.issue, errorDescription: cap.description, debugId: cap.debugId,
        errorSource: 'capture', reportedBy: 'server',
        userAgent: req.headers?.['user-agent'],
      });
      const declined = cap.issue === 'INSTRUMENT_DECLINED';
      return sendJSON(res, 402, {
        success: false, verified: false,
        issue: cap.issue || null,
        error: declined
          ? 'Your PayPal payment method was declined. Please choose another card or funding source.'
          : `Payment not completed${cap.description ? ': ' + cap.description : ''}. You have not been charged.`,
      });
    }

    await fulfilPaypalOrder({ orderID, orderData: cap.data, buyer, sourceHandler: 'paypal-capture' });
    return sendJSON(res, 200, { success: true, verified: true, paymentId: 'PP-' + orderID });
  } catch (err) {
    console.error('[paypal] capture handler threw:', err);
    return sendJSON(res, 500, { success: false, error: err.message || 'Internal error' });
  }
}
