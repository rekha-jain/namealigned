/**
 * Pre-render 9 per-Moolank Open Graph cards (1200×630 PNG).
 *
 * For each Moolank 1..9, loads the local share page in headless Chromium,
 * waits for the canvas to render, and writes a PNG to /assets/og/moolank-N.png.
 *
 * These static PNGs are referenced as og:image in the per-Moolank share pages
 * (/share/1.html ... /share/9.html), so when someone shares the link on
 * WhatsApp/Twitter/Facebook the platform crawler fetches the correct image
 * without needing JS execution.
 *
 * Usage:
 *   node tools/render-og-cards.js
 *
 * Requires: puppeteer (already in package.json), and the dev-server must
 * be runnable on port 3000. The script spawns it itself and shuts it down.
 */

import { spawn } from 'node:child_process';
import { setTimeout as sleep } from 'node:timers/promises';
import { writeFile, mkdir } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import puppeteer from 'puppeteer';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT      = path.resolve(__dirname, '..');
const OUT_DIR   = path.join(ROOT, 'assets', 'og');
const PORT      = 3000;
const BASE      = `http://localhost:${PORT}`;

async function pingServer(url){
  try { const r = await fetch(url); return r.ok || r.status === 404; }
  catch(e){ return false; }
}
async function waitForServer(url, tries = 30){
  for(let i=0;i<tries;i++){
    if(await pingServer(url)) return;
    await sleep(250);
  }
  throw new Error('dev-server did not come up');
}

async function main(){
  await mkdir(OUT_DIR, { recursive: true });

  // 1. Boot dev-server (skip if something is already serving on PORT)
  let server = null;
  if(await pingServer(BASE + '/share?m=1')){
    console.log('▸ dev-server already up on :' + PORT + ' — reusing');
  } else {
    console.log('▸ starting dev-server on :' + PORT);
    // dev-server.js is CJS but package.json declares ESM, so invoke with -e wrapper
    // (or just call it; user can run `node dev-server.cjs` separately).
    server = spawn('node', ['--input-type=commonjs', '-e',
      `require(${JSON.stringify(path.join(ROOT,'dev-server.js'))})`], {
      cwd: ROOT,
      stdio: ['ignore', 'pipe', 'pipe'],
    });
    server.stdout.on('data', d => process.stdout.write('[dev] ' + d));
    server.stderr.on('data', d => process.stderr.write('[dev!] ' + d));
    await waitForServer(BASE + '/share?m=1');
  }

  // 2. Boot Chromium @ 1200×630
  const browser = await puppeteer.launch({
    headless: 'new',
    defaultViewport: { width: 1200, height: 630, deviceScaleFactor: 1 },
  });
  const page = await browser.newPage();

  try {
    for(let m = 1; m <= 9; m++){
      const url = `${BASE}/share?m=${m}`;
      console.log(`▸ rendering Moolank ${m}  (${url})`);
      await page.goto(url, { waitUntil: 'networkidle0', timeout: 30000 });

      // Wait for fonts + canvas paint
      await page.evaluate(() => document.fonts && document.fonts.ready);
      await sleep(400);

      // Pull the rendered card straight off the canvas as a PNG buffer
      const dataUrl = await page.evaluate(() => {
        const c = document.getElementById('shareCardCanvas');
        return c ? c.toDataURL('image/png') : null;
      });
      if(!dataUrl) throw new Error('canvas not found for moolank ' + m);

      const b64 = dataUrl.replace(/^data:image\/png;base64,/, '');
      const out = path.join(OUT_DIR, `moolank-${m}.png`);
      await writeFile(out, Buffer.from(b64, 'base64'));
      console.log('  ✓ wrote', path.relative(ROOT, out));
    }
  } finally {
    await browser.close();
    if(server) server.kill('SIGTERM');
  }

  console.log('\n✓ all 9 cards rendered → assets/og/');
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
