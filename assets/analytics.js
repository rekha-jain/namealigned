/* ═══════════════════════════════════════════════════════════════
   NameAligned — lightweight GA4 analytics helper
   ═══════════════════════════════════════════════════════════════
   Single trackEvent() wrapper that fans out to gtag (GA4), dataLayer
   (Tag Manager-compatible), Mixpanel (if naTrack is loaded), and
   console (dev). Safe to call before gtag has loaded, and on pages
   where gtag is absent.

   Conventions
   - Event names are lowercase_snake_case (GA4 best practice).
   - Parameter names are lowercase_snake_case.
   - Free-text values are clamped to 100 chars (GA4 limit is 100).
   - Numeric values use _range buckets where appropriate (cardinality
     control). Raw numbers fire too where they're useful as Custom
     Metrics.
   - Boolean values fire as 1/0 (GA4 prefers numeric).
   ═══════════════════════════════════════════════════════════════ */
(function (g) {
  'use strict';

  // ── Core dispatcher ──────────────────────────────────────────
  function trackEvent(name, params) {
    if (!name) return;
    const safe = sanitize(params || {});
    try {
      if (g.dataLayer && typeof g.dataLayer.push === 'function') {
        g.dataLayer.push(Object.assign({ event: name }, safe));
      }
    } catch (e) {}
    try {
      if (typeof g.gtag === 'function') {
        g.gtag('event', name, safe);
      }
    } catch (e) {}
    try {
      if (typeof g.naTrack === 'function') {
        g.naTrack(name, safe);
      }
    } catch (e) {}
    try {
      if (g.console && g.console.debug) g.console.debug('[track]', name, safe);
    } catch (e) {}
  }

  // ── Param sanitiser ──────────────────────────────────────────
  // GA4 caps param value length at 100 chars and rejects non-scalar
  // values. Strip undefined, coerce booleans to 0/1.
  function sanitize(o) {
    const out = {};
    for (const k in o) {
      let v = o[k];
      if (v === null || v === undefined) continue;
      if (typeof v === 'boolean') v = v ? 1 : 0;
      if (typeof v === 'object') v = JSON.stringify(v);
      if (typeof v === 'string' && v.length > 100) v = v.slice(0, 100);
      out[k] = v;
    }
    return out;
  }

  // ── Helpers ─────────────────────────────────────────────────
  // Score buckets keep GA4 cardinality low while preserving signal.
  function scoreRange(pct) {
    if (pct == null || isNaN(pct)) return 'unknown';
    if (pct >= 85) return '85_100';
    if (pct >= 70) return '70_84';
    if (pct >= 55) return '55_69';
    if (pct >= 40) return '40_54';
    if (pct >= 25) return '25_39';
    return '0_24';
  }

  function deviceType() {
    try {
      const ua = (navigator.userAgent || '').toLowerCase();
      if (/ipad|tablet|android(?!.*mobile)/.test(ua)) return 'tablet';
      if (/mobi|iphone|android/.test(ua)) return 'mobile';
      return 'desktop';
    } catch (e) { return 'unknown'; }
  }

  function sourcePage() {
    try {
      const p = (location.pathname || '/').replace(/\/$/, '') || '/';
      return p === '/' ? 'home' : p.replace(/^\/+/, '');
    } catch (e) { return 'unknown'; }
  }

  // Map Chaldean tier classes / labels to a stable emotional-dynamic
  // bucket the dashboard can group by.
  function dynamicType(tierCls) {
    return ({
      high: 'strong_harmony',
      mid:  'workable',
      low:  'needs_awareness',
    })[tierCls] || 'unknown';
  }

  // Map birth-number → archetype label (matches mini-analyzers.js).
  const ARCHETYPES = {
    1: 'The Trailblazer', 2: 'The Empath',     3: 'The Storyteller',
    4: 'The Maverick',    5: 'The Explorer',   6: 'The Harmonizer',
    7: 'The Seeker',      8: 'The Architect',  9: 'The Warrior',
  };
  function compatArchetype(yBirth, pBirth) {
    const a = ARCHETYPES[yBirth] || 'unknown';
    const b = ARCHETYPES[pBirth] || 'unknown';
    // Stable order so {1,2} and {2,1} bucket together.
    return (yBirth <= pBirth ? a + '_x_' + b : b + '_x_' + a)
      .toLowerCase().replace(/\s+/g, '_');
  }

  // ── Site-wide click delegation for cross-page CTAs ──────────
  // Fires report_clicked and compatibility_cta_clicked whenever a user
  // clicks any link pointing at /report or /love-compatibility-numerology
  // from any page on the site. Single listener, very low overhead.
  function bindCrossPageCTAs(){
    document.addEventListener('click', function (e) {
      const a = e.target && e.target.closest && e.target.closest('a[href]');
      if (!a) return;
      const href = (a.getAttribute('href') || '').toLowerCase();
      // /report (with or without leading slash, query strings allowed)
      if (/^(?:\/)?report(?:[?#/]|$)/.test(href)) {
        trackEvent('report_clicked', {
          source_page: sourcePage(),
          device_type: deviceType(),
        });
      }
      // /love-compatibility-numerology, the relationship tool entry
      if (/^(?:\/)?love-compatibility-numerology(?:[?#/]|$)/.test(href)) {
        // Skip if the click originates on the relationship tool page itself
        // (it would be self-link / internal jump).
        if (sourcePage() !== 'love-compatibility-numerology') {
          trackEvent('compatibility_cta_clicked', {
            source_page: sourcePage(),
            device_type: deviceType(),
          });
        }
      }
    }, { passive: true });
  }
  if (typeof document !== 'undefined') {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', bindCrossPageCTAs);
    } else {
      bindCrossPageCTAs();
    }
  }

  // ── Expose ──────────────────────────────────────────────────
  g.NA = g.NA || {};
  g.NA.track       = trackEvent;
  g.NA.scoreRange  = scoreRange;
  g.NA.deviceType  = deviceType;
  g.NA.sourcePage  = sourcePage;
  g.NA.dynamicType = dynamicType;
  g.NA.compatArchetype = compatArchetype;

  // Back-compat: keep the global `trackEvent()` used elsewhere.
  if (typeof g.trackEvent !== 'function') {
    g.trackEvent = trackEvent;
  }
})(typeof window !== 'undefined' ? window : globalThis);
