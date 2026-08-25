'use strict';

/**
 * Normalise an Indian mobile to 10 digits.
 *
 * Razorpay `payment.contact` is often "+919300797434". Taking
 * `.replace(/\D/g,'').slice(0,10)` wrongly yields "9193007974".
 * Always keep the last 10 digits so +91 / 91 prefixes are dropped.
 */
export function normaliseIndianMobile(raw) {
  const digits = String(raw || '').replace(/\D/g, '');
  if (!digits) return '';
  if (digits.length >= 10) return digits.slice(-10);
  return digits;
}
