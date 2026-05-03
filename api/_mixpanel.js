/**
 * Server-side Mixpanel tracking via raw HTTP (no npm dep).
 *
 * Required env on Vercel:
 *   MIXPANEL_TOKEN   — same public project token used in assets/mixpanel.js
 *   MIXPANEL_SECRET  — project secret (used for the import API; safer auth)
 *
 * Server events use the /import endpoint so they don't get rate-limited like
 * /track and so they survive client-side ad-blockers. distinct_id should be
 * the user's email (or paymentId if email isn't available) so server events
 * merge with the client identity set by mixpanel.identify(email).
 */
'use strict';

const MIXPANEL_IMPORT_URL = 'https://api.mixpanel.com/import?strict=1';

function getCreds() {
  const token  = process.env.MIXPANEL_TOKEN  || '';
  const secret = process.env.MIXPANEL_SECRET || '';
  if (!token || !secret) {
    return null; // silent no-op if not configured (dev environments)
  }
  return { token, secret };
}

/**
 * Fire a single Mixpanel event server-side.
 * @param {string} eventName
 * @param {string} distinctId  email preferred; falls back to paymentId
 * @param {object} props
 */
export async function mpTrack(eventName, distinctId, props = {}) {
  const creds = getCreds();
  if (!creds) {
    console.warn(`[mixpanel] skipping "${eventName}" — MIXPANEL_TOKEN/SECRET not set`);
    return { skipped: true };
  }
  if (!distinctId) {
    console.warn(`[mixpanel] skipping "${eventName}" — no distinct_id`);
    return { skipped: true };
  }

  const payload = [{
    event: eventName,
    properties: {
      token: creds.token,
      distinct_id: String(distinctId),
      time: Math.floor(Date.now() / 1000),
      $insert_id: `${distinctId}-${eventName}-${Date.now()}`, // dedupe key
      source: 'server',
      ...props,
    },
  }];

  try {
    const auth = Buffer.from(`${creds.secret}:`).toString('base64');
    const res  = await fetch(MIXPANEL_IMPORT_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Basic ${auth}`,
      },
      body: JSON.stringify(payload),
    });

    if (!res.ok) {
      const body = await res.text();
      console.error(`[mixpanel] track "${eventName}" failed status=${res.status} body=${body}`);
      return { ok: false, status: res.status };
    }

    console.log(`[mixpanel] tracked "${eventName}" distinct_id=${distinctId}`);
    return { ok: true };
  } catch (err) {
    console.error(`[mixpanel] track "${eventName}" threw:`, err);
    return { ok: false, error: err.message };
  }
}

/**
 * Set people-properties on a profile (used after Lead Created).
 */
export async function mpSetPeople(distinctId, props = {}) {
  const creds = getCreds();
  if (!creds || !distinctId) return { skipped: true };

  const payload = [{
    $token: creds.token,
    $distinct_id: String(distinctId),
    $set: { $email: distinctId, ...props },
  }];

  try {
    const res = await fetch('https://api.mixpanel.com/engage', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    if (!res.ok) {
      console.error(`[mixpanel] people.set failed status=${res.status} body=${await res.text()}`);
    }
    return { ok: res.ok };
  } catch (err) {
    console.error('[mixpanel] people.set threw:', err);
    return { ok: false, error: err.message };
  }
}
