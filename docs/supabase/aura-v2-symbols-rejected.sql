-- ============================================================
-- Aura V2 Phase C followup: rejected-symbol audit trail.
-- Run this in Supabase SQL Editor. Idempotent.
--
-- During ingestion the grader rejects symbol cards that fail more
-- than 1 quality axis. We keep them here for periodic human review,
-- so we can spot patterns in what gets dropped and tune the grader.
-- ============================================================

create table if not exists public.aura_symbols_rejected (
  id           uuid primary key default uuid_generate_v4(),
  source       text,
  source_ref   text,
  body         text not null,
  card         jsonb not null,            -- the original extracted card
  scores       jsonb not null,            -- {absolute:false, prescription:false, citation:true, length:true, plain:true}
  reasons      text[] default array[]::text[],
  created_at   timestamptz not null default now()
);
create index if not exists aura_symbols_rejected_source_idx on public.aura_symbols_rejected (source, created_at desc);

revoke all on public.aura_symbols_rejected from anon, authenticated;

select 'aura_symbols_rejected ready' as status;
