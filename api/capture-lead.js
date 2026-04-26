/**
 * Vercel Serverless Function — POST /api/capture-lead
 *
 * Receives a lead from the free numerology tool, persists it to Supabase,
 * and sends a branded transactional email via Brevo.
 *
 * Required environment variables:
 *   SUPABASE_URL      — e.g. https://xyzxyz.supabase.co
 *   SUPABASE_ANON_KEY — Supabase project anon/public key
 *   BREVO_API_KEY     — Brevo (Sendinblue) v3 API key
 */

'use strict';

const CORS_HEADERS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
};

// ---------------------------------------------------------------------------
// Helper: send JSON response
// ---------------------------------------------------------------------------
function sendJSON(res, statusCode, payload) {
  res.status(statusCode).json(payload);
}

// ---------------------------------------------------------------------------
// Helper: insert lead row into Supabase
// ---------------------------------------------------------------------------
async function saveLeadToSupabase({ name, dob, email, mobile, birthNum, destNum, nameNum, pct, source }) {
  const url = `${process.env.SUPABASE_URL}/rest/v1/leads`;

  const response = await fetch(url, {
    method: 'POST',
    headers: {
      apikey: process.env.SUPABASE_SERVICE_KEY,
      Authorization: `Bearer ${process.env.SUPABASE_SERVICE_KEY}`,
      'Content-Type': 'application/json',
      Prefer: 'return=representation',
    },
    body: JSON.stringify({
      name,
      dob,
      email,
      phone: mobile || null,
      moolank: birthNum ?? null,
      bhagyank: destNum ?? null,
      name_number: nameNum ?? null,
      alignment_score: pct ?? null,
      created_at: new Date().toISOString(),
    }),
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Supabase insert failed [${response.status}]: ${errorText}`);
  }

  const rows = await response.json();
  return Array.isArray(rows) ? rows[0] : rows;
}

// ---------------------------------------------------------------------------
// Helper: send Brevo transactional email
// ---------------------------------------------------------------------------
async function sendBrevoEmail({ name, dob, email, birthNum, destNum, nameNum }) {
  const analyserUrl =
    `https://namealigned.com/analyzer.html` +
    `?name=${encodeURIComponent(name || '')}` +
    `&dob=${encodeURIComponent(dob || '')}`;

  const paidReportUrl =
    `https://namealigned.com/report.html` +
    `?name=${encodeURIComponent(name || '')}` +
    `&dob=${encodeURIComponent(dob || '')}`;

  const htmlContent = `
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Your Free Chaldean Numerology Analysis</title>
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
              <h1 style="margin:0;font-size:28px;font-weight:normal;color:#ffffff;
                         line-height:1.3;">Your Free Chaldean<br>Numerology Analysis</h1>
            </td>
          </tr>

          <!-- Greeting -->
          <tr>
            <td style="padding:40px 48px 24px;">
              <p style="margin:0 0 16px;font-size:16px;color:#374151;line-height:1.7;">
                Dear <strong>${escapeHtml(name)}</strong>,
              </p>
              <p style="margin:0;font-size:15px;color:#6b7280;line-height:1.7;">
                Your Chaldean numerology reading is ready. Below are your three core numbers,
                each revealing a distinct layer of your life's blueprint.
              </p>
            </td>
          </tr>

          <!-- Core Numbers -->
          <tr>
            <td style="padding:0 48px 32px;">
              <table width="100%" cellpadding="0" cellspacing="0">
                <tr>
                  <!-- Moolank -->
                  <td width="32%" style="text-align:center;padding:24px 16px;
                      background:#faf5ff;border-radius:10px;">
                    <p style="margin:0 0 6px;font-size:11px;letter-spacing:2px;
                               text-transform:uppercase;color:#7c3aed;">Moolank</p>
                    <p style="margin:0 0 4px;font-size:48px;font-weight:bold;
                               color:#1a0533;line-height:1;">${escapeHtml(String(birthNum ?? '—'))}</p>
                    <p style="margin:0;font-size:11px;color:#9ca3af;">Birth Number</p>
                  </td>
                  <td width="2%"></td>
                  <!-- Bhagyank -->
                  <td width="32%" style="text-align:center;padding:24px 16px;
                      background:#faf5ff;border-radius:10px;">
                    <p style="margin:0 0 6px;font-size:11px;letter-spacing:2px;
                               text-transform:uppercase;color:#7c3aed;">Bhagyank</p>
                    <p style="margin:0 0 4px;font-size:48px;font-weight:bold;
                               color:#1a0533;line-height:1;">${escapeHtml(String(destNum ?? '—'))}</p>
                    <p style="margin:0;font-size:11px;color:#9ca3af;">Destiny Number</p>
                  </td>
                  <td width="2%"></td>
                  <!-- Name Number -->
                  <td width="32%" style="text-align:center;padding:24px 16px;
                      background:#faf5ff;border-radius:10px;">
                    <p style="margin:0 0 6px;font-size:11px;letter-spacing:2px;
                               text-transform:uppercase;color:#7c3aed;">Name Number</p>
                    <p style="margin:0 0 4px;font-size:48px;font-weight:bold;
                               color:#1a0533;line-height:1;">${escapeHtml(String(nameNum ?? '—'))}</p>
                    <p style="margin:0;font-size:11px;color:#9ca3af;">Namank</p>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- Body copy -->
          <tr>
            <td style="padding:0 48px 32px;">
              <p style="margin:0;font-size:15px;color:#6b7280;line-height:1.7;">
                Each number carries centuries of Chaldean wisdom. Your full report explains
                how these numbers interact, the opportunities they reveal, and the patterns
                to be aware of in relationships, career, and life timing.
              </p>
            </td>
          </tr>

          <!-- CTA: View free report -->
          <tr>
            <td style="padding:0 48px 16px;text-align:center;">
              <a href="${analyserUrl}"
                 style="display:inline-block;padding:14px 36px;
                        background:linear-gradient(135deg,#7c3aed,#a855f7);
                        color:#ffffff;text-decoration:none;border-radius:8px;
                        font-size:15px;font-weight:600;letter-spacing:0.5px;">
                View Your Free Analysis →
              </a>
            </td>
          </tr>

          <!-- Upgrade divider -->
          <tr>
            <td style="padding:8px 48px 0;text-align:center;">
              <p style="margin:0;font-size:13px;color:#9ca3af;">or</p>
            </td>
          </tr>

          <!-- CTA: Paid report -->
          <tr>
            <td style="padding:12px 48px 16px;text-align:center;">
              <a href="${paidReportUrl}"
                 style="display:inline-block;padding:16px 40px;
                        background:linear-gradient(135deg,#f0b429,#f5d060);
                        color:#1a0533;text-decoration:none;border-radius:8px;
                        font-size:16px;font-weight:700;letter-spacing:0.5px;">
                Get Your 5-Year Destiny Report — ₹199 →
              </a>
            </td>
          </tr>

          <!-- Paid report features -->
          <tr>
            <td style="padding:0 48px 40px;text-align:center;">
              <p style="margin:8px 0 0;font-size:12px;color:#9ca3af;line-height:1.8;">
                ✦ Suggested names with Chaldean scores &nbsp;·&nbsp;
                ✦ 5-year personalised forecast<br>
                ✦ Year-by-year career, love, wealth &amp; health &nbsp;·&nbsp;
                ✦ Mobile number analysis<br>
                ✦ Downloadable PDF — One-time ₹199, instant delivery
              </p>
            </td>
          </tr>

          <!-- Footer -->
          <tr>
            <td style="background:#f9fafb;padding:24px 48px;text-align:center;
                       border-top:1px solid #e5e7eb;">
              <p style="margin:0;font-size:12px;color:#9ca3af;line-height:1.6;">
                You're receiving this because you requested a free numerology reading at
                <a href="https://namealigned.com" style="color:#7c3aed;text-decoration:none;">
                  namealigned.com</a>.<br>
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
      sender: { name: 'NameAligned', email: 'support@namealigned.com' },
      to: [{ email, name }],
      subject: 'Your free Chaldean numerology analysis is ready',
      htmlContent,
    }),
  });

  if (!response.ok) {
    const errorText = await response.text();
    // Non-fatal: log but don't throw — we don't want email failure to fail the lead capture
    console.error(`Brevo email failed [${response.status}]: ${errorText}`);
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
    const { name, dob, email, mobile, birthNum, destNum, nameNum, pct, source } =
      req.body || {};

    // --- Validation ---
    if (!name || typeof name !== 'string' || name.trim().length === 0) {
      return sendJSON(res, 400, { success: false, error: 'name is required' });
    }
    if (!email || typeof email !== 'string' || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.trim())) {
      return sendJSON(res, 400, { success: false, error: 'A valid email is required' });
    }

    const cleanName = name.trim();
    const cleanEmail = email.trim().toLowerCase();

    // --- Persist to Supabase ---
    let savedRow;
    try {
      savedRow = await saveLeadToSupabase({
        name: cleanName,
        dob: dob || null,
        email: cleanEmail,
        mobile: mobile || null,
        birthNum: birthNum ?? null,
        destNum: destNum ?? null,
        nameNum: nameNum ?? null,
        pct: pct ?? null,
        source: source || 'website',
      });
    } catch (dbErr) {
      console.error('Supabase error:', dbErr);
      return sendJSON(res, 500, { success: false, error: 'Failed to save lead' });
    }

    // --- Send welcome email (best-effort) ---
    try {
      await sendBrevoEmail({
        name: cleanName,
        dob: dob || '',
        email: cleanEmail,
        birthNum,
        destNum,
        nameNum,
      });
    } catch (emailErr) {
      // Already logged inside sendBrevoEmail; we still return success
      console.error('Brevo unexpected error:', emailErr);
    }

    return sendJSON(res, 200, {
      success: true,
      id: savedRow?.id ?? null,
    });
  } catch (err) {
    console.error('Unhandled error in capture-lead:', err);
    return sendJSON(res, 500, { success: false, error: 'Internal server error' });
  }
}
