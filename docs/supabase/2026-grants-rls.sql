-- ============================================================
-- NameAligned, Supabase grants + RLS prep (May 30 / Oct 30 2026)
-- ============================================================
-- Supabase is removing the implicit "public schema → Data API" exposure.
-- After May 30 2026 (new projects) and Oct 30 2026 (existing projects),
-- every table that needs Data API access must have explicit GRANTs.
--
-- Our server code uses the SERVICE_ROLE key, which bypasses RLS but
-- still requires GRANTs after the change. Anon access stays denied
-- (we never expose tables to the browser).
--
-- Run this in Supabase, SQL Editor as the postgres user.
-- Idempotent: safe to run multiple times.
-- ============================================================

-- ── ORDERS TABLE ────────────────────────────────────────────
-- Service role: full access (used by api/generate-report.js,
-- api/paypal-capture.js, api/razorpay-webhook.js).
grant select, insert, update, delete
  on table public.orders
  to service_role;

-- Authenticated role: read-only access to your own orders
-- (only used if you later add a logged-in customer dashboard).
grant select on table public.orders to authenticated;

-- Anon: NO ACCESS. Orders contain PII.
revoke all on table public.orders from anon;

-- Enable RLS
alter table public.orders enable row level security;

-- Policy: service role bypasses RLS automatically, but we still
-- define an explicit "deny-by-default" baseline by adding only the
-- one read policy for authenticated users we want.
drop policy if exists "orders_read_own" on public.orders;
create policy "orders_read_own"
  on public.orders
  for select
  to authenticated
  using (auth.uid()::text = lead_id::text);

-- ── LEADS TABLE ─────────────────────────────────────────────
grant select, insert, update, delete
  on table public.leads
  to service_role;

grant select on table public.leads to authenticated;
revoke all on table public.leads from anon;

alter table public.leads enable row level security;

drop policy if exists "leads_read_own" on public.leads;
create policy "leads_read_own"
  on public.leads
  for select
  to authenticated
  using (auth.uid()::text = id::text);

-- ── ORDERS COLUMNS SANITY CHECK ─────────────────────────────
-- The application code writes these columns. Run this query to
-- see which (if any) are missing in your current schema:
--
-- select column_name from information_schema.columns
-- where table_schema='public' and table_name='orders'
-- order by ordinal_position;
--
-- Expected columns (from api/generate-report.js + api/paypal-capture.js):
--   id (uuid, pk)
--   lead_id (uuid, fk → leads.id, nullable)
--   name (text)
--   dob (date or text, nullable)
--   payment_status (text)
--   razorpay_payment_id (text, nullable, unique)
--   paypal_order_id (text, nullable, unique)
--   paypal_capture_id (text, nullable)
--   payment_provider (text, nullable, default 'razorpay')
--   payment_amount (numeric or int, nullable)
--   payment_currency (text, nullable, default 'INR')
--   email (text)
--   phone (text, nullable)
--   moolank (int, nullable)
--   bhagyank (int, nullable)
--   name_number (int, nullable)
--   created_at (timestamptz, default now())

-- If any column is missing, add it. Example (idempotent):
alter table public.orders
  add column if not exists paypal_order_id    text,
  add column if not exists paypal_capture_id  text,
  add column if not exists payment_provider   text default 'razorpay',
  add column if not exists payment_amount     numeric,
  add column if not exists payment_currency   text default 'INR';

-- Uniqueness on payment identifiers (prevents the same payment
-- from being inserted twice if a webhook + browser race both fire).
do $$
begin
  if not exists (
    select 1 from pg_indexes
    where schemaname='public' and indexname='orders_razorpay_payment_id_key'
  ) then
    alter table public.orders
      add constraint orders_razorpay_payment_id_key
      unique (razorpay_payment_id);
  end if;
exception when others then
  -- Allow nulls to coexist (Postgres unique allows multiple NULLs by default).
  null;
end $$;

do $$
begin
  if not exists (
    select 1 from pg_indexes
    where schemaname='public' and indexname='orders_paypal_order_id_key'
  ) then
    alter table public.orders
      add constraint orders_paypal_order_id_key
      unique (paypal_order_id);
  end if;
exception when others then
  null;
end $$;
