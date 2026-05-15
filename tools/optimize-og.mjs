/**
 * Convert /assets/og/moolank-*.png to WebP + a JPEG fallback.
 *
 * Why: each PNG is ~450 KB. Crawlers + share-target previews download these,
 * and on /share/N.html they are also used as og:image, which Google reads
 * during indexing. WebP at quality 82 is visually identical and ~80% smaller.
 *
 * Output:
 *   /assets/og/moolank-N.webp   (primary, ~50 KB each)
 *   /assets/og/moolank-N.jpg    (fallback for old crawlers, ~120 KB each)
 *
 * Originals are kept (don't break old shared links).
 *
 * Run:
 *   node tools/optimize-og.mjs
 */

import sharp from 'sharp';
import { readdir, stat } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const OG_DIR    = path.join(__dirname, '..', 'assets', 'og');

async function main() {
  const files = (await readdir(OG_DIR)).filter(f => /^moolank-\d+\.png$/.test(f));
  if (!files.length) {
    console.error('No moolank-*.png files found in ' + OG_DIR);
    process.exit(1);
  }
  console.log('Converting ' + files.length + ' OG cards...');

  for (const f of files) {
    const src = path.join(OG_DIR, f);
    const base = f.replace(/\.png$/, '');
    const webpOut = path.join(OG_DIR, base + '.webp');
    const jpgOut  = path.join(OG_DIR, base + '.jpg');

    const before = (await stat(src)).size;

    await sharp(src).webp({ quality: 82, effort: 5 }).toFile(webpOut);
    await sharp(src).jpeg({ quality: 86, mozjpeg: true }).toFile(jpgOut);

    const webpSize = (await stat(webpOut)).size;
    const jpgSize  = (await stat(jpgOut)).size;
    console.log(
      '  ' + f
      + ' : png=' + (before / 1024).toFixed(0) + ' KB'
      + ' -> webp=' + (webpSize / 1024).toFixed(0) + ' KB'
      + ' jpg=' + (jpgSize / 1024).toFixed(0) + ' KB'
    );
  }
  console.log('Done.');
}

main().catch(err => { console.error(err); process.exit(1); });
