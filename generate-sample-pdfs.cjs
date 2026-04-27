/**
 * generate-sample-pdfs.js
 * Spins up a local HTTP server, renders 5 sample paid reports in
 * headless Chrome, and saves each as a PDF in docs/sample-reports/.
 *
 * Usage:  node generate-sample-pdfs.js
 */

'use strict';

const puppeteer = require('puppeteer');
const http      = require('http');
const fs        = require('fs');
const path      = require('path');

// ── 1. SAMPLE PROFILES ───────────────────────────────────────────
// Each will generate a fully personalised Chaldean report.
const SAMPLES = [
  {
    name:      'Rekha Jain',
    dob:       '1985-06-22',   // Moolank 4 (day 22 → 4), various destiny
    email:     'rekha.jain@example.com',
    paymentId: 'TEST_PAY_001',
  },
  {
    name:      'Arjun Sharma',
    dob:       '1990-03-15',   // Moolank 6
    email:     'arjun.sharma@example.com',
    paymentId: 'TEST_PAY_002',
  },
  {
    name:      'Priya Mehta',
    dob:       '1988-11-08',   // Moolank 8
    email:     'priya.mehta@example.com',
    paymentId: 'TEST_PAY_003',
  },
  {
    name:      'Vikram Singh',
    dob:       '1992-07-04',   // Moolank 4
    email:     'vikram.singh@example.com',
    paymentId: 'TEST_PAY_004',
  },
  {
    name:      'Sunita Patel',
    dob:       '1975-09-27',   // Moolank 9
    email:     'sunita.patel@example.com',
    paymentId: 'TEST_PAY_005',
  },
];

// ── 2. TINY STATIC FILE SERVER ────────────────────────────────────
const ROOT = path.resolve(__dirname);
const PORT = 4444;

const MIME = {
  '.html': 'text/html',
  '.css':  'text/css',
  '.js':   'application/javascript',
  '.json': 'application/json',
  '.png':  'image/png',
  '.jpg':  'image/jpeg',
  '.svg':  'image/svg+xml',
  '.ico':  'image/x-icon',
  '.woff2':'font/woff2',
};

const server = http.createServer((req, res) => {
  let filePath = path.join(ROOT, req.url.split('?')[0]);
  if (filePath === ROOT || filePath.endsWith('/')) filePath = path.join(filePath, 'index.html');

  const ext  = path.extname(filePath);
  const mime = MIME[ext] || 'application/octet-stream';

  fs.readFile(filePath, (err, data) => {
    if (err) { res.writeHead(404); res.end('Not found'); return; }
    res.writeHead(200, { 'Content-Type': mime });
    res.end(data);
  });
});

// ── 3. MAIN ───────────────────────────────────────────────────────
async function main() {
  // Ensure output folder exists
  const outDir = path.join(ROOT, 'docs', 'sample-reports');
  fs.mkdirSync(outDir, { recursive: true });

  // Start local server
  await new Promise(resolve => server.listen(PORT, resolve));
  console.log(`\n📡  Local server running on http://localhost:${PORT}`);

  // Launch Puppeteer
  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox'],
  });

  for (const [i, profile] of SAMPLES.entries()) {
    const idx    = String(i + 1).padStart(2, '0');
    const label  = profile.name.replace(/\s+/g, '_');
    const outPDF = path.join(outDir, `${idx}_${label}.pdf`);

    const params = new URLSearchParams({
      paymentId: profile.paymentId,
      name:      profile.name,
      dob:       profile.dob,
      email:     profile.email,
      // birthNum / destNum / nameNum / pct intentionally omitted —
      // the page JS recomputes them from name + dob.
    });

    const url = `http://localhost:${PORT}/generate-report.html?${params}`;
    console.log(`\n[${idx}/05] ${profile.name}  (${profile.dob})`);
    console.log(`       ${url}`);

    const page = await browser.newPage();
    await page.setViewport({ width: 1280, height: 900 });

    // Navigate and wait for the loader overlay to disappear
    await page.goto(url, { waitUntil: 'networkidle0', timeout: 30000 });

    // Wait for #reportWrap to be visible (loader finishes in ~4 s)
    await page.waitForFunction(
      () => {
        const wrap = document.getElementById('reportWrap');
        return wrap && wrap.style.display !== 'none' && wrap.style.display !== '';
      },
      { timeout: 15000 }
    );

    // Extra settle time for any animations / async rendering
    await new Promise(r => setTimeout(r, 1200));

    await page.pdf({
      path:              outPDF,
      format:            'A4',
      printBackground:   true,
      margin:            { top: '12mm', right: '12mm', bottom: '16mm', left: '12mm' },
      displayHeaderFooter: true,
      headerTemplate:    `<div style="font-size:9px;font-family:sans-serif;color:#9ca3af;
                            width:100%;text-align:center;padding-top:4px;">
                            NameAligned.com · Personalised Chaldean Numerology Report</div>`,
      footerTemplate:    `<div style="font-size:9px;font-family:sans-serif;color:#9ca3af;
                            width:100%;text-align:center;padding-bottom:4px;">
                            Page <span class="pageNumber"></span> of <span class="totalPages"></span>
                            &nbsp;·&nbsp; ${profile.name} &nbsp;·&nbsp; namealigned.com</div>`,
    });

    const stats = fs.statSync(outPDF);
    const kb    = Math.round(stats.size / 1024);
    console.log(`       ✓  Saved: ${path.basename(outPDF)}  (${kb} KB)`);

    await page.close();
  }

  await browser.close();
  server.close();

  console.log(`\n✅  All 5 PDFs saved to:  docs/sample-reports/\n`);
}

main().catch(err => {
  console.error('\n❌  Error:', err.message);
  process.exit(1);
});
