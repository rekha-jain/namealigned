/**
 * POST /api/aura/v2/auth/anonymous
 *
 * Mints an anonymous user row + signed token. Client stores the token in
 * localStorage as `aura_anon` and sends it back in the X-Aura-Anon header
 * on every subsequent request.
 *
 * Idempotent-ish: if the caller already has a valid token, we echo it back
 * with the same uid, so refreshes don't fragment identity.
 */

'use strict';

import { insertInto, selectFrom, updateWhere } from '../_lib/supabaseAdmin.js';
import { mintAnonToken, verifyAnonToken } from '../_lib/anonToken.js';

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, X-Aura-Anon');
  if (req.method === 'OPTIONS') return res.status(204).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'method_not_allowed' });

  try {
    const existing = req.headers['x-aura-anon'] || req.headers['X-Aura-Anon'];
    if (existing) {
      const payload = verifyAnonToken(existing);
      if (payload && payload.uid) {
        const user = await selectFrom('aura_users', {
          filters: ['id=eq.' + payload.uid],
          single: true,
        }).catch(() => null);
        if (user) {
          updateWhere('aura_users', { last_seen_at: new Date().toISOString() }, ['id=eq.' + user.id])
            .catch(() => {});
          return res.status(200).json({ userId: user.id, anonToken: existing, reused: true });
        }
      }
    }

    const user = await insertInto('aura_users', {
      profile: {},
      subscription_tier: 'free',
    });
    const token = mintAnonToken(user.id);
    updateWhere('aura_users', { anonymous_token: token }, ['id=eq.' + user.id]).catch(() => {});
    return res.status(200).json({ userId: user.id, anonToken: token, reused: false });
  } catch (err) {
    console.error('[aura/v2/auth/anonymous] failed:', err && err.message, err && err.body);
    return res.status(500).json({ error: 'auth_failed', detail: String(err && err.message || err) });
  }
}
