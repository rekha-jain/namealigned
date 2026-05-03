/**
 * Vercel Serverless Function — POST /api/razorpay-webhook
 *
 * Receives Razorpay webhook events, verifies the signature, and handles
 * payment.captured events — saving the order to Supabase and sending the
 * delivery email. This covers UPI / async payments where the browser
 * redirect may not fire reliably.
 *
 * Required environment variables:
 *   RAZORPAY_WEBHOOK_SECRET — set in Razorpay Dashboard → Webhooks
 *   SUPABASE_URL            — e.g. https://xyzxyz.supabase.co
 *   SUPABASE_SERVICE_KEY    — Supabase service role key
 *   BREVO_API_KEY           — Brevo v3 API key
 *
 * Register this URL in Razorpay Dashboard → Webhooks:
 *   https://namealigned.com/api/razorpay-webhook
 *   Event: payment.captured
 */

'use strict';

import crypto from 'crypto';
import { insertSupabaseRow, findLeadIdByEmail } from './_supabase.js';

// ---------------------------------------------------------------------------
// Verify Razorpay webhook signature
// Razorpay signs the raw body with HMAC-SHA256 using your webhook secret.
// ---------------------------------------------------------------------------
function verifyWebhookSignature(rawBody, signature, secret) {
  if (!rawBody || !signature || !secret) return false;
  const expected = crypto
    .createHmac('sha256', secret)
    .update(rawBody)
    .digest('hex');
  try {
    return crypto.timingSafeEqual(Buffer.from(expected), Buffer.from(signature));
  } catch {
    return false;
  }
}

// ---------------------------------------------------------------------------
// Save order to Supabase (same logic as generate-report.js)
// ---------------------------------------------------------------------------
async function saveOrderToSupabase({ paymentId, name, email, dob, mobile, amount }) {
  let lead_id = null;
  try {
    lead_id = await findLeadIdByEmail(email);
  } catch (e) {
    console.error('[orders/webhook] lead_id lookup error (continuing with null):', e);
  }

  // Same shape as generate-report.js — payment_status was the missing column
  // that made every prior insert fail.
  const saved = await insertSupabaseRow('orders', {
    lead_id,
    name:                name || null,
    dob:                 dob || null,
    payment_status:      'paid',
    razorpay_payment_id: paymentId,
    email:               email || null,
    phone:               mobile || null,
    created_at:          new Date().toISOString(),
  }, { duplicateOk: true, prefer: 'return=minimal' });

  if (saved === null) {
    console.log(`[orders/webhook] ${paymentId} duplicate or return=minimal`);
  } else {
    console.log(`[orders/webhook] saved ${paymentId} email=${email}`);
  }
  return saved;
}

