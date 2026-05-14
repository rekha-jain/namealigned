/**
 * Vercel Serverless Function, GET /api/health-supabase
 *
 * Diagnostic-only endpoint that surfaces exactly why orders are or
 * aren't reaching Supabase. Checks env vars, network, schema, and
 * does a dry-run insert/rollback against the orders table.
 *
 * NOT for public traffic. Protected by a shared secret.
 *
 * Usage:
 *   curl https://www.namealigned.com/api/health-supabase?secret=YOUR_SECRET
 *
 * Required env vars:
 *   SUPABASE_URL
 *   SUPABASE_SERVICE_KEY
 *   HEALTH_CHECK_SECRET   (any string; if unset the endpoint refuses)
 */

'use strict';

const ORDERS_COLUMNS = [
  'lead_id', 'name', 'dob', 'payment_status',
  'razorpay_payment_id', 'paypal_order_id', 'paypal_capture_id',
  'payment_provider', 'payment_amount', 'payment_currency',
  'email', 'phone', 'moolank', 'bhagyank', 'name_number',
  'created_at',
];

const LEADS_COLUMNS = ['id', 'email', 'created_at'];

export default async function handler(req, res) {
  const url    = (process.env.SUPABASE_URL || '').replace(/\/+$/, '');
  const key    = process.env.SUPABASE_SERVICE_KEY || '';
  const secret = process.env.HEALTH_CHECK_SECRET || '';

  // Auth: require either an env-defined secret OR (if unset) refuse hard.
  // This prevents drive-by enumeration of the schema.
  const provided = (req.query && req.query.secret) || req.headers['x-health-secret'];
  if (!secret) return json(res, 403, { ok: false, error: 'HEALTH_CHECK_SECRET env var is not set' });
  if (provided !== secret) return json(res, 401, { ok: false, error: 'Invalid or missing secret' });

  const report = {
    ok: true,
    checks: {},
    schema: { orders: { present: [], missing: [] }, leads: { present: [], missing: [] } },
    sample_rows: { orders: null, leads: null },
    dry_run_insert: null,
  };

  // 1. Env vars
  report.checks.env_supabase_url = !!url;
  report.checks.env_service_key  = !!key && key.length > 30;
  if (!url || !key) {
    report.ok = false;
    report.error = 'Missing SUPABASE_URL or SUPABASE_SERVICE_KEY';
    return json(res, 500, report);
  }

  // 2. Connectivity + auth (HEAD on a system view)
  try {
    const r = await fetch(`${url}/rest/v1/orders?select=*&limit=0`, {
      headers: { apikey: key, Authorization: `Bearer ${key}`, Prefer: 'count=exact' },
    });
    report.checks.orders_table_reachable = r.ok;
    report.checks.orders_row_count       = r.headers.get('content-range');
    if (!r.ok) {
      const body = await r.text();
      report.ok = false;
      report.error = `orders SELECT failed [${r.status}]`;
      report.error_body = body.slice(0, 500);
      return json(res, 500, report);
    }
  } catch (e) {
    report.ok = false;
    report.error = 'Network error contacting Supabase: ' + (e && e.message);
    return json(res, 500, report);
  }

  // 3. Schema probe, request every column we send and see which return
  //    PGRST/42703 "column does not exist". If a column is missing, that
  //    is almost certainly why the insert is rejected.
  await probeColumns('orders', ORDERS_COLUMNS, url, key, report);
  await probeColumns('leads',  LEADS_COLUMNS,  url, key, report);

  // 4. Latest 3 rows from each table (just for sanity)
  report.sample_rows.orders = await fetchLatest(url, key, 'orders', 'id,email,payment_status,created_at', 3);
  report.sample_rows.leads  = await fetchLatest(url, key, 'leads',  'id,email,created_at',                3);

  // 5. Dry-run insert into orders with a sentinel email so we can prove
  //    the write path works end-to-end. Rolled back via delete on the
  //    same razorpay_payment_id.
  const probeId = 'health-probe-' + Date.now();
  const probeEmail = 'health-probe@namealigned.test';
  try {
    const ins = await fetch(`${url}/rest/v1/orders`, {
      method: 'POST',
      headers: { apikey: key, Authorization: `Bearer ${key}`, 'Content-Type': 'application/json', Prefer: 'return=representation' },
      body: JSON.stringify({
        name: 'health-probe',
        email: probeEmail,
        payment_status: 'paid',
        razorpay_payment_id: probeId,
        created_at: new Date().toISOString(),
      }),
    });
    report.dry_run_insert = { status: ins.status, ok: ins.ok };
    if (!ins.ok) {
      report.dry_run_insert.error_body = (await ins.text()).slice(0, 500);
    } else {
      // Clean up the probe row
      await fetch(`${url}/rest/v1/orders?razorpay_payment_id=eq.${encodeURIComponent(probeId)}`, {
        method: 'DELETE',
        headers: { apikey: key, Authorization: `Bearer ${key}`, Prefer: 'return=minimal' },
      });
    }
  } catch (e) {
    report.dry_run_insert = { error: e && e.message };
  }

  return json(res, 200, report);
}

async function probeColumns(table, cols, url, key, report) {
  for (const col of cols) {
    try {
      const r = await fetch(`${url}/rest/v1/${table}?select=${col}&limit=0`, {
        headers: { apikey: key, Authorization: `Bearer ${key}` },
      });
      if (r.ok) report.schema[table].present.push(col);
      else {
        const body = await r.text();
        if (/PGRST|42703|column .* does not exist/i.test(body)) {
          report.schema[table].missing.push(col);
        } else {
          report.schema[table].missing.push(col + ' (status=' + r.status + ')');
        }
      }
    } catch (e) {
      report.schema[table].missing.push(col + ' (network err)');
    }
  }
}

async function fetchLatest(url, key, table, select, limit) {
  try {
    const r = await fetch(
      `${url}/rest/v1/${table}?select=${select}&order=created_at.desc&limit=${limit}`,
      { headers: { apikey: key, Authorization: `Bearer ${key}` } }
    );
    if (!r.ok) return { error: 'status=' + r.status, body: (await r.text()).slice(0, 200) };
    return await r.json();
  } catch (e) {
    return { error: e && e.message };
  }
}

function json(res, status, body) {
  res.status(status).setHeader('content-type', 'application/json');
  res.end(JSON.stringify(body, null, 2));
}
