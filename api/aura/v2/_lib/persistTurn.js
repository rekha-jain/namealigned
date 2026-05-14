/**
 * Persist a single conversational turn (user message + assistant reply)
 * and update the conversation's last_msg_at / message_count.
 *
 * Called async after the SSE stream closes. Errors are logged but never
 * surfaced to the user, since the reply already left the wire.
 */

'use strict';

import { insertInto, updateWhere } from './supabaseAdmin.js';

async function persistTurn({ user, conversation, userText, assistantText, model, latencyMs, intent }) {
  try {
    await insertInto('aura_messages', {
      conversation_id: conversation.id,
      user_id: user.id,
      role: 'user',
      content: String(userText || ''),
      intent_category: intent && intent.category ? intent.category : null,
      intent_subcat:   intent && intent.subcategory ? intent.subcategory : null,
      emotional_tone:  intent && intent.emotionalTone ? intent.emotionalTone : null,
    });
    await insertInto('aura_messages', {
      conversation_id: conversation.id,
      user_id: user.id,
      role: 'assistant',
      content: String(assistantText || ''),
      model_used: model || null,
      latency_ms: latencyMs || null,
    });
    await updateWhere('aura_conversations', {
      last_msg_at: new Date().toISOString(),
      message_count: (Number(conversation.message_count || 0) + 2),
    }, ['id=eq.' + conversation.id]);
    await updateWhere('aura_users', {
      total_messages: (Number(user.total_messages || 0) + 1),
      last_seen_at: new Date().toISOString(),
    }, ['id=eq.' + user.id]);
  } catch (err) {
    console.error('[aura/persistTurn] failed:', err && err.message);
  }
}

export { persistTurn };
