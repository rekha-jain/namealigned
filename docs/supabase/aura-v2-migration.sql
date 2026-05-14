-- ============================================================
-- Aura V2 schema migration.
-- Idempotent. Safe to run multiple times.
--
-- Apply via Supabase SQL Editor:
--   1. Paste this entire file.
--   2. Run.
--   3. Verify the SELECT at the bottom returns all expected tables.
--
-- Tables:
--   aura_users               anonymous + signed-in users
--   aura_conversations       threads
--   aura_messages            individual turns
--   aura_celestial_states    cached planetary snapshots (15-min buckets)
--   aura_symbols             RAG corpus (pgvector)
--   aura_user_memories       continuity layer (pgvector)
--   aura_subscriptions       payment records (future)
--   aura_events              server-side analytics mirror
--   aura_daily_quota         global Gemini free-tier counter
-- ============================================================

create extension if not exists "uuid-ossp";
create extension if not exists "pgcrypto";
create extension if not exists "vector";

-- ---------- aura_users ----------
create table if not exists public.aura_users (
  id                   uuid primary key default uuid_generate_v4(),
  auth_user_id         uuid unique,
  anonymous_token      text unique,
  first_seen_at        timestamptz not null default now(),
  last_seen_at         timestamptz not null default now(),
  profile              jsonb not null default '{}'::jsonb,
  subscription_tier    text not null default 'free',
  trial_messages_used  int not null default 0,
  total_messages       int not null default 0,
  flags                jsonb not null default '{}'::jsonb
);
create index if not exists aura_users_auth_idx     on public.aura_users (auth_user_id);
create index if not exists aura_users_anon_idx     on public.aura_users (anonymous_token);
create index if not exists aura_users_lastseen_idx on public.aura_users (last_seen_at desc);

-- ---------- aura_conversations ----------
create table if not exists public.aura_conversations (
  id             uuid primary key default uuid_generate_v4(),
  user_id        uuid not null references public.aura_users(id) on delete cascade,
  started_at     timestamptz not null default now(),
  last_msg_at    timestamptz not null default now(),
  title          text,
  topic_summary  text,
  message_count  int not null default 0,
  archived       boolean not null default false
);
create index if not exists aura_conv_user_idx on public.aura_conversations (user_id, last_msg_at desc);

-- ---------- aura_messages ----------
create table if not exists public.aura_messages (
  id                  uuid primary key default uuid_generate_v4(),
  conversation_id     uuid not null references public.aura_conversations(id) on delete cascade,
  user_id             uuid not null references public.aura_users(id) on delete cascade,
  role                text not null check (role in ('user','assistant','system')),
  content             text not null,
  intent_category     text,
  intent_subcat       text,
  emotional_tone      text,
  archetype_tags      text[] default array[]::text[],
  symbol_ids          uuid[] default array[]::uuid[],
  celestial_state_id  uuid,
  model_used          text,
  prompt_tokens       int,
  completion_tokens   int,
  latency_ms          int,
  created_at          timestamptz not null default now()
);
create index if not exists aura_msg_conv_idx  on public.aura_messages (conversation_id, created_at);
create index if not exists aura_msg_user_idx  on public.aura_messages (user_id, created_at desc);
create index if not exists aura_msg_tags_idx  on public.aura_messages using gin (archetype_tags);

-- ---------- aura_celestial_states ----------
create table if not exists public.aura_celestial_states (
  id            uuid primary key default uuid_generate_v4(),
  ts_bucket     timestamptz not null,
  geo_bucket    text not null,
  planets       jsonb not null,
  ascendant     numeric(6,3),
  moon_phase    text,
  retrogrades   text[] default array[]::text[],
  transits      jsonb default '{}'::jsonb,
  computed_at   timestamptz not null default now(),
  unique (ts_bucket, geo_bucket)
);
create index if not exists aura_celestial_ts_idx on public.aura_celestial_states (ts_bucket desc);

-- ---------- aura_symbols ----------
create table if not exists public.aura_symbols (
  id              uuid primary key default uuid_generate_v4(),
  name            text not null,
  category        text not null,
  archetype       text,
  planet          text,
  house           int,
  intent_tags     text[] default array[]::text[],
  emotional_tags  text[] default array[]::text[],
  body            text not null,
  source          text,
  source_ref      text,
  embedding       vector(768),
  created_at      timestamptz not null default now()
);
-- HNSW index on pgvector. Cosine distance for normalised embeddings.
do $$
begin
  if not exists (select 1 from pg_indexes where schemaname='public' and indexname='aura_symbols_embedding_idx') then
    create index aura_symbols_embedding_idx
      on public.aura_symbols using hnsw (embedding vector_cosine_ops)
      with (m = 16, ef_construction = 64);
  end if;
end$$;
create index if not exists aura_symbols_intent_idx    on public.aura_symbols using gin (intent_tags);
create index if not exists aura_symbols_emotional_idx on public.aura_symbols using gin (emotional_tags);

