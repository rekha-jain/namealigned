import fs from 'node:fs';
import path from 'node:path';
import { JSDOM } from 'jsdom';

const ROOT = path.resolve(new URL('..', import.meta.url).pathname);
const BASE = 'https://www.namealigned.com';
const MARKER_START = '<!-- NA_RELATED_INSIGHTS_START -->';
const MARKER_END = '<!-- NA_RELATED_INSIGHTS_END -->';
const HUB_START = '<!-- NA_HUB_DISCOVERY_START -->';
const HUB_END = '<!-- NA_HUB_DISCOVERY_END -->';
const BREAD_START = '<!-- NA_BREADCRUMB_START -->';
const BREAD_END = '<!-- NA_BREADCRUMB_END -->';

const planets = {
  1: ['Sun', 'leadership'],
  2: ['Moon', 'sensitivity'],
  3: ['Jupiter', 'expression'],
  4: ['Rahu', 'restlessness'],
  5: ['Mercury', 'adaptability'],
  6: ['Venus', 'harmony'],
  7: ['Ketu', 'depth'],
  8: ['Saturn', 'endurance'],
  9: ['Mars', 'courage'],
};

const exclude = [
  /^api\//,
  /^docs\//,
  /^samples\//,
  /^ingestion\//,
  /^assets\//,
  /^node_modules\//,
  /(^|\/)(wordmark-preview|index-preview|analyzer-preview|report-preview|staging-report|share-card|google31ebae08d641fdfa)\.html$/,
  // ask-aura.html is a full-viewport chat UI with no scroll. Injecting
  // breadcrumb / related-insights sections breaks the layout because the
  // page is built on flex height:100vh + overflow:hidden. Skip.
  /^ask-aura\.html$/,
];

function walk(dir) {
  return fs.readdirSync(dir, { withFileTypes: true }).flatMap((entry) => {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      if (entry.name === 'node_modules' || entry.name.startsWith('.')) return [];
      return walk(full);
    }
    return full;
  });
}

function routeFor(rel) {
  let route = '/' + rel.replace(/\\/g, '/').replace(/\.html$/, '');
  route = route.replace(/\/index$/, '');
  return route === '' ? '/' : route;
}

function titleFromDoc(doc, route) {
  const h1 = doc.querySelector('h1')?.textContent?.trim();
  const title = doc.querySelector('title')?.textContent?.trim();
  return (h1 || title || route).replace(/\s+/g, ' ');
}

function classify(route) {
  const c = { cluster: 'site', nums: [], pair: null };
  let m;
  if (route === '/') c.cluster = 'home';
  else if (route === '/number') c.cluster = 'number-hub';
  else if (route === '/love-compatibility-numerology') c.cluster = 'relationship-hub';
  else if (route === '/analyzer' || route.includes('calculator') || route.includes('name-correction') || route.includes('business-name')) c.cluster = 'tool';
  else if (route === '/report' || route === '/generate-report') c.cluster = 'report';
  else if ((m = route.match(/^\/number\/([1-9])-personality$/))) { c.cluster = 'personality'; c.nums = [+m[1]]; }
  else if ((m = route.match(/^\/number\/([1-9])-career$/))) { c.cluster = 'career'; c.nums = [+m[1]]; }
  else if ((m = route.match(/^\/name-number-([1-9])-meaning$/))) { c.cluster = 'identity'; c.nums = [+m[1]]; }
  else if ((m = route.match(/^\/life-path-number-([1-9])-meaning$/))) { c.cluster = 'life-path'; c.nums = [+m[1]]; }
  else if ((m = route.match(/^\/number-([1-9])-in-love$/))) { c.cluster = 'love-style'; c.nums = [+m[1]]; }
  else if ((m = route.match(/^\/why-number-([1-9])-overthinks$/))) { c.cluster = 'emotional-pattern'; c.nums = [+m[1]]; }
  else if ((m = route.match(/^\/number-([1-9])-spiritual-meaning$/))) { c.cluster = 'spiritual'; c.nums = [+m[1]]; }
  else if ((m = route.match(/^\/lucky-attributes-number-([1-9])$/))) { c.cluster = 'lucky'; c.nums = [+m[1]]; }
  else if ((m = route.match(/^\/number-([1-9])-and-([1-9])-compatibility$/))) { c.cluster = 'compatibility'; c.nums = [+m[1], +m[2]]; c.pair = [+m[1], +m[2]]; }
  else if (route.startsWith('/blog/')) c.cluster = 'blog';
  else if (route === '/blog') c.cluster = 'blog-hub';
  return c;
}

