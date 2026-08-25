-- Deduplicate orders by razorpay_payment_id / paypal_order_id, then
-- enforce UNIQUE constraints so delivery emails cannot fire twice.
--
-- Run in Supabase SQL Editor (Dashboard → SQL) once.
-- Safe to re-run: keeps the oldest row per payment id.

-- 1. Razorpay duplicates: keep earliest created_at, delete the rest
delete from public.orders o
using public.orders newer
where o.razorpay_payment_id is not null
  and o.razorpay_payment_id = newer.razorpay_payment_id
  and o.created_at > newer.created_at;

-- 2. PayPal duplicates: keep earliest created_at, delete the rest
delete from public.orders o
using public.orders newer
where o.paypal_order_id is not null
  and o.paypal_order_id = newer.paypal_order_id
  and o.created_at > newer.created_at;

-- 3. Unique constraints (idempotent)
do $$
begin
  if not exists (
    select 1 from pg_constraint
    where conname = 'orders_razorpay_payment_id_key'
  ) then
    alter table public.orders
      add constraint orders_razorpay_payment_id_key
      unique (razorpay_payment_id);
  end if;
end $$;

do $$
begin
  if not exists (
    select 1 from pg_constraint
    where conname = 'orders_paypal_order_id_key'
  ) then
    alter table public.orders
      add constraint orders_paypal_order_id_key
      unique (paypal_order_id);
  end if;
end $$;
