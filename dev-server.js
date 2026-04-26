/**
 * NameAligned.com — Local Development Server
 * Serves all static files + mocks API endpoints
 * Usage: node dev-server.js
 */

const http = require('http');
const fs   = require('fs');
const path = require('path');
const url  = require('url');

const PORT = 3000;
const ROOT = __dirname;

const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.css':  'text/css',
  '.js':   'application/javascript',
  '.json': 'application/json',
  '.png':  'image/png',
  '.jpg':  'image/jpeg',
  '.ico':  'image/x-icon',
  '.svg':  'image/svg+xml',
  '.woff': 'font/woff',
  '.woff2':'font/woff2',
};

// ── Mock API handlers ──────────────────────────────────────────────────────
const API_HANDLERS = {
  '/api/capture-lead': (req, res) => {
    let body = '';
    req.on('data', c => body += c);
    req.on('end', () => {
      try {
        const data = JSON.parse(body || '{}');
        console.log('\n📧  [API] /api/capture-lead  →  lead captured (mock)');
        console.log('    name:', data.name, '| email:', data.email,
                    '| Moolank:', data.birthNum, '| Bhagyank:', data.destNum);
        res.writeHead(200, { 'Content-Type': 'application/json',
                             'Access-Control-Allow-Origin': '*' });
        res.end(JSON.stringify({ success: true, id: 'mock_' + Date.now() }));
      } catch(e) {
        res.writeHead(400, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: 'bad request' }));
      }
    });
  },

  '/api/generate-report': (req, res) => {
    let body = '';
    req.on('data', c => body += c);
    req.on('end', () => {
      try {
        const data = JSON.parse(body || '{}');
        console.log('\n💳  [API] /api/generate-report  →  payment verified (mock)');
        console.log('    paymentId:', data.paymentId || '(none)', '| name:', data.name);
        res.writeHead(200, { 'Content-Type': 'application/json',
                             'Access-Control-Allow-Origin': '*' });
        res.end(JSON.stringify({ success: true, verified: true }));
      } catch(e) {
        res.writeHead(400, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: 'bad request' }));
      }
    });
  },
};

// ── Static file helper ─────────────────────────────────────────────────────
function serveFile(filePath, res) {
  fs.readFile(filePath, (err, data) => {
    if (err) {
      res.writeHead(404, { 'Content-Type': 'text/html' });
      res.end('<h2>404 — Not found</h2><p>' + filePath + '</p>');
      return;
    }
    const ext  = path.extname(filePath).toLowerCase();
    const mime = MIME[ext] || 'application/octet-stream';
    res.writeHead(200, { 'Content-Type': mime });
    res.end(data);
  });
}

// ── Server ─────────────────────────────────────────────────────────────────
const server = http.createServer((req, res) => {
  const parsedUrl = url.parse(req.url);
  let pathname    = parsedUrl.pathname;

  // CORS preflight
  if (req.method === 'OPTIONS') {
    res.writeHead(204, {
      'Access-Control-Allow-Origin':  '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    });
    res.end();
    return;
  }

  // API mock routes (POST)
  if (req.method === 'POST' && API_HANDLERS[pathname]) {
    return API_HANDLERS[pathname](req, res);
  }

  // Static files
  // Strip query string, decode URI
  let filePath = path.join(ROOT, decodeURIComponent(pathname));

  // Default to index.html for directories
  if (pathname === '/' || pathname.endsWith('/')) {
    filePath = path.join(filePath, 'index.html');
  }

  // If no extension, try .html
  if (!path.extname(filePath)) {
    filePath += '.html';
  }

  console.log('GET', pathname);
  serveFile(filePath, res);
});

server.listen(PORT, () => {
  console.log('');
  console.log('╔════════════════════════════════════════════════════╗');
  console.log('║    ☽  NameAligned.com  —  Dev Server Running       ║');
  console.log('╠════════════════════════════════════════════════════╣');
  console.log('║                                                    ║');
  console.log('║  Home       →  http://localhost:' + PORT + '/             ║');
  console.log('║  Analyzer   →  http://localhost:' + PORT + '/analyzer     ║');
  console.log('║  Report     →  http://localhost:' + PORT + '/report       ║');
  console.log('║  Blog       →  http://localhost:' + PORT + '/blog/        ║');
  console.log('║  About      →  http://localhost:' + PORT + '/about        ║');
  console.log('║                                                    ║');
  console.log('║  Test paid report page (no real payment needed):  ║');
  console.log('║  http://localhost:' + PORT + '/generate-report?          ║');
  console.log('║    paymentId=pay_test&name=Rekha+Jain&            ║');
  console.log('║    dob=1985-05-14&email=test@test.com&            ║');
  console.log('║    birthNum=5&destNum=6&nameNum=3&pct=82          ║');
  console.log('║                                                    ║');
  console.log('║  API calls are mocked (no Supabase/Razorpay       ║');
  console.log('║  credentials needed). Responses logged above.     ║');
  console.log('║                                                    ║');
  console.log('║  Press Ctrl+C to stop                             ║');
  console.log('╚════════════════════════════════════════════════════╝');
  console.log('');
});
