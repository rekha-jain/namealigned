/**
 * GET /api/generate-report?paymentId=... (routed from generate-report.js;
 * kept out of its own function to stay within Vercel's 12-function limit)
 *
 * The report page builds the report ONLY from what this returns, never
 * from name/dob in the link. A paymentId that is not a paid order in
 * Supabase gets a 404, so editing the link or inventing an id cannot
 * produce a report.
 *
 * paymentId formats:
 *   PP-<paypal order id>   → orders.paypal_order_id
 *   pay_... / PROMO100_... → orders.razorpay_payment_id
 */
'use strict';

import { getSupabaseConfig } from './_supabase.js';
import { buildSupabaseHeaders } from './_supabaseHeaders.js';

function orderFilter(paymentId) {
  return paymentId.startsWith('PP-')
    ? `paypal_order_id=eq.${encodeURIComponent(paymentId.slice(3))}`
    : `razorpay_payment_id=eq.${encodeURIComponent(paymentId)}`;
}

export async function handleReportData(req, res) {
  res.setHeader('Cache-Control', 'no-store');

  const paymentId = String(req.query?.paymentId || '').trim();
  if (!paymentId || paymentId.length > 300) {
    return res.status(400).json({ success: false, error: 'paymentId is required' });
  }

  const filter = orderFilter(paymentId);

  try {
    const { url, key } = getSupabaseConfig();
    const r = await fetch(
      `${url}/rest/v1/orders?${filter}&payment_status=eq.paid&select=name,dob,email,phone,report_snapshot&order=created_at.asc&limit=1`,
      { headers: buildSupabaseHeaders(key) }
    );
    if (!r.ok) {
      console.error(`[report-data] lookup failed status=${r.status} body=${await r.text()}`);
      return res.status(502).json({ success: false, error: 'Lookup failed' });
    }
    const rows = await r.json();
    const order = Array.isArray(rows) ? rows[0] : null;
    if (!order) return res.status(404).json({ success: false, error: 'Order not found' });

    return res.status(200).json({
      success: true,
      paymentId,
      name:   order.name || '',
      dob:    order.dob || '',
      email:  order.email || '',
      mobile: order.phone || '',
      snapshot: order.report_snapshot || null,
    });
  } catch (err) {
    console.error('[report-data] error:', err);
    return res.status(500).json({ success: false, error: 'Internal error' });
  }
}

/**
 * POST /api/generate-report { action:'snapshot', paymentId, snapshot }
 *
 * Freezes what the buyer saw the first time the report opened (date,
 * score, name suggestions) so later logic changes never alter a report
 * a customer already has. Only writes when no snapshot exists yet.
 */
export async function handleSnapshotSave(req, res) {
  const { paymentId: rawId, snapshot } = req.body || {};
  const paymentId = String(rawId || '').trim();
  if (!paymentId || paymentId.length > 300) {
    return res.status(400).json({ success: false, error: 'paymentId is required' });
  }

  const corr = snapshot && snapshot.corrResult;
  const valid =
    snapshot && typeof snapshot === 'object' &&
    !isNaN(Date.parse(snapshot.generatedAt)) &&
    Number.isFinite(snapshot.pct) && snapshot.pct >= 0 && snapshot.pct <= 100 &&
    corr && Array.isArray(corr.corrections) && corr.corrections.length <= 3 &&
    JSON.stringify(snapshot).length < 20000;
  if (!valid) return res.status(400).json({ success: false, error: 'Invalid snapshot' });

  try {
    const { url, key } = getSupabaseConfig();
    const r = await fetch(
      `${url}/rest/v1/orders?${orderFilter(paymentId)}&payment_status=eq.paid&report_snapshot=is.null`,
      {
        method: 'PATCH',
        headers: buildSupabaseHeaders(key, { 'Content-Type': 'application/json', Prefer: 'return=minimal' }),
        body: JSON.stringify({ report_snapshot: snapshot }),
      }
    );
    if (!r.ok) {
      console.error(`[report-snapshot] save failed status=${r.status} body=${await r.text()}`);
      return res.status(502).json({ success: false, error: 'Save failed' });
    }
    return res.status(200).json({ success: true });
  } catch (err) {
    console.error('[report-snapshot] error:', err);
    return res.status(500).json({ success: false, error: 'Internal error' });
  }
}
