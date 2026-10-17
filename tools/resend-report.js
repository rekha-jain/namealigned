/**
 * Resend the report delivery email for a PayPal order and stamp report_sent_at.
 *
 *   node --env-file=.env.local tools/resend-report.js <order-uuid> [--send]
 *
 * Without --send it only prints what would be sent.
 * Needs SUPABASE_URL, SUPABASE_SERVICE_KEY and BREVO_API_KEY in env.
 */
import { getSupabaseConfig, markReportSent } from '../api/_supabase.js';
import { buildSupabaseHeaders } from '../api/_supabaseHeaders.js';
import { sendDeliveryEmail } from '../api/paypal-capture.js';

const [orderId, flag] = process.argv.slice(2);
if (!orderId) {
  console.error('Usage: node tools/resend-report.js <order-uuid> [--send]');
  process.exit(1);
}

const { url, key } = getSupabaseConfig();
const res = await fetch(`${url}/rest/v1/orders?id=eq.${encodeURIComponent(orderId)}&select=*`, {
  headers: buildSupabaseHeaders(key),
});
const [order] = await res.json();
if (!order) { console.error('Order not found'); process.exit(1); }
if (!order.paypal_order_id) { console.error('Only PayPal orders are supported'); process.exit(1); }

console.log(`Order ${order.id}: ${order.name} <${order.email}> paypal=${order.paypal_order_id} report_sent_at=${order.report_sent_at}`);
if (flag !== '--send') { console.log('Dry run. Add --send to email.'); process.exit(0); }

const sent = await sendDeliveryEmail({
  paypalOrderId: order.paypal_order_id,
  name: order.name,
  email: order.email,
  dob: order.dob || '',
  mobile: order.phone || '',
  birthNum: order.moolank,
  destNum: order.bhagyank,
  nameNum: order.name_number,
});
if (!sent) { console.error('Send failed'); process.exit(1); }
await markReportSent(order.id);
console.log('Sent and stamped report_sent_at');
