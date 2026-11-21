-- ============================================================
-- NameAligned, payment_failures table
-- ============================================================
-- Records failed and cancelled checkout attempts from both providers:
--   * Razorpay: browser payment.failed / modal dismiss, plus the
--     payment.failed webhook (authoritative, overwrites client rows)
--   * PayPal:   server-side capture failures (INSTRUMENT_DECLINED etc),
--     PAYMENT.CAPTURE.DENIED webhook, browser onCancel / onError
--
-- Written by api/_paymentFailures.js using the service role key.
-- One row per (provider, reference_id); reference_id is the provider
-- payment id when known, else the provider order id.
--
-- Run once in Supabase, SQL Editor. Idempotent.
-- ============================================================

create table if not exists public.payment_failures (
  id                bigserial primary key,
  created_at        timestamptz not null default now(),
  updated_at        timestamptz,
  provider          text not null check (provider in ('razorpay', 'paypal')),
  kind              text not null check (kind in ('failed', 'cancelled')),
  reference_id      text,
  payment_id        text,
  order_id          text,
  email             text,
  name              text,
  phone             text,
  amount            numeric,
  currency          text,
  error_code        text,
  error_description text,
  error_source      text,
  error_step        text,
  error_reason      text,
  debug_id          text,
  reported_by       text not null check (reported_by in ('client', 'server', 'webhook')),
  user_agent        text,
  raw               jsonb
);

create unique index if not exists payment_failures_provider_ref_key
  on public.payment_failures (provider, reference_id);

create index if not exists payment_failures_created_at_idx
  on public.payment_failures (created_at desc);

create index if not exists payment_failures_email_idx
  on public.payment_failures (email);

grant select, insert, update, delete on table public.payment_failures to service_role;
grant usage, select on sequence public.payment_failures_id_seq to service_role;
revoke all on table public.payment_failures from anon;
revoke all on table public.payment_failures from authenticated;

alter table public.payment_failures enable row level security;

-- Handy view: last 30 days of failures by reason
-- select provider, kind, error_code, error_reason, count(*)
--   from public.payment_failures
--  where created_at > now() - interval '30 days'
--  group by 1,2,3,4 order by 5 desc;
