'use strict';

/**
 * Shared Brevo (Sendinblue) transactional email helper.
 *
 * Required env:
 *   BREVO_API_KEY
 *
 * Optional env:
 *   BREVO_FROM_EMAIL  (default: support@namealigned.com)
 *   BREVO_FROM_NAME   (default: NameAligned)
 *   BREVO_REPLY_TO    (default: same as BREVO_FROM_EMAIL)
 */

export function getBrevoSender() {
  const email = (process.env.BREVO_FROM_EMAIL || 'support@namealigned.com').trim();
  const name = (process.env.BREVO_FROM_NAME || 'NameAligned').trim();
  const replyTo = (process.env.BREVO_REPLY_TO || email).trim();
  return { email, name, replyTo };
}

export function isBrevoConfigured() {
  return !!(process.env.BREVO_API_KEY || '').trim();
}

export async function sendBrevoEmail({ to, toName, subject, htmlContent, tags }) {
  const apiKey = (process.env.BREVO_API_KEY || '').trim();
  if (!apiKey) {
    console.error('[brevo] BREVO_API_KEY is not configured');
    return { ok: false, error: 'missing_api_key' };
  }

  const sender = getBrevoSender();
  const payload = {
    sender: { name: sender.name, email: sender.email },
    to: [{ email: String(to).trim(), name: (toName || to || '').trim() || String(to).trim() }],
    subject,
    htmlContent,
  };

  if (sender.replyTo) payload.replyTo = { email: sender.replyTo };
  if (tags && tags.length) payload.tags = tags;

  const response = await fetch('https://api.brevo.com/v3/smtp/email', {
    method: 'POST',
    headers: {
      'api-key': apiKey,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const errorText = await response.text();
    console.error(
      `[brevo] send failed to=${payload.to[0].email} from=${sender.email} [${response.status}]: ${errorText}`
    );
    return { ok: false, status: response.status, error: errorText };
  }

  const data = await response.json().catch(() => null);
  return { ok: true, data };
}
