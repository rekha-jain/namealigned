import fs from 'node:fs';
import path from 'node:path';
import { JSDOM } from 'jsdom';

const ROOT = path.resolve(new URL('..', import.meta.url).pathname);
const BASE = 'https://www.namealigned.com';
const LASTMOD = '2026-05-29';

function walk(dir) {
  return fs.readdirSync(dir, { withFileTypes: true }).flatMap((entry) => {
    if (entry.name === 'node_modules' || entry.name.startsWith('.')) return [];
    const full = path.join(dir, entry.name);
    return entry.isDirectory() ? walk(full) : [full];
  });
}

function routeFor(file) {
  let rel = path.relative(ROOT, file).replace(/\\/g, '/').replace(/\.html$/, '');
  if (rel === 'index') return '/';
  return '/' + rel.replace(/\/index$/, '');
}

function priorityFor(route) {
  if (route === '/') return '1.0';
  if (route === '/number') return '0.95';
  if (['/analyzer', '/name-numerology-calculator', '/name-alignment', '/love-compatibility-numerology', '/ask-aura'].includes(route)) return '0.9';
  if (/^\/number\/[1-9]-(personality|career)$/.test(route)) return '0.88';
  if (/^\/(name-number|life-path-number)-[1-9]-meaning$/.test(route)) return '0.88';
  if (/^\/(number-[1-9]-in-love|why-number-[1-9]-overthinks|number-[1-9]-spiritual-meaning|lucky-attributes-number-[1-9])$/.test(route)) return '0.84';
  if (/^\/number-[1-9]-and-[1-9]-compatibility$/.test(route)) return '0.84';
  if (route.startsWith('/blog/')) return '0.72';
  if (route === '/blog') return '0.8';
  if (['/privacy', '/terms', '/refund'].includes(route)) return '0.25';
  return '0.65';
}

function changefreqFor(route) {
  if (route === '/' || route === '/number' || route === '/blog' || route === '/sitemap-pages' || route === '/ask-aura') return 'weekly';
  if (['/privacy', '/terms', '/refund'].includes(route)) return 'yearly';
  return 'monthly';
}

const files = walk(ROOT).filter((file) => file.endsWith('.html'));
const urls = [];

for (const file of files) {
  const route = routeFor(file);
  if (
    route.startsWith('/share') ||
    route.startsWith('/samples') ||
    /preview|staging-report|share-card|wordmark|google31/.test(route)
  ) continue;

  const html = fs.readFileSync(file, 'utf8');
  const doc = new JSDOM(html).window.document;
  const robots = doc.querySelector('meta[name="robots"]')?.getAttribute('content') || '';
  if (/noindex/i.test(robots)) continue;

  const canonical = doc.querySelector('link[rel="canonical"]')?.getAttribute('href');
  const loc = canonical && canonical.startsWith(BASE) ? canonical : BASE + (route === '/' ? '/' : route);
  urls.push({ loc, route, priority: priorityFor(route), changefreq: changefreqFor(route) });
}

urls.sort((a, b) => {
  if (a.route === '/') return -1;
  if (b.route === '/') return 1;
  return a.route.localeCompare(b.route);
});

const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls.map((url) => `  <url>
    <loc>${url.loc}</loc>
    <lastmod>${LASTMOD}</lastmod>
    <changefreq>${url.changefreq}</changefreq>
    <priority>${url.priority}</priority>
  </url>`).join('\n')}
</urlset>
`;

fs.writeFileSync(path.join(ROOT, 'sitemap.xml'), xml);
console.log(JSON.stringify({ urls: urls.length, lastmod: LASTMOD }, null, 2));
