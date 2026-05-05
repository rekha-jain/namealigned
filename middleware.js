/**
 * Vercel Edge Middleware — HTTP Basic Auth gate for staging URLs.
 *
 * Runs on the edge before any static asset / serverless function is
 * served. The password lives only in the STAGING_PASSWORD env var on
 * Vercel and is never sent to the browser. Anyone hitting a matched
 * path without correct credentials gets a 401 + browser auth dialog.
 *
 * Required env on Vercel (Production + Preview):
 *   STAGING_PASSWORD   — the password to enter (username is ignored)
 *
 * To rotate: change STAGING_PASSWORD in Vercel → Settings → Env Vars
 * and redeploy. All cached browser creds become invalid immediately.
 */

export const config = {
  // Gate the staging entry page (cleanUrl + .html form). Add more
  // paths here later if more staging surfaces appear.
  matcher: ['/staging-report', '/staging-report.html'],
};

export default function middleware(request) {
  const password = process.env.STAGING_PASSWORD || '';

  // Fail closed if the env var isn't configured — better a clear
  // 503 than an accidentally-public page.
  if (!password) {
    return new Response(
      'Staging gate not configured. Set STAGING_PASSWORD env var on Vercel.',
      { status: 503, headers: { 'Content-Type': 'text/plain' } }
    );
  }

  const auth = request.headers.get('authorization') || '';
  if (auth.startsWith('Basic ')) {
    try {
      const decoded = atob(auth.slice(6));
      // Username is ignored; only the password after the first ':'
      // matters. This lets the browser show "Sign in" with any user.
      const idx = decoded.indexOf(':');
      const supplied = idx >= 0 ? decoded.slice(idx + 1) : decoded;
      if (timingSafeEqual(supplied, password)) {
        return; // authenticated — continue to static page
      }
    } catch (_) { /* fall through to 401 */ }
  }

  return new Response('Authentication required', {
    status: 401,
    headers: {
      'WWW-Authenticate': 'Basic realm="NameAligned Staging", charset="UTF-8"',
      'Content-Type': 'text/plain',
      'Cache-Control': 'no-store',
    },
  });
}

// Constant-time string compare to prevent timing-attack guesses.
function timingSafeEqual(a, b) {
  if (typeof a !== 'string' || typeof b !== 'string') return false;
  if (a.length !== b.length) return false;
  let mismatch = 0;
  for (let i = 0; i < a.length; i++) {
    mismatch |= a.charCodeAt(i) ^ b.charCodeAt(i);
  }
  return mismatch === 0;
}