// ---------------------------------------------------------------------------
// Send delivery email via Brevo
// ---------------------------------------------------------------------------
function escapeHtml(str) {
  return String(str || '')
    .replace(/&/g, '&amp;').replace(/</g, '&lt;')
    .replace(/>/g, '&gt;').replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

async function sendDeliveryEmail({ paymentId, name, email, dob, mobile }) {
  const reportUrl =
    `https://namealigned.com/generate-report` +
    `?paymentId=${encodeURIComponent(paymentId)}` +
    `&name=${encodeURIComponent(name || '')}` +
    `&dob=${encodeURIComponent(dob || '')}` +
    `&email=${encodeURIComponent(email || '')}` +
    (mobile ? `&mobile=${encodeURIComponent(mobile)}` : '');

  const htmlContent = `
<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"/></head>
<body style="margin:0;padding:0;background:#f5f0eb;font-family:Georgia,serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f5f0eb;padding:40px 0;">
    <tr><td align="center">
      <table width="600" cellpadding="0" cellspacing="0"
             style="background:#fff;border-radius:12px;overflow:hidden;max-width:600px;width:100%;box-shadow:0 4px 24px rgba(0,0,0,.08);">
        <tr>
          <td style="background:linear-gradient(135deg,#071e2d 0%,#0c3347 100%);padding:40px 48px;text-align:center;">
            <p style="margin:0 0 8px;font-size:13px;letter-spacing:3px;text-transform:uppercase;color:#06b6d4;">NameAligned.com</p>
            <h1 style="margin:0;font-size:28px;font-weight:normal;color:#fff;line-height:1.3;">Your Numerology Report<br>is Ready ✨</h1>
          </td>
        </tr>
        <tr>
          <td style="padding:40px 48px 24px;">
            <p style="margin:0 0 16px;font-size:16px;color:#374151;line-height:1.7;">Dear <strong>${escapeHtml(name)}</strong>,</p>
            <p style="margin:0;font-size:15px;color:#6b7280;line-height:1.7;">Thank you for your payment. Your complete Chaldean numerology report is ready. Click below to access it anytime.</p>
          </td>
        </tr>
        <tr>
          <td style="padding:0 48px 48px;text-align:center;">
            <a href="${reportUrl}"
               style="display:inline-block;padding:18px 48px;background:linear-gradient(135deg,#f0b429,#f5d060);
                      color:#1a0533;text-decoration:none;border-radius:8px;font-size:17px;font-weight:700;">
              Open My Full Report →
            </a>
            <p style="margin:16px 0 0;font-size:12px;color:#9ca3af;font-family:Arial,sans-serif;">
              This link is unique to your reading. Please keep it safe.
            </p>
          </td>
        </tr>
        <tr>
          <td style="background:#f9fafb;padding:24px 48px;text-align:center;border-top:1px solid #e5e7eb;">
            <p style="margin:0;font-size:12px;color:#9ca3af;line-height:1.6;font-family:Arial,sans-serif;">
              Questions? <a href="mailto:hello@namealigned.com" style="color:#0e7490;">hello@namealigned.com</a><br>
              © ${new Date().getFullYear()} NameAligned.com
            </p>
          </td>
        </tr>
      </table>
    </td></tr>
  </table>
</body></html>`.trim();

  const response = await fetch('https://api.brevo.com/v3/smtp/email', {
    method: 'POST',
    headers: { 'api-key': process.env.BREVO_API_KEY, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      sender: { name: 'NameAligned', email: 'support@namealigned.com' },
      to: [{ email, name: name || email }],
      subject: 'Your numerology report is ready 🌟',
      htmlContent,
    }),
  });

  if (!response.ok) {
    const text = await response.text();
    console.error(`Brevo webhook email failed [${response.status}]: ${text}`);
  }
}

// ---------------------------------------------------------------------------
// Main handler
// Vercel doesn't parse the raw body for webhook signature verification,
// so we read it manually.
// ---------------------------------------------------------------------------
export const config = { api: { bodyParser: false } };

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).end('Method not allowed');
  }

  // Read raw body for signature verification
  const rawBody = await new Promise((resolve, reject) => {
    const chunks = [];
    req.on('data', chunk => chunks.push(chunk));
    req.on('end', () => resolve(Buffer.concat(chunks).toString('utf8')));
    req.on('error', reject);
  });

  // Verify signature
  const signature = req.headers['x-razorpay-signature'] || '';
  const secret    = process.env.RAZORPAY_WEBHOOK_SECRET || '';

  if (!verifyWebhookSignature(rawBody, signature, secret)) {
    console.warn('Webhook signature verification failed');
    return res.status(400).json({ error: 'Invalid signature' });
  }

  let event;
  try {
    event = JSON.parse(rawBody);
  } catch {
    return res.status(400).json({ error: 'Invalid JSON' });
  }

  // We only care about payment.captured
  if (event.event !== 'payment.captured') {
    return res.status(200).json({ received: true, handled: false });
  }

  const payment = event.payload?.payment?.entity;
  if (!payment) {
    return res.status(400).json({ error: 'Missing payment entity' });
  }

  const paymentId = payment.id;
  const email     = payment.email || payment.notes?.email || '';
  const name      = payment.notes?.customer_name || '';
  const dob       = payment.notes?.dob || '';
  const mobile    = payment.contact?.replace(/\D/g, '').slice(0, 10) || payment.notes?.mobile || '';
  const amount    = payment.amount;

  console.log(`Webhook: payment.captured ${paymentId} — ${email}`);

  // Save to Supabase (skips silently if browser flow already saved it)
  try {
    await saveOrderToSupabase({ paymentId, name, email, dob, mobile, amount });
  } catch (err) {
    console.error('Webhook Supabase error:', err);
    // Don't return error — still try to send the email
  }

  // Send delivery email if we have an address
  if (email) {
    try {
      await sendDeliveryEmail({ paymentId, name, email, dob, mobile });
    } catch (err) {
      console.error('Webhook email error:', err);
    }
  }

  return res.status(200).json({ received: true, handled: true });
}
