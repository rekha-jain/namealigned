'use strict';

const puppeteer = require('puppeteer');
const http      = require('http');
const fs        = require('fs');
const path      = require('path');

const ROOT = path.resolve(__dirname);
const PORT = 4445;

const MIME = {
  '.html':'text/html','.css':'text/css','.js':'application/javascript',
  '.json':'application/json','.png':'image/png','.jpg':'image/jpeg',
  '.svg':'image/svg+xml','.ico':'image/x-icon','.woff2':'font/woff2',
};

const server = http.createServer((req, res) => {
  let filePath = path.join(ROOT, req.url.split('?')[0]);
  if (filePath === ROOT || filePath.endsWith('/')) filePath = path.join(filePath, 'index.html');
  const ext = path.extname(filePath);
  fs.readFile(filePath, (err, data) => {
    if (err) { res.writeHead(404); res.end('Not found'); return; }
    res.writeHead(200, { 'Content-Type': MIME[ext] || 'application/octet-stream' });
    res.end(data);
  });
});

async function main() {
  await new Promise(resolve => server.listen(PORT, resolve));
  console.log(`Local server on http://localhost:${PORT}`);

  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox'],
  });

  const params = new URLSearchParams({
    paymentId: 'pay_SiRjbII0bqHyzM',
    name:      'Rekha Jain',
    dob:       '1981-03-15',
    email:     'jainrekha1313@gmail.com',
    mobile:    '9930459453',
    birthNum:  '6',
    destNum:   '1',
    nameNum:   '5',
  });

  const url = `http://localhost:${PORT}/generate-report.html?${params}`;
  console.log(`Rendering: ${url}`);

  const page = await browser.newPage();
  await page.setViewport({ width: 1280, height: 900 });
  await page.goto(url, { waitUntil: 'networkidle0', timeout: 30000 });

  // Wait for JS loader to finish and report to be visible
  await page.waitForFunction(
    () => {
      const wrap = document.getElementById('reportWrap');
      return wrap && wrap.style.display !== 'none' && wrap.style.display !== '';
    },
    { timeout: 15000 }
  );

  // Extra settle for animations
  await new Promise(r => setTimeout(r, 1500));

  const outPDF = path.join(ROOT, 'docs', 'sample-reports', 'Rekha_Jain_Report.pdf');
  fs.mkdirSync(path.dirname(outPDF), { recursive: true });

  await page.pdf({
    path:            outPDF,
    format:          'A4',
    printBackground: true,
    margin:          { top: '14mm', right: '12mm', bottom: '14mm', left: '12mm' },
    displayHeaderFooter: true,
    headerTemplate: `<div style="font-size:8.5px;font-family:sans-serif;color:#9ca3af;
                      width:100%;text-align:center;padding-top:5px;">
                      NameAligned.com · Chaldean Numerology Personal Destiny Report</div>`,
    footerTemplate: `<div style="font-size:8.5px;font-family:sans-serif;color:#9ca3af;
                      width:100%;text-align:center;padding-bottom:5px;">
                      Your Numerology Report
                      &nbsp;·&nbsp; Page <span class="pageNumber"></span> of <span class="totalPages"></span></div>`,
  });

  const kb = Math.round(fs.statSync(outPDF).size / 1024);
  console.log(`✅  PDF saved: ${outPDF}  (${kb} KB)`);

  await page.close();
  await browser.close();
  server.close();
}

main().catch(err => {
  console.error('❌ Error:', err.message);
  process.exit(1);
});
