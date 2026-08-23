'use strict';

/**
 * Build PostgREST headers for Supabase.
 *
 * New opaque keys (sb_secret_* / sb_publishable_*) must go on the `apikey`
 * header only. Sending them as Authorization: Bearer makes PostgREST try to
 * parse them as JWTs and return "Invalid JWT".
 *
 * Legacy JWT keys (service_role / anon) still use both headers.
 */
export function buildSupabaseHeaders(key, extra = {}) {
  const headers = {
    apikey: key,
    ...extra,
  };

  const isOpaqueKey =
    key.startsWith('sb_secret_') || key.startsWith('sb_publishable_');

  if (!isOpaqueKey) {
    headers.Authorization = `Bearer ${key}`;
  }

  return headers;
}
