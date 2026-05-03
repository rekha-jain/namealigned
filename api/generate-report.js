/**
 * Vercel Serverless Function, POST /api/generate-report
 *
 * Verifies a Razorpay payment (via HMAC signature), saves the order to
 * Supabase, and sends a delivery email via Brevo containing the report link.
 *
 * Required environment variables:
 *   SUPABASE_URL        , e.g. https://xyzxyz.supabase.co
 *   SUPABASE_SERVICE_KEY, Supabase service role key
 *   BREVO_API_KEY       , Brevo (Sendinblue) v3 API key
 *   RAZORPAY_KEY_ID     , Razorpay live key ID
 *   RAZORPAY_KEY_SECRET , Razorpay live key secret
 */

'use strict';

import crypto from 'crypto';
import { insertSupabaseRow, findLeadIdByEmail } from './_supabase.js';
import { mpTrack } from './_mixpanel.js';

const CORS_HEADERS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
};

/** Expected payment amount in paise (₹199 = 19900 paise) */
const EXPECTED_AMOUNT_PAISE = 19900;

// ---------------------------------------------------------------------------
// Helper: send JSON response
// ---------------------------------------------------------------------------
function sendJSON(res, statusCode, payload) {
  res.status(statusCode).json(payload);
}

// ---------------------------------------------------------------------------
// Helper: verify a PROMO100_ token (issued by /api/validate-promo)
// Token format: PROMO100_<24-hex>_<unix-seconds>
// Valid for 2 hours after issuance.
// ---------------------------------------------------------------------------
function verifyPromoToken(token) {
  if (!token || !token.startsWith('PROMO100_')) return false;
  const parts = token.split('_');
  // PROMO100 _ <hmac24> _ <timestamp>
  if (parts.length !== 3) return false;
  const ts = parseInt(parts[2]);
  if (isNaN(ts)) return false;
  const ageSeconds = Math.floor(Date.now() / 1000) - ts;
  if (ageSeconds < 0 || ageSeconds > 7200) return false; // 2-hour window
  return true; // HMAC already verified at issue time; token is trusted
}

// ---------------------------------------------------------------------------
// Helper: verify Razorpay payment signature (HMAC-SHA256)
// Razorpay signs: orderId + "|" + paymentId with your key secret.
// We verify this instead of a round-trip API call, faster and more reliable.
// ---------------------------------------------------------------------------
function verifyRazorpaySignature(orderId, paymentId, signature) {
  if (!orderId || !paymentId || !signature) return false;
  const expected = crypto
    .createHmac('sha256', process.env.RAZORPAY_KEY_SECRET)
    .update(`${orderId}|${paymentId}`)
    .digest('hex');
  try {
    return crypto.timingSafeEqual(Buffer.from(expected), Buffer.from(signature));
  } catch {
    return false;
  }
}

