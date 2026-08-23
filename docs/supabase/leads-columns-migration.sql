-- ============================================================
-- NameAligned — leads table column alignment (Apr 2026 app rename)
-- ============================================================
-- Run in Supabase SQL Editor if /api/capture-lead returns 500
-- or logs "column ... does not exist" for public.leads.
-- Idempotent: safe to run multiple times.
-- ============================================================

alter table public.leads
  add column if not exists phone           text,
  add column if not exists moolank         integer,
  add column if not exists bhagyank        integer,
  add column if not exists name_number     integer,
  add column if not exists alignment_score numeric;

-- Backfill renamed columns from legacy names when present.
do $$
begin
  if exists (
    select 1 from information_schema.columns
    where table_schema = 'public' and table_name = 'leads' and column_name = 'mobile'
  ) then
    execute 'update public.leads set phone = mobile where phone is null and mobile is not null';
  end if;

  if exists (
    select 1 from information_schema.columns
    where table_schema = 'public' and table_name = 'leads' and column_name = 'birth_num'
  ) then
    execute 'update public.leads set moolank = birth_num where moolank is null and birth_num is not null';
  end if;

  if exists (
    select 1 from information_schema.columns
    where table_schema = 'public' and table_name = 'leads' and column_name = 'dest_num'
  ) then
    execute 'update public.leads set bhagyank = dest_num where bhagyank is null and dest_num is not null';
  end if;

  if exists (
    select 1 from information_schema.columns
    where table_schema = 'public' and table_name = 'leads' and column_name = 'name_num'
  ) then
    execute 'update public.leads set name_number = name_num where name_number is null and name_num is not null';
  end if;

  if exists (
    select 1 from information_schema.columns
    where table_schema = 'public' and table_name = 'leads' and column_name = 'pct'
  ) then
    execute 'update public.leads set alignment_score = pct where alignment_score is null and pct is not null';
  end if;
end $$;

grant select, insert, update, delete on table public.leads to service_role;
