/**
 * Vercel Serverless Function — POST /api/generate-report
 *
 * Verifies a Razorpay payment, saves the order to Supabase, and sends a
 * delivery email via Brevo containing the link to the full paid report.
 *
 * Required environment variables:
 *   SUPABASE_URL        — e.g. https://xyzxyz.supabase.co
 *   SUPABASE_ANON_KEY   — Supabase project anon/public key
 *   BREVO_API_KEY       — Brevo (Sendinblue) v3 API key
 *   RAZORPAY_KEY_ID     — Razorpay live/test key ID
 *   RAZORPAY_KEY_SECRET — Razorpay live/test key secret
 */

'use strict';

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
// Helper: verify payment with Razorpay REST API
// ---------------------------------------------------------------------------
async function verifyRazorpayPayment(paymentId) {
  if (!paymentId || typeof paymentId !== 'string') {
    throw new TypeError('paymentId must be a non-empty string');
  }

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
  paymentId, name, email, dob, birthNum, destNum, nameNum,
}) {
  const url = `${process.env.SUPABASE_URL}/rest/v1/orders`;

  const response = await fetch(url, {
    method: 'POST',
    headers: {
      apikey: process.env.SUPABASE_ANON_KEY,
      Authorization: `Bearer ${process.env.SUPABASE_ANON_KEY}`,
      'Content-Type': 'application/json',
      Prefer: 'return=representation',
    },
    body: JSON.stringify({
      payment_id: paymentId,
      name,
      email,
      dob: dob || null,
      birth_num: birthNum ?? null,
      dest_num: destNum ?? null,
      name_num: nameNum ?? null,
      created_at: new Date().toISOString(),
    }),
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Supabase orders insert failed [${response.status}]: ${errorText}`);
  }

  const rows = await response.json();
  return Array.isArray(rows) ? rows[0] : rows;
}

// ---------------------------------------------------------------------------
// Helper: send report delivery email via Brevo
// ---------------------------------------------------------------------------
async function sendReportEmail({ paymentId, name, email, dob, birthNum, destNum, nameNum }) {
  const reportUrl =
    `https://namealigned.com/generate-report.html` +
    `?paymentId=${encodeURIComponent(paymentId || '')}` +
    `&name=${encodeURIComponent(name || '')}` +
    `&dob=${encodeURIComponent(dob || '')}` +
    `&email=${encodeURIComponent(email || '')}` +
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
                          &nbsp;&nbsp;${escapeHtml(String(birthNum ?? '—'))}
                        </td>
                      </tr>
                      <tr>
                        <td style="padding:4px 0;font-size:14px;color:#374151;
                                   font-family:Arial,sans-serif;">
                          Bhagyank (Destiny Number)
                        </td>
                        <td style="padding:4px 0;font-size:18px;font-weight:bold;
                                   color:#1a0533;font-family:Arial,sans-serif;">
                          &nbsp;&nbsp;${escapeHtml(String(destNum ?? '—'))}
                        </td>
                      </tr>
                      <tr>
                        <td style="padding:4px 0;font-size:14px;color:#374151;
                                   font-family:Arial,sans-serif;">
                          Name Number (Namank)
                        </td>
                        <td style="padding:4px 0;font-size:18px;font-weight:bold;
                                   color:#1a0533;font-family:Arial,sans-serif;">
                          &nbsp;&nbsp;${escapeHtml(String(nameNum ?? '—'))}
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
                insights, and personalised guidance for 2025–2026 — crafted using the
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
                © ${new Date().getFullYear()} NameAligned.com — All rights reserved.
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
      sender: { name: 'NameAligned.com', email: 'hello@namealigned.com' },
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
// Tiny HTML escaper — prevents XSS in the email template
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
    const { paymentId, name, dob, email, birthNum, destNum, nameNum } =
      req.body || {};

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

    // --- Verify payment with Razorpay ---
    let payment;
    try {
      payment = await verifyRazorpayPayment(cleanPaymentId);
    } catch (rzpErr) {
      console.error('Razorpay fetch error:', rzpErr);
      return sendJSON(res, 402, {
        success: false,
        verified: false,
        error: 'Unable to verify payment. Please try again or contact support.',
      });
    }

    // Validate payment status and amount
    if (payment.status !== 'captured') {
      console.warn(`Payment ${cleanPaymentId} has status "${payment.status}" — expected "captured"`);
      return sendJSON(res, 402, {
        success: false,
        verified: false,
        error: `Payment not captured (status: ${payment.status})`,
      });
    }

    if (payment.amount !== EXPECTED_AMOUNT_PAISE) {
      console.warn(
        `Payment ${cleanPaymentId} amount mismatch: got ${payment.amount}, expected ${EXPECTED_AMOUNT_PAISE}`
      );
      return sendJSON(res, 402, {
        success: false,
        verified: false,
        error: 'Payment amount does not match the expected value',
      });
    }

    // --- Save order to Supabase ---
    try {
      await saveOrderToSupabase({
        paymentId: cleanPaymentId,
        name: cleanName,
        email: cleanEmail,
        dob: dob || null,
        birthNum: birthNum ?? null,
        destNum: destNum ?? null,
        nameNum: nameNum ?? null,
      });
    } catch (dbErr) {
      console.error('Supabase order save error:', dbErr);
      // Payment is verified — still send the email and return success so the
      // user gets their report, but log the DB failure for investigation.
    }

    // --- Send delivery email (best-effort) ---
    try {
      await sendReportEmail({
        paymentId: cleanPaymentId,
        name: cleanName,
        email: cleanEmail,
        dob: dob || '',
        birthNum,
        destNum,
        nameNum,
      });
    } catch (emailErr) {
      console.error('Brevo unexpected error in generate-report:', emailErr);
    }

    return sendJSON(res, 200, { success: true, verified: true });
  } catch (err) {
    console.error('Unhandled error in generate-report:', err);
    return sendJSON(res, 500, { success: false, error: 'Internal server error' });
  }
}
