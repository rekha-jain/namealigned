-- Freeze each paid report as the buyer first saw it (date, score, name
-- suggestions). Written once by POST /api/generate-report {action:'snapshot'}
-- and read back by GET /api/generate-report so later logic changes never
-- alter a report a customer already has.
alter table public.orders add column if not exists report_snapshot jsonb;
