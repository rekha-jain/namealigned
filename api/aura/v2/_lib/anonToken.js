/**
 * HMAC-signed anonymous tokens. Stored in browser localStorage as
 * `aura_anon`. Lets us identify a returning anonymous visitor without
 * any account. When the user signs up later, we link the anon row to
 * their auth.users row in aura_users.auth_user_id.
 *
 * Token format: base64url(JSON payload) + "." + base64url(HMAC-SHA256(payload))
 * Payload: { uid, iat, exp, aud:'aura-anon' }
 *
 * Secret: env AURA_ANON_SECRET (any 32+ char random string).
 */

'use strict';

import crypto from 'node:crypto';

const SECRET = process.env.AURA_ANON_SECRET || '';
const DEFAULT_TTL_DAYS = 365;

function b64url(buf) {
  return Buffer.from(buf).toString('base64')
    .replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}
function b64urlDecode(str) {
  const pad = str.length % 4 === 0 ? '' : '='.repeat(4 - (str.length % 4));
  return Buffer.from(String(str).replace(/-/g, '+').replace(/_/g, '/') + pad, 'base64');
}
function hmac(payloadB64) {
  return b64url(crypto.createHmac('sha256', SECRET).update(payloadB64).digest());
}

function mintAnonToken(userId, ttlDays) {
  if (!SECRET) throw Object.assign(new Error('AURA_ANON_SECRET not set'), { code: 'no_secret' });
  const now  = Math.floor(Date.now() / 1000);
  const days = Number(ttlDays || DEFAULT_TTL_DAYS);
  const payload = { uid: userId, iat: now, exp: now + days * 86400, aud: 'aura-anon' };
  const p = b64url(JSON.stringify(payload));
  return p + '.' + hmac(p);
}

function verifyAnonToken(token) {
  if (!SECRET) return null;
  if (!token || typeof token !== 'string') return null;
  const dot = token.indexOf('.');
  if (dot < 1) return null;
  const p = token.slice(0, dot);
  const sig = token.slice(dot + 1);
  const expected = hmac(p);
  // constant-time compare
  if (sig.length !== expected.length) return null;
  let diff = 0;
  for (let i = 0; i < sig.length; i++) diff |= sig.charCodeAt(i) ^ expected.charCodeAt(i);
  if (diff !== 0) return null;
  let payload;
  try { payload = JSON.parse(b64urlDecode(p).toString('utf8')); } catch { return null; }
  if (!payload || payload.aud !== 'aura-anon') return null;
  if (typeof payload.exp === 'number' && payload.exp < Math.floor(Date.now() / 1000)) return null;
  if (!payload.uid || typeof payload.uid !== 'string') return null;
  return payload;
}

export { mintAnonToken, verifyAnonToken };