-- ---------- aura_user_memories ----------
create table if not exists public.aura_user_memories (
  id                  uuid primary key default uuid_generate_v4(),
  user_id             uuid not null references public.aura_users(id) on delete cascade,
  kind                text not null,
  content             text not null,
  source_message_id   uuid references public.aura_messages(id) on delete set null,
  embedding           vector(768),
  salience            real not null default 1.0,
  last_referenced_at  timestamptz not null default now(),
  expires_at          timestamptz,
  created_at          timestamptz not null default now()
);
do $$
begin
  if not exists (select 1 from pg_indexes where schemaname='public' and indexname='aura_memories_embedding_idx') then
    create index aura_memories_embedding_idx
      on public.aura_user_memories using hnsw (embedding vector_cosine_ops)
      with (m = 16, ef_construction = 64);
  end if;
end$$;
create index if not exists aura_memories_user_idx on public.aura_user_memories (user_id, salience desc);

-- ---------- aura_subscriptions ----------
create table if not exists public.aura_subscriptions (
  id            uuid primary key default uuid_generate_v4(),
  user_id       uuid not null references public.aura_users(id) on delete cascade,
  tier          text not null,
  status        text not null,
  started_at    timestamptz not null default now(),
  expires_at    timestamptz not null,
  provider      text not null,
  provider_ref  text not null,
  amount        int not null,
  currency      text not null default 'INR',
  unique (provider, provider_ref)
);
create index if not exists aura_subs_user_idx on public.aura_subscriptions (user_id, status);

-- ---------- aura_events ----------
create table if not exists public.aura_events (
  id          bigserial primary key,
  user_id     uuid references public.aura_users(id) on delete set null,
  event_name  text not null,
  properties  jsonb not null default '{}'::jsonb,
  occurred_at timestamptz not null default now()
);
create index if not exists aura_events_name_idx on public.aura_events (event_name, occurred_at desc);
create index if not exists aura_events_user_idx on public.aura_events (user_id, occurred_at desc);

-- ---------- aura_daily_quota ----------
create table if not exists public.aura_daily_quota (
  date          date not null,
  model_family  text not null default 'gemini_free',
  call_count    int not null default 0,
  cap           int not null default 1250,
  last_call_at  timestamptz,
  primary key (date, model_family)
);

-- Atomic increment helper. Returns the new state.
create or replace function public.inc_aura_daily_quota(p_date date, p_model text)
returns table (call_count int, cap int)
language sql as $$
  insert into public.aura_daily_quota (date, model_family, call_count, last_call_at)
  values (p_date, p_model, 1, now())
  on conflict (date, model_family) do update
    set call_count   = public.aura_daily_quota.call_count + 1,
        last_call_at = now()
  returning aura_daily_quota.call_count, aura_daily_quota.cap;
$$;

-- pgvector cosine match helper for aura_symbols.
create or replace function public.match_aura_symbols(
  query_embedding vector(768),
  match_count int default 5
)
returns table (
  id           uuid,
  name         text,
  body         text,
  planet       text,
  intent_tags  text[],
  source       text,
  source_ref   text,
  similarity   float
)
language sql stable as $$
  select s.id, s.name, s.body, s.planet, s.intent_tags, s.source, s.source_ref,
         1 - (s.embedding <=> query_embedding) as similarity
  from public.aura_symbols s
  where s.embedding is not null
  order by s.embedding <=> query_embedding
  limit match_count;
$$;

-- pgvector cosine match helper for aura_user_memories.
create or replace function public.match_aura_memories(
  p_user_id uuid,
  query_embedding vector(768),
  match_count int default 5
)
returns table (
  id          uuid,
  kind        text,
  content     text,
  salience    real,
  similarity  float
)
language sql stable as $$
  select m.id, m.kind, m.content, m.salience,
         1 - (m.embedding <=> query_embedding) as similarity
  from public.aura_user_memories m
  where m.user_id = p_user_id
    and m.embedding is not null
    and (m.expires_at is null or m.expires_at > now())
  order by m.embedding <=> query_embedding
  limit match_count;
$$;

-- ---------- RLS ----------
alter table public.aura_users          enable row level security;
alter table public.aura_conversations  enable row level security;
alter table public.aura_messages       enable row level security;
alter table public.aura_user_memories  enable row level security;
alter table public.aura_subscriptions  enable row level security;

-- All writes happen via service_role (backend). No client read paths yet.
-- Authenticated users may read their own rows once we wire Supabase Auth.
do $$
begin
  if not exists (select 1 from pg_policies where schemaname='public' and policyname='own_conversations') then
    create policy own_conversations on public.aura_conversations
      for select to authenticated
      using (user_id in (select id from public.aura_users where auth_user_id = auth.uid()));
  end if;
  if not exists (select 1 from pg_policies where schemaname='public' and policyname='own_messages') then
    create policy own_messages on public.aura_messages
      for select to authenticated
      using (user_id in (select id from public.aura_users where auth_user_id = auth.uid()));
  end if;
end$$;

-- aura_symbols, aura_celestial_states, aura_events, aura_daily_quota
-- are server-only. Clients should never query them directly.
revoke all on public.aura_symbols           from anon, authenticated;
revoke all on public.aura_celestial_states  from anon, authenticated;
revoke all on public.aura_events            from anon, authenticated;
revoke all on public.aura_daily_quota       from anon, authenticated;

-- ---------- Verify ----------
select table_name
from information_schema.tables
where table_schema = 'public'
  and table_name like 'aura_%'
order by table_name;
