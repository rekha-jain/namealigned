/**
 * Session loading. Resolves the caller to an aura_users row (creating
 * one if needed), then loads or creates the active conversation and
 * the last N messages for context.
 *
 * Anonymous-only in Phase A. When Supabase Auth is wired we add an
 * authed-JWT path.
 */

'use strict';

import { selectFrom, insertInto, updateWhere } from './supabaseAdmin.js';
import { mintAnonToken, verifyAnonToken } from './anonToken.js';

const HISTORY_LIMIT = 8;

/**
 * Resolve the caller. Headers consulted:
 *   x-aura-anon: <signed token>
 * If absent or invalid, mint a new anon user.
 *
 * Returns { user, anonToken } where anonToken is non-null only when
 * we minted a fresh one (so the client can persist it).
 */
async function resolveUser(req) {
  const headerToken = req.headers && (req.headers['x-aura-anon'] || req.headers['X-Aura-Anon']);
  let user = null;
  let mintedToken = null;

  if (headerToken) {
    const payload = verifyAnonToken(headerToken);
    if (payload && payload.uid) {
      user = await selectFrom('aura_users', {
        filters: ['id=eq.' + payload.uid],
        single: true,
      }).catch(() => null);
      if (user) {
        // Touch last_seen, ignore errors.
        updateWhere('aura_users', { last_seen_at: new Date().toISOString() }, ['id=eq.' + user.id])
          .catch(() => {});
      }
    }
  }

  if (!user) {
    user = await insertInto('aura_users', {
      profile: {},
      subscription_tier: 'free',
    });
    mintedToken = mintAnonToken(user.id);
    // Store the token for future verification consistency (not strictly required).
    updateWhere('aura_users', { anonymous_token: mintedToken }, ['id=eq.' + user.id])
      .catch(() => {});
  }

  return { user, anonToken: mintedToken };
}

/**
 * Load or create the active conversation for the user.
 * If conversationId is provided and belongs to user, use it. Otherwise
 * create a new one.
 */
async function loadOrCreateConversation(userId, conversationId) {
  if (conversationId) {
    const found = await selectFrom('aura_conversations', {
      filters: ['id=eq.' + conversationId, 'user_id=eq.' + userId],
      single: true,
    }).catch(() => null);
    if (found) return found;
  }
  return insertInto('aura_conversations', {
    user_id: userId,
    title: null,
  });
}

/**
 * Load the most recent N messages for a conversation, oldest first.
 */
async function recentMessages(conversationId, limit = HISTORY_LIMIT) {
  const rows = await selectFrom('aura_messages', {
    filters: ['conversation_id=eq.' + conversationId],
    columns: 'role,content,created_at',
    order: 'created_at.desc',
    limit,
  }).catch(() => []);
  return (rows || []).slice().reverse();
}

async function loadSession(req, body) {
  const { user, anonToken } = await resolveUser(req);
  const conversation = await loadOrCreateConversation(user.id, body.conversationId);
  const history = await recentMessages(conversation.id, HISTORY_LIMIT);
  return { user, conversation, history, anonToken };
}

export { loadSession, resolveUser, loadOrCreateConversation, recentMessages };
