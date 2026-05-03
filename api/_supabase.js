'use strict';

export function getSupabaseConfig() {
  const url = (process.env.SUPABASE_URL || '').replace(/\/+$/, '');
  // ENFORCE service key on the server. Anon key + RLS silently rejects inserts.
  const key = process.env.SUPABASE_SERVICE_KEY || '';

  if (!url) throw new Error('SUPABASE_URL is not configured');
  if (!key) {
    throw new Error(
      'SUPABASE_SERVICE_KEY is not configured. Server-side inserts MUST use the service role key, not anon.'
    );
  }
  return { url, key };
}

export async function insertSupabaseRow(
  table,
  row,
  { duplicateOk = false, prefer = 'return=representation' } = {}
) {
  const { url, key } = getSupabaseConfig();

  const response = await fetch(`${url}/rest/v1/${table}`, {
    method: 'POST',
    headers: {
      apikey: key,
      Authorization: `Bearer ${key}`,
      'Content-Type': 'application/json',
      Prefer: prefer,
    },
    body: JSON.stringify(row),
  });

  if (!response.ok) {
    const errorText = await response.text();
    if (duplicateOk && response.status === 409) {
      console.warn(`[supabase] ${table} duplicate ignored: ${errorText}`);
      return null;
    }
    // LOUD log so it shows up in Vercel without being mistaken for a warning.
    console.error(
      `[supabase] INSERT ${table} FAILED status=${response.status} body=${errorText} payload=${JSON.stringify(row)}`
    );
    throw new Error(`Supabase ${table} insert failed [${response.status}]: ${errorText}`);
  }

  if (prefer === 'return=minimal' || response.status === 204) return null;
  const rows = await response.json();
  return Array.isArray(rows) ? rows[0] : rows;
}

// Look up a lead by email so we can attach lead_id to orders.
export async function findLeadIdByEmail(email) {
  if (!email) return null;
  const { url, key } = getSupabaseConfig();
  const res = await fetch(
    `${url}/rest/v1/leads?email=eq.${encodeURIComponent(email)}&select=id&order=created_at.desc&limit=1`,
    { headers: { apikey: key, Authorization: `Bearer ${key}` } }
  );
  if (!res.ok) {
    console.error(`[supabase] lead lookup failed status=${res.status} body=${await res.text()}`);
    return null;
  }
  const rows = await res.json();
  return Array.isArray(rows) && rows[0] ? rows[0].id : null;
}
