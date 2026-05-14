/**
 * Global Gemini free-tier daily quota gate.
 * One row per (date, model_family). Atomic increment in Postgres.
 * Resets at midnight US Pacific (Gemini's reset boundary).
 */

'use strict';

import { rpc } from './supabaseAdmin.js';

const QUOTA_TZ = 'America/Los_Angeles';

function ptDate() {
  // en-CA gives YYYY-MM-DD
  return new Intl.DateTimeFormat('en-CA', { timeZone: QUOTA_TZ }).format(new Date());
}

/**
 * Reserve one Gemini call against the global daily quota.
 * Returns:
 *   { ok: true,  count, cap }     proceed
 *   { ok: false, count, cap }     quota exhausted, do not call Gemini
 *
 * Fails open on infra errors (better to serve than to error out).
 */
async function reserveQuota() {
  try {
    const result = await rpc('inc_aura_daily_quota', {
      p_date: ptDate(),
      p_model: 'gemini_free',
    });
    // RPC returns an array of rows.
    const row = Array.isArray(result) ? result[0] : result;
    if (!row) return { ok: true, count: 0, cap: 0 };
    const count = Number(row.call_count || 0);
    const cap   = Number(row.cap || 0);
    if (count > cap) return { ok: false, count, cap };
    return { ok: true, count, cap };
  } catch (err) {
    // Fail open. Quota infra outage should not block users.
    console.error('[aura/quota] reserve failed, failing open:', err && err.message);
    return { ok: true, count: 0, cap: 0, soft: true };
  }
}

/**
 * The next reset time, in IST string form, for the resting message.
 * Gemini resets at midnight PT, which is ~12:30 PM IST.
 */
function nextResetIST() {
  // Static label; Gemini's free-quota reset is at 12:30 PM IST give or take
  // a few minutes through the year (DST shifts).
  return '12:30 PM IST';
}

const AURA_RESTING_MESSAGE =
  "Aura is resting tonight. The day has been full of questions, and the well needs to refill. " +
  "Come back tomorrow, sometimes the answer arrives clearer with a night between. ✨\n\n" +
  "Aura returns at " + nextResetIST() + ".";

export { reserveQuota, AURA_RESTING_MESSAGE, nextResetIST };
