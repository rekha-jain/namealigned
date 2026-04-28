/**
 * Generate /i/1.html ... /i/9.html from share.html template.
 *
 * Each per-Moolank page is a near-clone of share.html but with hardcoded
 * og:image / twitter:image / og:url / og:title / og:description, so when
 * a crawler (WhatsApp, Twitter, Facebook, Telegram) fetches the URL it
 * sees the right preview image without needing to run JS.
 *
 * The page itself still derives `sMool` from URL (?m= or path), so the
 * client-side card renders correctly when a real visitor lands.
 *
 * Usage: node tools/build-share-pages.js
 */

import { readFile, writeFile, mkdir } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');

// Per-Moolank OG copy. Mirrors the planet/qualities so previews tease
// what the recipient is about to see.
const META = {
  1:{planet:'Sun',     theme:'Leadership · Confidence · Vitality'},
  2:{planet:'Moon',    theme:'Sensitivity · Intuition · Harmony'},
  3:{planet:'Jupiter', theme:'Expression · Optimism · Joy'},
  4:{planet:'Rahu',    theme:'Innovation · Logic · Structure'},
  5:{planet:'Mercury', theme:'Adaptability · Wit · Communication'},
  6:{planet:'Venus',   theme:'Harmony · Love · Aesthetics'},
  7:{planet:'Ketu',    theme:'Wisdom · Introspection · Depth'},
  8:{planet:'Saturn',  theme:'Discipline · Authority · Resilience'},
  9:{planet:'Mars',    theme:'Courage · Energy · Action'},
};

async function main(){
  const tplPath = path.join(ROOT, 'share.html');
  const tpl = await readFile(tplPath, 'utf8');
  const outDir = path.join(ROOT, 'i');
  await mkdir(outDir, { recursive: true });

  for(const m of Object.keys(META)){
    const { planet, theme } = META[m];
    const ogImage = `https://namealigned.com/assets/og/moolank-${m}.png`;
    const ogUrl   = `https://namealigned.com/i/${m}`;
    const title   = `A Moolank ${m} insight (${planet}) ✦`;
    const desc    = `${theme}. A 30-second Chaldean numerology insight that's surprisingly accurate.`;

    let html = tpl
      .replace(
        /<meta property="og:url"[^>]*\/?>/,
        `<meta property="og:url" content="${ogUrl}"/>`
      )
      .replace(
        /<meta property="og:image"[^>]*\/?>/,
        `<meta property="og:image" content="${ogImage}"/>`
      )
      .replace(
        /<meta property="og:title"[^>]*\/?>/,
        `<meta property="og:title" content="${title}"/>`
      )
      .replace(
        /<meta property="og:description"[^>]*\/?>/,
        `<meta property="og:description" content="${desc}"/>`
      )
      .replace(
        /<meta name="twitter:image"[^>]*\/?>/,
        `<meta name="twitter:image" content="${ogImage}"/>`
      )
      .replace(
        /<meta name="twitter:title"[^>]*\/?>/,
        `<meta name="twitter:title" content="${title}"/>`
      )
      .replace(
        /<meta name="twitter:description"[^>]*\/?>/,
        `<meta name="twitter:description" content="${desc}"/>`
      );

    // Ensure the page knows its Moolank even if URL has no ?m=, by injecting
    // a default just before the existing param-parse block.
    html = html.replace(
      /const params = new URLSearchParams\(location\.search\);/,
      `const params = new URLSearchParams(location.search);\n` +
      `if(!params.get('m')) params.set('m','${m}'); // path-baked default for /i/${m}`
    );

    const out = path.join(outDir, `${m}.html`);
    await writeFile(out, html);
    console.log('  ✓ wrote i/' + m + '.html');
  }
  console.log('\n✓ 9 per-Moolank share pages built');
}

main().catch(e => { console.error(e); process.exit(1); });
