/**
 * One-off script: injects OG, Twitter Card and Article JSON-LD into every
 * blog HTML file. Idempotent — re-running is a no-op.
 *
 * Usage:  node inject-blog-seo.cjs
 */

'use strict';

const fs   = require('fs');
const path = require('path');

const BLOG_DIR = path.join(__dirname, 'blog');
const SITE_URL = 'https://namealigned.com';
const OG_IMAGE = SITE_URL + '/assets/namealigned-logo-full.svg';

// Map filename → published date for Article schema (best-effort; can be updated)
const PUBLISHED = {
  'chaldean-numerology-guide.html':           '2025-09-15',
  'name-correction-guide.html':               '2025-09-22',
  'name-numerology-business.html':            '2025-10-05',
  'moolank-meanings.html':                    '2025-10-12',
  'relationship-compatibility-numerology.html':'2025-10-20',
  'lo-shu-grid-guide.html':                   '2025-11-02',
  'personal-year-guide.html':                 '2025-11-10',
  'lucky-numbers-india.html':                 '2025-11-18',
  'number-4-8-cheiro.html':                   '2025-12-01',
  'compound-numbers-cheiro.html':             '2025-12-15',
};
const MODIFIED = '2026-04-27';

function escAttr(s){
  return s.replace(/&(?!amp;|lt;|gt;|quot;|#)/g,'&amp;')
          .replace(/"/g,'&quot;');
}

function buildSeoBlock(opts){
  const { title, description, url, type, datePublished, dateModified } = opts;
  const t  = escAttr(title);
  const d  = escAttr(description);

  let block =
`<meta name="author" content="NameAligned.com"/>
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1"/>
<meta property="og:title" content="${t}"/>
<meta property="og:description" content="${d}"/>
<meta property="og:type" content="${type}"/>
<meta property="og:url" content="${url}"/>
<meta property="og:site_name" content="NameAligned.com"/>
<meta property="og:locale" content="en_IN"/>
<meta property="og:image" content="${OG_IMAGE}"/>
<meta property="og:image:alt" content="${t}"/>
<meta name="twitter:card" content="summary_large_image"/>
<meta name="twitter:title" content="${t}"/>
<meta name="twitter:description" content="${d}"/>
<meta name="twitter:image" content="${OG_IMAGE}"/>`;

  if(type === 'article'){
    const ld = {
      '@context':'https://schema.org',
      '@type':'Article',
      headline: title,
      description,
      url,
      image: OG_IMAGE,
      datePublished,
      dateModified,
      inLanguage:'en-IN',
      author: { '@type':'Organization', name:'NameAligned.com', url: SITE_URL+'/' },
      publisher: {
        '@type':'Organization',
        name:'NameAligned.com',
        logo:{ '@type':'ImageObject', url: OG_IMAGE }
      },
      mainEntityOfPage: { '@type':'WebPage', '@id': url }
    };
    block += `\n<script type="application/ld+json">\n${JSON.stringify(ld)}\n</script>`;
  } else if(type === 'website'){
    const ld = {
      '@context':'https://schema.org',
      '@type':'Blog',
      name:'NameAligned Blog',
      description,
      url,
      inLanguage:'en-IN',
      publisher:{
        '@type':'Organization',
        name:'NameAligned.com',
        logo:{ '@type':'ImageObject', url: OG_IMAGE }
      }
    };
    block += `\n<script type="application/ld+json">\n${JSON.stringify(ld)}\n</script>`;
  }
  return block;
}

function processFile(file){
  const full = path.join(BLOG_DIR, file);
  let html = fs.readFileSync(full, 'utf8');

  // Idempotency guard
  if(html.includes('property="og:url"')){
    console.log(`  skip  ${file}  (already has OG tags)`);
    return false;
  }

  // Extract title
  const tMatch = html.match(/<title>([^<]+)<\/title>/);
  if(!tMatch){ console.log(`  skip  ${file}  (no <title>)`); return false; }
  const title = tMatch[1].trim()
                  .replace(/&amp;/g,'&').replace(/&quot;/g,'"');

  // Extract description
  const dMatch = html.match(/<meta name="description" content="([^"]+)"/);
  const description = dMatch ? dMatch[1] : '';

  // Determine URL & type
  const isIndex = file === 'index.html';
  const url = SITE_URL + '/blog/' + (isIndex ? '' : file);
  const type = isIndex ? 'website' : 'article';

  const datePublished = PUBLISHED[file] || '2025-09-01';
  const dateModified  = MODIFIED;

  const block = buildSeoBlock({ title, description, url, type, datePublished, dateModified });

  // Insert immediately after the <link rel="canonical" .../> line.
  // For files that don't have one yet, insert after <meta name="description">.
  let inserted = false;
  if(/<link rel="canonical"[^>]+>/.test(html)){
    html = html.replace(/(<link rel="canonical"[^>]+>)/, `$1\n${block}`);
    inserted = true;
  } else if(/<meta name="description"[^>]+>/.test(html)){
    const canonicalLine = `<link rel="canonical" href="${url}"/>`;
    html = html.replace(
      /(<meta name="description"[^>]+>)/,
      `$1\n${canonicalLine}\n${block}`
    );
    inserted = true;
  }

  if(!inserted){ console.log(`  skip  ${file}  (no insertion point)`); return false; }

  fs.writeFileSync(full, html);
  console.log(`  ok    ${file}`);
  return true;
}

function main(){
  const files = fs.readdirSync(BLOG_DIR).filter(f => f.endsWith('.html'));
  console.log(`Processing ${files.length} blog file(s) in ${BLOG_DIR}\n`);
  let count = 0;
  for(const f of files){ if(processFile(f)) count++; }
  console.log(`\nUpdated ${count} file(s).`);
}

main();