const allHtmlFiles = walk(ROOT)
  .filter((file) => file.endsWith('.html'))
  .map((file) => ({ file, rel: path.relative(ROOT, file).replace(/\\/g, '/') }))
  .filter(({ rel }) => !exclude.some((rx) => rx.test(rel)));

const htmlFiles = [];
let noindexCleaned = 0;
for (const item of allHtmlFiles) {
  let html = fs.readFileSync(item.file, 'utf8');
  const noindex = /<meta[^>]+name=["']robots["'][^>]+content=["'][^"']*noindex/i.test(html);
  if (noindex) {
    const before = html;
    html = stripMarked(html, MARKER_START, MARKER_END);
    html = stripMarked(html, HUB_START, HUB_END);
    html = stripMarked(html, BREAD_START, BREAD_END);
    html = html.replace(/\n?<link rel="stylesheet" href="\/?assets\/internal-linking\.css"\/>/g, '');
    if (html !== before) {
      fs.writeFileSync(item.file, html);
      noindexCleaned++;
    }
    continue;
  }
  htmlFiles.push(item);
}

const pages = htmlFiles.map(({ file, rel }) => {
  const html = fs.readFileSync(file, 'utf8');
  const doc = new JSDOM(html).window.document;
  const route = routeFor(rel);
  return { file, rel, route, title: titleFromDoc(doc, route), ...classify(route) };
});

const pageByRoute = new Map(pages.map((p) => [p.route, p]));
const has = (route) => pageByRoute.has(route);
const link = (href, title, note) => ({ href, title, note });

function existing(route) {
  return has(route) ? route : null;
}

function compactLinks(items, current, limit = 12) {
  const seen = new Set([current]);
  const out = [];
  for (const item of items) {
    if (!item?.href || seen.has(item.href) || !has(item.href)) continue;
    seen.add(item.href);
    out.push(item);
    if (out.length >= limit) break;
  }
  return out;
}

function pairRoutesFor(n) {
  return pages
    .filter((p) => p.cluster === 'compatibility' && p.nums.includes(n))
    .sort((a, b) => {
      const selfA = a.nums[0] === a.nums[1] ? 1 : 0;
      const selfB = b.nums[0] === b.nums[1] ? 1 : 0;
      return selfA - selfB || a.route.localeCompare(b.route);
    })
    .slice(0, 7)
    .map((p) => link(p.route, p.title.replace(' · Chaldean Numerology', ''), 'Relationship dynamic'));
}

function linksFor(page) {
  const n = page.nums[0];
  const base = [
    link('/analyzer', 'Run your free Chaldean analysis', 'Start with your full number map'),
    link('/love-compatibility-numerology', 'Compare a relationship dynamic', 'Partners, friends, family, coworkers'),
    link('/number', 'Explore the number archetype hub', 'All numbers, all angles'),
    link('/report', 'Unlock the full destiny report', 'Name, career, timing, compatibility'),
    link('/ask-aura', 'Ask Aura a personal follow-up', 'Turn the insight into a conversation'),
  ];

  if (n) {
    const planet = planets[n][0];
    const numberCluster = [
      link(`/number/${n}-personality`, `Number ${n} personality pattern`, `${planet} archetype and traits`),
      link(`/number/${n}-career`, `Number ${n} career rhythm`, 'Work style, strengths, pressure points'),
      link(`/name-number-${n}-meaning`, `Name Number ${n} meaning`, 'How the name vibration is received'),
      link(`/life-path-number-${n}-meaning`, `Life Path ${n} meaning`, 'Long-arc identity and timing'),
      link(`/number-${n}-in-love`, `Number ${n} in love`, 'Attachment style and emotional pacing'),
      link(`/why-number-${n}-overthinks`, `Why Number ${n} overthinks`, 'Stress response and mental loops'),
      link(`/number-${n}-spiritual-meaning`, `Number ${n} spiritual meaning`, 'Soul lesson and shadow practice'),
      link(`/lucky-attributes-number-${n}`, `Lucky attributes for Number ${n}`, 'Days, colours, stones, directions'),
      ...pairRoutesFor(n),
      link('/blog/moolank-meanings', 'Birth Number meanings guide', 'Read the number through Moolank'),
      link('/blog/relationship-compatibility-numerology', 'Relationship compatibility guide', 'How number pairs actually meet'),
    ];
    if (['personality', 'career', 'identity', 'life-path', 'love-style', 'emotional-pattern', 'spiritual', 'lucky'].includes(page.cluster)) {
      return compactLinks([...numberCluster, ...base], page.route, 15);
    }
  }

  if (page.cluster === 'compatibility') {
    const [a, b] = page.nums;
    return compactLinks([
      link('/love-compatibility-numerology', 'Read your own relationship dynamic', 'Use both names and birth dates'),
      link('/blog/relationship-compatibility-numerology', 'How compatibility scoring works', 'The relationship framework behind the score'),
      link(`/number/${a}-personality`, `Number ${a} personality pattern`, `${planets[a][0]} side of the match`),
      link(`/number/${b}-personality`, `Number ${b} personality pattern`, `${planets[b][0]} side of the match`),
      link(`/number-${a}-in-love`, `Number ${a} in love`, 'How this side bonds'),
      link(`/number-${b}-in-love`, `Number ${b} in love`, 'How this side bonds'),
      link(`/why-number-${a}-overthinks`, `Number ${a} stress pattern`, 'What pressure can trigger'),
      link(`/why-number-${b}-overthinks`, `Number ${b} stress pattern`, 'What pressure can trigger'),
      link('/number', 'Explore all number archetypes', 'Move from pair to full chart'),
      link('/report', 'See compatibility inside a full report', 'Personalised PDF context'),
      ...base,
    ], page.route, 12);
  }

  if (page.cluster === 'relationship-hub') {
    return compactLinks([
      link('/blog/relationship-compatibility-numerology', 'Relationship compatibility guide', 'The deeper framework'),
      link('/number-1-and-2-compatibility', 'Sun and Moon compatibility', 'A complementary emotional rhythm'),
      link('/number-2-and-7-compatibility', 'Moon and Ketu compatibility', 'Quiet depth and spiritual attunement'),
      link('/number-3-and-6-compatibility', 'Jupiter and Venus compatibility', 'Warmth, beauty, and expression'),
      link('/number-4-and-8-compatibility', 'Rahu and Saturn compatibility', 'Heavy patterns and conscious repair'),
      link('/number-8-and-9-compatibility', 'Saturn and Mars compatibility', 'Structure meeting urgency'),
      link('/number', 'Explore number archetypes before comparing', 'Read each person separately'),
      link('/report', 'Add the full chart context', 'Beyond one pair score'),
      ...base,
    ], page.route, 12);
  }

  if (page.cluster === 'number-hub') {
    return compactLinks([
      link('/love-compatibility-numerology', 'Compare two number rhythms', 'Relationship dynamics tool'),
      link('/blog/moolank-meanings', 'Birth Number meanings', 'Moolank as the inner number'),
      link('/blog/what-is-name-numerology', 'What name numerology reads', 'Name as public vibration'),
      link('/blog/personal-year-guide', 'Personal year timing guide', 'The annual cycle layer'),
      link('/number-4-and-8-compatibility', 'The 4 and 8 compatibility pattern', 'A core Chaldean caution'),
      link('/why-number-7-overthinks', 'Number 7 emotional depth', 'A sample stress-pattern page'),
      link('/number-6-in-love', 'Number 6 in love', 'A sample relationship-style page'),
      link('/lucky-attributes-number-8', 'Number 8 lucky attributes', 'A sample remedy page'),
      ...base,
    ], page.route, 12);
  }

  if (page.cluster === 'blog' || page.cluster === 'blog-hub') {
    return compactLinks([
      link('/name-numerology-calculator', 'Calculate your name number', 'Apply the guide to your own name'),
      link('/analyzer', 'Run the free full analysis', 'Birth, life path, name, alignment'),
      link('/number', 'Browse number meanings', 'Connect article concepts to archetypes'),
      link('/love-compatibility-numerology', 'Explore relationship compatibility', 'Turn number theory into a two-person read'),
      link('/name-correction-numerology', 'Check name correction options', 'When the name feels misaligned'),
      link('/business-name-numerology', 'Read a business name', 'Brand and venture vibration'),
      link('/report', 'Get the full report', 'Personalised PDF with timing'),
      link('/blog/chaldean-numerology-guide', 'Chaldean numerology guide', 'Method and tradition'),
      link('/blog/relationship-compatibility-numerology', 'Compatibility guide', 'How numbers meet emotionally'),
      link('/blog/name-correction-guide', 'Name correction guide', 'Practical naming decisions'),
      link('/blog/personal-year-guide', 'Personal year guide', 'Timing and cycles'),
    ], page.route, 10);
  }

  if (page.cluster === 'tool' || page.cluster === 'report' || page.cluster === 'home') {
    return compactLinks([
      link('/number', 'Understand your number archetype', 'Use after calculating'),
      link('/blog/what-is-name-numerology', 'What your name number means', 'A plain-language primer'),
      link('/blog/moolank-meanings', 'Read your Birth Number', 'The day-of-birth layer'),
      link('/blog/relationship-compatibility-numerology', 'Relationship compatibility guide', 'How two charts meet'),
      link('/love-compatibility-numerology', 'Compare a relationship', 'Try a second exploration path'),
      link('/name-correction-numerology', 'Check name correction', 'When the score needs context'),
      link('/business-name-numerology', 'Check a business name', 'For brands and ventures'),
      link('/report', 'Full destiny report', 'Deeper personalised PDF'),
      ...base,
    ], page.route, 10);
  }

  return compactLinks([...base, link('/blog/chaldean-numerology-guide', 'Read the Chaldean guide', 'Method behind the site'), link('/sitemap-pages', 'Browse the complete site map', 'All pages by cluster')], page.route, 8);
}

function sectionFor(page, items) {
  if (!items.length) return '';
  const title = page.cluster === 'compatibility'
    ? 'Related relationship insights'
    : page.cluster === 'emotional-pattern'
      ? 'Related emotional patterns'
      : 'Related insights';
  const lead = page.cluster === 'compatibility'
    ? 'After reading this pair, it helps to look at each person separately, then come back to the relationship as a living dynamic rather than a fixed verdict.'
    : page.nums.length
      ? `Number ${page.nums[0]} makes more sense when you move between personality, love, stress, career, and name-vibration pages. These are the closest next reads.`
      : 'Use these next paths to keep the exploration connected, from calculation to meaning to relationship context.';
  return `${MARKER_START}
<section class="na-related-insights" aria-labelledby="na-related-title">
  <div class="na-related-inner">
    <div class="na-related-kicker">Continue the pattern</div>
    <h2 id="na-related-title">${title}</h2>
    <p>${lead}</p>
    <div class="na-related-grid">
${items.map((item) => `      <a class="na-related-card" href="${item.href}"><span>${item.note}</span><strong>${item.title}</strong></a>`).join('\n')}
    </div>
  </div>
</section>
${MARKER_END}`;
}

function hubDiscoveryFor(page) {
  if (page.cluster === 'relationship-hub') {
    const pairs = pages
      .filter((p) => p.cluster === 'compatibility')
      .sort((a, b) => a.route.localeCompare(b.route));
    return `${HUB_START}
<section class="na-hub-discovery" aria-labelledby="na-compat-library">
  <div class="na-hub-inner">
    <div class="na-related-kicker">Compatibility library</div>
    <h2 id="na-compat-library">Explore specific number pairs</h2>
    <p>Use the tool for your own names and dates, then compare it with the closest pair page. Each page reads the emotional pace, conflict loop, repair style, and relationship strengths of that combination.</p>
    <div class="na-hub-link-grid">
${pairs.map((p) => `      <a href="${p.route}">${p.title.replace(' · Chaldean Numerology', '').replace(' | NameAligned', '')}</a>`).join('\n')}
    </div>
  </div>
</section>
${HUB_END}`;
  }

  if (page.cluster === 'number-hub') {
    return `${HUB_START}
<section class="na-hub-discovery" aria-labelledby="na-number-journeys">
  <div class="na-hub-inner">
    <div class="na-related-kicker">Depth paths</div>
    <h2 id="na-number-journeys">Move from number meaning into lived patterns</h2>
    <p>Once you know the number, the next layer is how it behaves in love, under pressure, in spiritual practice, and in everyday timing choices.</p>
    <div class="na-number-paths">
${[1,2,3,4,5,6,7,8,9].map((n) => `      <div class="na-number-path"><strong>Number ${n}</strong><a href="/number-${n}-in-love">Love style</a><a href="/why-number-${n}-overthinks">Stress pattern</a><a href="/number-${n}-spiritual-meaning">Spiritual meaning</a><a href="/lucky-attributes-number-${n}">Lucky attributes</a><a href="/number-${n}-and-${n}-compatibility">Same-number compatibility</a></div>`).join('\n')}
    </div>
  </div>
</section>
${HUB_END}`;
  }

  if (page.route === '/about' || page.route === '/methodology' || page.route === '/report') {
    return `${HUB_START}
<section class="na-hub-discovery" aria-labelledby="na-trust-paths">
  <div class="na-hub-inner">
    <div class="na-related-kicker">Trust and method</div>
    <h2 id="na-trust-paths">How the interpretation layer is built</h2>
    <p>These pages explain the calculation flow, name-alignment model, source posture, and AI-use boundaries behind the public tools.</p>
    <div class="na-hub-link-grid">
      <a href="/how-it-works">How NameAligned works</a>
      <a href="/name-alignment">How name alignment is scored</a>
      <a href="/methodology">Calculation methodology</a>
      <a href="/sources">Sources and tradition</a>
      <a href="/ai-disclosure">AI disclosure</a>
    </div>
  </div>
</section>
${HUB_END}`;
  }

  return '';
}

function crumbFor(page) {
  if (page.route === '/' || page.route === '/sitemap-pages') return '';
  let parent = { href: '/sitemap-pages', label: 'Site Map' };
  if (page.route.startsWith('/blog/')) parent = { href: '/blog', label: 'Blog' };
  if (page.route.startsWith('/number/')) parent = { href: '/number', label: 'Numbers' };
  if (page.cluster === 'compatibility' || page.cluster === 'relationship-hub') parent = { href: '/love-compatibility-numerology', label: 'Relationships' };
  if (['personality', 'career', 'identity', 'life-path', 'love-style', 'emotional-pattern', 'spiritual', 'lucky'].includes(page.cluster)) parent = { href: '/number', label: 'Numbers' };
  const label = page.title.split('|')[0].split('·')[0].trim();
  return `${BREAD_START}
<nav class="na-breadcrumb" aria-label="Breadcrumb">
  <a href="/">Home</a><span>/</span><a href="${parent.href}">${parent.label}</a><span>/</span><span>${label}</span>
</nav>
${BREAD_END}`;
}

function stripMarked(html, start, end) {
  const pattern = new RegExp(`${start.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}[\\s\\S]*?${end.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}\\n?`, 'g');
  return html.replace(pattern, '');
}

function ensureCssLink(html, rel) {
  const href = rel.includes('/') ? '/assets/internal-linking.css' : 'assets/internal-linking.css';
  if (html.includes('internal-linking.css')) return html;
  const linkTag = `<link rel="stylesheet" href="${href}"/>`;
  return html.replace(/<\/head>/i, `${linkTag}\n</head>`);
}

function ensurePrimaryNavLinks(html) {
  if (!/<nav\b[^>]*class=["'][^"']*\bnav\b/i.test(html)) return html;
  let next = html;
  next = next
    .replace(/href=(["'])analyzer\1/g, 'href="/analyzer"')
    .replace(/href=(["'])about\1/g, 'href="/about"')
    .replace(/href=(["'])report\1/g, 'href="/report"')
    .replace(/href=(["'])blog\1/g, 'href="/blog"')
    .replace(/href=(["'])name-numerology-calculator\1/g, 'href="/name-numerology-calculator"')
    .replace(/href=(["'])name-correction-numerology\1/g, 'href="/name-correction-numerology"')
    .replace(/href=(["'])business-name-numerology\1/g, 'href="/business-name-numerology"')
    .replace(/href=(["'])love-compatibility-numerology\1/g, 'href="/love-compatibility-numerology"')
    .replace(/href=(["'])sitemap-pages\1/g, 'href="/sitemap-pages"');
  if (!/href=["']\/number["']/.test(next)) {
    next = next.replace(/(<li><a href=["'][^"']*analyzer[^"']*["'][^>]*>[^<]*(?:Analysis|Analyser)[^<]*<\/a><\/li>)/i, `$1\n      <li><a href="/number">Numbers</a></li>\n      <li><a href="/love-compatibility-numerology">Compatibility</a></li>`);
  }
  if (/<div class=["']nav-mobile["']/.test(next) && !/class=["']nav-mobile["'][\s\S]*href=["']\/number["']/.test(next)) {
    next = next.replace(/(<div class=["']nav-mobile["'][^>]*>[\s\S]*?<a href=["'][^"']*analyzer[^"']*["'][^>]*>[^<]*<\/a>)/i, `$1\n    <a href="/number">Numbers</a>\n    <a href="/love-compatibility-numerology">Compatibility</a>`);
  }
  return next;
}

let changed = 0;
const audit = [];

for (const page of pages) {
  let html = fs.readFileSync(page.file, 'utf8');
  const before = html;
  html = stripMarked(html, MARKER_START, MARKER_END);
  html = stripMarked(html, HUB_START, HUB_END);
  html = stripMarked(html, BREAD_START, BREAD_END);
  html = ensureCssLink(html, page.rel);
  html = ensurePrimaryNavLinks(html);

  const items = linksFor(page);
  const hubDiscovery = hubDiscoveryFor(page);
  const related = sectionFor(page, items);
  const additions = `${hubDiscovery}${hubDiscovery && related ? '\n\n' : ''}${related}`;
  if (additions) {
    if (/<footer\b/i.test(html)) html = html.replace(/<footer\b/i, `${additions}\n\n<footer`);
    else html = html.replace(/<\/body>/i, `${additions}\n</body>`);
  }

  if (!/aria-label=["']Breadcrumb["']/i.test(html)) {
    const crumb = crumbFor(page);
    if (crumb) {
      if (/<nav\b[^>]*class=["'][^"']*\bnav\b[\s\S]*?<\/nav>/i.test(html)) {
        html = html.replace(/(<nav\b[^>]*class=["'][^"']*\bnav\b[\s\S]*?<\/nav>)/i, `$1\n\n${crumb}`);
      }
      else if (/<main\b/i.test(html)) html = html.replace(/<main\b/i, `${crumb}\n<main`);
      else if (/<header\b/i.test(html)) html = html.replace(/<header\b/i, `${crumb}\n<header`);
      else html = html.replace(/<body[^>]*>/i, (m) => `${m}\n${crumb}`);
    }
  }

  if (html !== before) {
    fs.writeFileSync(page.file, html);
    changed++;
  }
  audit.push({ route: page.route, cluster: page.cluster, relatedLinksAdded: items.length, file: page.rel });
}

const routes = new Set(pages.map((p) => p.route));
const inbound = new Map([...routes].map((r) => [r, 0]));
const outbound = new Map([...routes].map((r) => [r, 0]));
for (const page of pages) {
  const html = fs.readFileSync(page.file, 'utf8');
  const dom = new JSDOM(html);
  const links = [...dom.window.document.querySelectorAll('a[href]')]
    .map((a) => a.getAttribute('href').split('#')[0].replace(/\/$/, '') || '/')
    .filter((href) => href.startsWith('/') && routes.has(href) && href !== page.route);
  outbound.set(page.route, new Set(links).size);
  for (const href of new Set(links)) inbound.set(href, (inbound.get(href) || 0) + 1);
}

const weak = [...routes]
  .map((route) => ({ route, inbound: inbound.get(route) || 0, outbound: outbound.get(route) || 0 }))
  .filter((row) => row.inbound < 3 || row.outbound < 5)
  .sort((a, b) => a.inbound - b.inbound || a.outbound - b.outbound);

fs.mkdirSync(path.join(ROOT, 'docs', 'seo-urls'), { recursive: true });
fs.writeFileSync(path.join(ROOT, 'docs', 'seo-urls', 'internal-linking-audit.json'), JSON.stringify({
  generatedAt: new Date().toISOString(),
  pagesProcessed: pages.length,
  pagesChanged: changed,
  weakPagesRemaining: weak,
  pages: audit.map((row) => ({ ...row, inbound: inbound.get(row.route) || 0, outbound: outbound.get(row.route) || 0 })),
}, null, 2));

console.log(JSON.stringify({ pagesProcessed: pages.length, pagesChanged: changed, noindexCleaned, weakPagesRemaining: weak.length }, null, 2));
