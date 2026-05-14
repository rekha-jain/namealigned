/**
 * GET /api/aura/v2/me
 *
 * Returns the caller's user record + quota state. Used by the frontend
 * to render any "Aura is resting" banners or per-user soft limits.
 *
 * Headers:
 *   x-aura-anon: <signed token>   required for now
 */

'use strict';

import { selectFrom } from './_lib/supabaseAdmin.js';
import { verifyAnonToken } from './_lib/anonToken.js';

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, X-Aura-Anon');
  if (req.method === 'OPTIONS') return res.status(204).end();
  if (req.method !== 'GET') return res.status(405).json({ error: 'method_not_allowed' });

  const token = req.headers['x-aura-anon'] || req.headers['X-Aura-Anon'];
  const payload = verifyAnonToken(token);
  if (!payload || !payload.uid) {
    return res.status(401).json({ error: 'no_anon_token' });
  }

  try {
    const user = await selectFrom('aura_users', {
      filters: ['id=eq.' + payload.uid],
      single: true,
    });
    if (!user) return res.status(404).json({ error: 'user_not_found' });
    return res.status(200).json({
      userId: user.id,
      authed: !!user.auth_user_id,
      tier: user.subscription_tier || 'free',
      totalMessages: user.total_messages || 0,
      profile: user.profile || {},
    });
  } catch (err) {
    console.error('[aura/v2/me] failed:', err && err.message);
    return res.status(500).json({ error: 'me_failed' });
  }
}
