import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const envPath = path.join(root, '.env.local');
const outPath = path.join(root, 'exports', 'analyzer-users.csv');

function loadEnv(filePath) {
  const env = {};
  const raw = fs.readFileSync(filePath, 'utf8');
  for (const line of raw.split(/\r?\n/)) {
    if (!line || line.trim().startsWith('#')) continue;
    const match = line.match(/^([A-Za-z_][A-Za-z0-9_]*)=(.*)$/);
    if (!match) continue;
    let value = match[2].trim();
    if (
      (value.startsWith('"') && value.endsWith('"')) ||
      (value.startsWith("'") && value.endsWith("'"))
    ) {
      value = value.slice(1, -1);
    }
    env[match[1]] = value;
  }
  return env;
}

function csvCell(value) {
  return `"${String(value ?? '').replace(/"/g, '""')}"`;
}

const env = loadEnv(envPath);
const supabaseUrl = (env.SUPABASE_URL || '').replace(/\/+$/, '');
const supabaseKey = env.SUPABASE_SERVICE_KEY || env.SUPABASE_ANON_KEY || '';

if (!supabaseUrl || !supabaseKey) {
  throw new Error('SUPABASE_URL and SUPABASE_SERVICE_KEY are required in .env.local');
}

const rows = [];
const pageSize = 1000;

for (let offset = 0; ; offset += pageSize) {
  const url = new URL(`${supabaseUrl}/rest/v1/leads`);
  url.searchParams.set('select', 'name,email,created_at');
  url.searchParams.set('email', 'not.is.null');
  url.searchParams.set('order', 'created_at.asc');
  url.searchParams.set('limit', String(pageSize));
  url.searchParams.set('offset', String(offset));

  const response = await fetch(url, {
    headers: {
      apikey: supabaseKey,
      Authorization: `Bearer ${supabaseKey}`,
    },
  });

  if (!response.ok) {
    throw new Error(`Supabase export failed [${response.status}]: ${await response.text()}`);
  }

  const batch = await response.json();
  rows.push(...batch);
  if (batch.length < pageSize) break;
}

const byEmail = new Map();
for (const row of rows) {
  const email = String(row.email || '').trim().toLowerCase();
  if (!email) continue;
  if (!byEmail.has(email)) {
    byEmail.set(email, {
      name: String(row.name || '').trim(),
      email,
    });
  }
}

fs.mkdirSync(path.dirname(outPath), { recursive: true });
fs.writeFileSync(
  outPath,
  ['name,email', ...Array.from(byEmail.values()).map(row => [row.name, row.email].map(csvCell).join(','))].join('\n') + '\n'
);

console.log(`Exported ${byEmail.size} analyzer users to ${outPath}`);