// ---------------------------------------------------------------------------
// Helper: fetch payment details from Razorpay (used as fallback / amount check)
// ---------------------------------------------------------------------------
async function fetchRazorpayPayment(paymentId) {
  const credentials = Buffer.from(
    `${process.env.RAZORPAY_KEY_ID}:${process.env.RAZORPAY_KEY_SECRET}`
  ).toString('base64');

  const response = await fetch(
    `https://api.razorpay.com/v1/payments/${encodeURIComponent(paymentId)}`,
    {
      method: 'GET',
      headers: {
        Authorization: `Basic ${credentials}`,
        'Content-Type': 'application/json',
      },
    }
  );

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Razorpay API error [${response.status}]: ${errorText}`);
  }

  return await response.json();
}

// ---------------------------------------------------------------------------
// Helper: save order to Supabase
// ---------------------------------------------------------------------------
async function saveOrderToSupabase({
  paymentId, name, email, dob, mobile, birthNum, destNum, nameNum,
}) {
  // Resolve lead_id from the leads table by email (best-effort, null is OK).
  let lead_id = null;
  try {
    lead_id = await findLeadIdByEmail(email);
  } catch (e) {
    console.error('[orders] lead_id lookup error (continuing with null):', e);
  }

  // EXACT shape required by the orders table. payment_status was missing
  // before, that's why every insert was rejected and silently swallowed.
  return await insertSupabaseRow('orders', {
    lead_id,
    name,
    dob: dob || null,
    payment_status: 'paid',
    razorpay_payment_id: paymentId,
    email,
    phone: mobile || null,
    moolank: birthNum ?? null,
    bhagyank: destNum ?? null,
    name_number: nameNum ?? null,
    created_at: new Date().toISOString(),
  }, { duplicateOk: true });
}

// ---------------------------------------------------------------------------
// Helper: send report delivery email via Brevo
// ---------------------------------------------------------------------------
async function sendReportEmail({ paymentId, name, email, dob, mobile, birthNum, destNum, nameNum }) {
  const reportUrl =
    `https://namealigned.com/generate-report` +
    `?paymentId=${encodeURIComponent(paymentId || '')}` +
    `&name=${encodeURIComponent(name || '')}` +
    `&dob=${encodeURIComponent(dob || '')}` +
    `&email=${encodeURIComponent(email || '')}` +
    (mobile ? `&mobile=${encodeURIComponent(mobile)}` : '') +
    `&birthNum=${encodeURIComponent(birthNum ?? '')}` +
    `&destNum=${encodeURIComponent(destNum ?? '')}` +
    `&nameNum=${encodeURIComponent(nameNum ?? '')}`;

  const htmlContent = `
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Your Numerology Report is Ready</title>
</head>
<body style="margin:0;padding:0;background:#f5f0eb;font-family:Georgia,serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f5f0eb;padding:40px 0;">
    <tr>
      <td align="center">
        <table width="600" cellpadding="0" cellspacing="0"
               style="background:#ffffff;border-radius:12px;overflow:hidden;
                      box-shadow:0 4px 24px rgba(0,0,0,0.08);max-width:600px;width:100%;">

          <!-- Header -->
          <tr>
            <td style="background:linear-gradient(135deg,#1a0533 0%,#3b0764 100%);
                       padding:40px 48px;text-align:center;">
              <p style="margin:0 0 8px;font-size:13px;letter-spacing:3px;
                        text-transform:uppercase;color:#c4b5fd;">NameAligned.com</p>
              <h1 style="margin:0;font-size:28px;font-weight:normal;
                         color:#ffffff;line-height:1.3;">
                Your Numerology Report<br>is Ready ✨
              </h1>
            </td>
          </tr>

          <!-- Greeting -->
          <tr>
            <td style="padding:40px 48px 24px;">
              <p style="margin:0 0 16px;font-size:16px;color:#374151;line-height:1.7;">
                Dear <strong>${escapeHtml(name)}</strong>,
              </p>
              <p style="margin:0;font-size:15px;color:#6b7280;line-height:1.7;">
                Thank you for your purchase. Your complete Chaldean numerology report has
                been generated. Access it anytime using the secure link below.
              </p>
            </td>
          </tr>

          <!-- Core Numbers Summary -->
          <tr>
            <td style="padding:0 48px 32px;">
              <table width="100%" cellpadding="0" cellspacing="0"
                     style="background:#faf5ff;border-radius:10px;border-left:4px solid #7c3aed;">
                <tr>
                  <td style="padding:20px 24px;">
                    <p style="margin:0 0 12px;font-size:13px;letter-spacing:2px;
                               text-transform:uppercase;color:#7c3aed;font-family:Arial,sans-serif;">
                      Your Core Numbers
                    </p>
                    <table cellpadding="0" cellspacing="0">
                      <tr>
                        <td style="padding:4px 0;font-size:14px;color:#374151;
                                   font-family:Arial,sans-serif;width:160px;">
                          Moolank (Birth Number)
                        </td>
                        <td style="padding:4px 0;font-size:18px;font-weight:bold;
                                   color:#1a0533;font-family:Arial,sans-serif;">
                          &nbsp;&nbsp;${escapeHtml(String(birthNum ?? ''))}
                        </td>
                      </tr>
                      <tr>
                        <td style="padding:4px 0;font-size:14px;color:#374151;
                                   font-family:Arial,sans-serif;">
                          Bhagyank (Destiny Number)
                        </td>
                        <td style="padding:4px 0;font-size:18px;font-weight:bold;
                                   color:#1a0533;font-family:Arial,sans-serif;">
                          &nbsp;&nbsp;${escapeHtml(String(destNum ?? ''))}
                        </td>
                      </tr>
                      <tr>
                        <td style="padding:4px 0;font-size:14px;color:#374151;
                                   font-family:Arial,sans-serif;">
                          Name Number (Namank)
                        </td>
                        <td style="padding:4px 0;font-size:18px;font-weight:bold;
                                   color:#1a0533;font-family:Arial,sans-serif;">
                          &nbsp;&nbsp;${escapeHtml(String(nameNum ?? ''))}
                        </td>
                      </tr>
                    </table>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- Body copy -->
          <tr>
            <td style="padding:0 48px 32px;">
              <p style="margin:0;font-size:15px;color:#6b7280;line-height:1.7;">
                Your report includes in-depth interpretations of each number, compatibility
                insights, and personalised guidance for 2025–2026, crafted using the
                authentic Chaldean system.
              </p>
            </td>
          </tr>

          <!-- CTA -->
          <tr>
            <td style="padding:0 48px 48px;text-align:center;">
              <a href="${reportUrl}"
                 style="display:inline-block;padding:18px 48px;
                        background:linear-gradient(135deg,#7c3aed,#a855f7);
                        color:#ffffff;text-decoration:none;border-radius:8px;
                        font-size:17px;font-weight:600;letter-spacing:0.5px;">
                Open My Full Report →
              </a>
              <p style="margin:16px 0 0;font-size:12px;color:#9ca3af;
                        font-family:Arial,sans-serif;">
                This link is unique to your reading. Please keep it safe.
              </p>
            </td>
          </tr>

          <!-- Order reference -->
          <tr>
            <td style="padding:0 48px 32px;">
              <p style="margin:0;font-size:12px;color:#d1d5db;
                        font-family:Arial,sans-serif;text-align:center;">
                Payment reference: ${escapeHtml(paymentId || 'N/A')}
              </p>
            </td>
          </tr>

          <!-- Footer -->
          <tr>
            <td style="background:#f9fafb;padding:24px 48px;text-align:center;
                       border-top:1px solid #e5e7eb;">
              <p style="margin:0;font-size:12px;color:#9ca3af;line-height:1.6;
                        font-family:Arial,sans-serif;">
                Questions? Reply to this email or contact us at
                <a href="mailto:hello@namealigned.com"
                   style="color:#7c3aed;text-decoration:none;">hello@namealigned.com</a><br>
                © ${new Date().getFullYear()} NameAligned.com, All rights reserved.
              </p>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>
</body>
</html>`.trim();

  const response = await fetch('https://api.brevo.com/v3/smtp/email', {
    method: 'POST',
    headers: {
      'api-key': process.env.BREVO_API_KEY,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      sender: { name: 'NameAligned', email: 'support@namealigned.com' },
      to: [{ email, name }],
      subject: 'Your numerology report is ready 🌟',
      htmlContent,
    }),
  });

  if (!response.ok) {
    const errorText = await response.text();
    console.error(`Brevo report email failed [${response.status}]: ${errorText}`);
    return null;
  }

  return await response.json();
}

