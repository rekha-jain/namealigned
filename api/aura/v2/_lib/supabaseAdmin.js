/**
 * Thin Supabase REST helper. Uses the service role key (server only).
 * Mirrors the raw-fetch pattern already used in api/health-supabase.js,
 * so no new dependency is introduced.
 */

'use strict';

const SUPABASE_URL = (process.env.SUPABASE_URL || '').replace(/\/+$/, '');
const SUPABASE_KEY = process.env.SUPABASE_SERVICE_KEY || '';

function ensureConfigured() {
  if (!SUPABASE_URL || !SUPABASE_KEY) {
    const err = new Error('supabase_not_configured');
    err.code = 'supabase_not_configured';
    throw err;
  }
}

function baseHeaders(extra) {
  return Object.assign({
    apikey: SUPABASE_KEY,
    Authorization: 'Bearer ' + SUPABASE_KEY,
    'Content-Type': 'application/json',
  }, extra || {});
}

/**
 * Run a PostgREST select. Returns the parsed body (array or single object).
 * Options:
 *   single   true => use Accept: application/vnd.pgrst.object+json
 *   columns  string of columns; defaults to '*'
 *   filters  array of "col=eq.val" style PostgREST filter strings
 *   order    e.g. 'created_at.desc'
 *   limit    integer
 */
async function selectFrom(table, options) {
  ensureConfigured();
  options = options || {};
  const params = new URLSearchParams();
  params.set('select', options.columns || '*');
  (options.filters || []).forEach(f => {
    const i = f.indexOf('=');
    if (i > 0) params.append(f.slice(0, i), f.slice(i + 1));
  });
  if (options.order) params.set('order', options.order);
  if (options.limit) params.set('limit', String(options.limit));

  const url = SUPABASE_URL + '/rest/v1/' + table + '?' + params.toString();
  const headers = baseHeaders(options.single ? { Accept: 'application/vnd.pgrst.object+json' } : {});
  const r = await fetch(url, { headers });
  if (r.status === 406 && options.single) return null; // PGRST "no rows" with single
  if (!r.ok) {
    const body = await r.text().catch(() => '');
    throw Object.assign(new Error('select_failed'), { status: r.status, body });
  }
  if (r.status === 204) return options.single ? null : [];
  return r.json();
}

/**
 * Insert a row, returning the inserted row (Prefer: return=representation).
 */
async function insertInto(table, row) {
  ensureConfigured();
  const url = SUPABASE_URL + '/rest/v1/' + table;
  const r = await fetch(url, {
    method: 'POST',
    headers: baseHeaders({ Prefer: 'return=representation' }),
    body: JSON.stringify(row),
  });
  if (!r.ok) {
    const body = await r.text().catch(() => '');
    throw Object.assign(new Error('insert_failed'), { status: r.status, body });
  }
  const data = await r.json();
  return Array.isArray(data) ? data[0] : data;
}

/**
 * Update rows matching `filters`. Returns updated rows.
 */
async function updateWhere(table, patch, filters) {
  ensureConfigured();
  const params = new URLSearchParams();
  (filters || []).forEach(f => {
    const i = f.indexOf('=');
    if (i > 0) params.append(f.slice(0, i), f.slice(i + 1));
  });
  const url = SUPABASE_URL + '/rest/v1/' + table + '?' + params.toString();
  const r = await fetch(url, {
    method: 'PATCH',
    headers: baseHeaders({ Prefer: 'return=representation' }),
    body: JSON.stringify(patch),
  });
  if (!r.ok) {
    const body = await r.text().catch(() => '');
    throw Object.assign(new Error('update_failed'), { status: r.status, body });
  }
  return r.json();
}

/**
 * Call a Postgres function (RPC). Returns whatever the function returns.
 */
async function rpc(fn, args) {
  ensureConfigured();
  const url = SUPABASE_URL + '/rest/v1/rpc/' + fn;
  const r = await fetch(url, {
    method: 'POST',
    headers: baseHeaders(),
    body: JSON.stringify(args || {}),
  });
  if (!r.ok) {
    const body = await r.text().catch(() => '');
    throw Object.assign(new Error('rpc_failed'), { status: r.status, body });
  }
  if (r.status === 204) return null;
  return r.json();
}

export { selectFrom, insertInto, updateWhere, rpc, ensureConfigured };
