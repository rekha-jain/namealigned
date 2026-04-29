'use strict';

export function getSupabaseConfig() {
  const url = (process.env.SUPABASE_URL || '').replace(/\/+$/, '');
  const key = process.env.SUPABASE_SERVICE_KEY || process.env.SUPABASE_ANON_KEY || '';

  if (!url) {
    throw new Error('SUPABASE_URL is not configured');
  }
  if (!key) {
    throw new Error('SUPABASE_SERVICE_KEY or SUPABASE_ANON_KEY is not configured');
  }

  return { url, key };
}

export async function insertSupabaseRow(table, row, { duplicateOk = false, prefer = 'return=representation' } = {}) {
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
      return null;
    }
    throw new Error(`Supabase ${table} insert failed [${response.status}]: ${errorText}`);
  }

  if (prefer === 'return=minimal' || response.status === 204) {
    return null;
  }

  const rows = await response.json();
  return Array.isArray(rows) ? rows[0] : rows;
}