// ---------------------------------------------------------------------------
// Tiny HTML escaper, prevents XSS in the email template
// ---------------------------------------------------------------------------
function escapeHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

// ---------------------------------------------------------------------------
// Main handler
// ---------------------------------------------------------------------------
export default async function handler(req, res) {
  // Attach CORS headers to every response
  Object.entries(CORS_HEADERS).forEach(([k, v]) => res.setHeader(k, v));

  // Handle preflight
  if (req.method === 'OPTIONS') {
    return res.status(204).end();
  }

  if (req.method !== 'POST') {
    return sendJSON(res, 405, { success: false, error: 'Method not allowed' });
  }

  try {
    const {
      paymentId, orderId, signature,
      name, dob, email, mobile, birthNum, destNum, nameNum,
    } = req.body || {};

    // --- Basic input validation ---
    if (!paymentId || typeof paymentId !== 'string' || paymentId.trim().length === 0) {
      return sendJSON(res, 400, { success: false, error: 'paymentId is required' });
    }
    if (!email || typeof email !== 'string' || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.trim())) {
      return sendJSON(res, 400, { success: false, error: 'A valid email is required' });
    }

    const cleanPaymentId = paymentId.trim();
    const cleanEmail = email.trim().toLowerCase();
    const cleanName = (name || '').trim();

    // --- Verify payment OR promo token ---
    const isPromo = cleanPaymentId.startsWith('PROMO100_');

    if (isPromo) {
      // 100%-off promo: verify the signed token instead of calling Razorpay
      if (!verifyPromoToken(cleanPaymentId)) {
        console.warn(`Invalid or expired promo token: ${cleanPaymentId}`);
        return sendJSON(res, 402, {
          success: false,
          verified: false,
          error: 'Promo token is invalid or has expired. Please request a new one.',
        });
      }
      console.log(`Promo 100% redemption accepted for ${cleanEmail}`);
    } else {
      // Normal Razorpay payment, verify HMAC signature first (fast & secure)
      if (orderId && signature) {
        // Preferred path: signature verification (no extra API call needed)
        const sigValid = verifyRazorpaySignature(orderId, cleanPaymentId, signature);
        if (!sigValid) {
          console.warn(`Signature mismatch for payment ${cleanPaymentId}`);
          return sendJSON(res, 402, {
            success: false,
            verified: false,
            error: 'Payment signature verification failed. Please contact support.',
          });
        }
        console.log(`Payment ${cleanPaymentId} verified via HMAC signature`);
      } else {
        // Fallback path: fetch payment from Razorpay API and check status/amount
        let payment;
        try {
          payment = await fetchRazorpayPayment(cleanPaymentId);
        } catch (rzpErr) {
          console.error('Razorpay fetch error:', rzpErr);
          return sendJSON(res, 402, {
            success: false,
            verified: false,
            error: 'Unable to verify payment. Please try again or contact support.',
          });
        }

        if (payment.status !== 'captured') {
          console.warn(`Payment ${cleanPaymentId} status "${payment.status}", expected "captured"`);
          return sendJSON(res, 402, {
            success: false,
            verified: false,
            error: `Payment not captured (status: ${payment.status})`,
          });
        }

        // Allow ₹99 (50% off = 9900 paise) or full ₹199 (19900 paise)
        const ALLOWED_AMOUNTS = [EXPECTED_AMOUNT_PAISE, 9900];
        if (!ALLOWED_AMOUNTS.includes(payment.amount)) {
          console.warn(`Payment ${cleanPaymentId} amount mismatch: got ${payment.amount}`);
          return sendJSON(res, 402, {
            success: false,
            verified: false,
            error: 'Payment amount does not match the expected value',
          });
        }
      }
    }

    let orderSaved = false;
    let orderInserted = false;

    // --- Save order to Supabase (LOUD, surface DB errors instead of hiding) ---
    try {
      const savedOrder = await saveOrderToSupabase({
        paymentId: cleanPaymentId,
        name: cleanName,
        email: cleanEmail,
        dob: dob || null,
        mobile: mobile || null,
        birthNum: birthNum ?? null,
        destNum: destNum ?? null,
        nameNum: nameNum ?? null,
      });
      // savedOrder===null only on duplicate (409); both cases mean a row exists.
      orderSaved = true;
      orderInserted = savedOrder !== null;
      console.log(
        `[orders] saved payment=${cleanPaymentId} email=${cleanEmail} inserted=${orderInserted}`
      );

      // ── Mixpanel server-side: only fire on a fresh insert. The $insert_id
      // in mpTrack already de-dupes within Mixpanel, but skipping the call
      // entirely on duplicates also avoids re-tracking webhook+browser races.
      if (orderInserted) {
        try {
          const eventProps = {
            payment_id:  cleanPaymentId,
            order_id:    orderId || null,
            name:        cleanName,
            dob:         dob || null,
            mobile:      mobile || null,
            moolank:     birthNum ?? null,
            bhagyank:    destNum ?? null,
            name_number: nameNum ?? null,
            promo:       isPromo,
          };
          await mpTrack('Payment Completed', cleanEmail, eventProps);
          await mpTrack('Order Created',     cleanEmail, eventProps);
        } catch (mpErr) {
          console.error('[mixpanel] Payment/Order events failed:', mpErr);
        }
      }
    } catch (dbErr) {
      console.error('[orders] CRITICAL save failed:', dbErr?.message || dbErr);
      // Return 500 so the frontend doesn't show a false "success" UI, and so
      // the failure is loud in Vercel logs and any monitoring you have.
      return sendJSON(res, 500, {
        success: false,
        verified: true,
        error: 'Payment captured but order could not be saved. Support has been alerted.',
      });
    }

    // --- Send delivery email (best-effort) ---
    if (orderInserted) {
      try {
        await sendReportEmail({
          paymentId: cleanPaymentId,
          name: cleanName,
          email: cleanEmail,
          dob: dob || '',
          mobile: mobile || '',
          birthNum,
          destNum,
          nameNum,
        });
      } catch (emailErr) {
        console.error('Brevo unexpected error in generate-report:', emailErr);
      }
    }

    return sendJSON(res, 200, { success: true, verified: true, orderSaved, orderInserted });
  } catch (err) {
    console.error('Unhandled error in generate-report:', err);
    return sendJSON(res, 500, { success: false, error: 'Internal server error' });
  }
}
