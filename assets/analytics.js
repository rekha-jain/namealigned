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

  // ── Engagement events (v2 emotional layer) ──────────────────
  // Convenience wrappers so call sites do not have to remember exact
  // parameter names. Each wrapper enforces a consistent shape and
  // auto-attaches source_page + device_type.
  const events = {
    analyzerStarted: function(p) {
      trackEvent('analyzer_started', Object.assign({ source_page: sourcePage(), device_type: deviceType() }, p || {}));
    },
    analyzerCompleted: function(p) {
      // p: { number, name_number, birth_number, life_path }
      trackEvent('analyzer_completed', Object.assign({ source_page: sourcePage() }, p || {}));
    },
    compatibilityStarted: function(p) {
      trackEvent('compatibility_started', Object.assign({ source_page: sourcePage(), device_type: deviceType() }, p || {}));
    },
    compatibilityCompleted: function(p) {
      // p: { relationship_type, dynamic_type, score_range, archetype }
      trackEvent('compatibility_completed', Object.assign({ source_page: sourcePage() }, p || {}));
    },
    compatibilityShared: function(p) {
      // p: { share_method ('whatsapp'|'copy'|'native'), relationship_type, archetype }
      trackEvent('compatibility_shared', Object.assign({ source_page: sourcePage() }, p || {}));
    },
    shareWhatsApp: function(p) {
      // p: { source ('insight_card'|'pair_insight'|'compatibility_result'|...) }
      trackEvent('share_whatsapp', Object.assign({ source_page: sourcePage() }, p || {}));
    },
    shareCopy: function(p) {
      trackEvent('share_copy', Object.assign({ source_page: sourcePage() }, p || {}));
    },
    archetypeViewed: function(p) {
      // p: { archetype, number }
      trackEvent('archetype_viewed', Object.assign({ source_page: sourcePage() }, p || {}));
    },
    relatedInsightClicked: function(p) {
      // p: { from_page, to_page, link_text }
      trackEvent('related_insight_clicked', Object.assign({ source_page: sourcePage() }, p || {}));
    },
    reportClicked: function(p) {
      // p: { source ('cta_band'|'sidebar'|'footer'|'analyzer_result'|...) }
      trackEvent('report_clicked', Object.assign({ source_page: sourcePage() }, p || {}));
    },
    checkAnotherRelationship: function(p) {
      // p: { from_result, relationship_type }
      trackEvent('check_another_relationship', Object.assign({ source_page: sourcePage() }, p || {}));
    },
    insightCopied: function(p) {
      trackEvent('insight_copied', Object.assign({ source_page: sourcePage() }, p || {}));
    },
  };

  // Auto-instrumentation: any element with [data-na-event] fires that
  // event on click. Optional [data-na-params] is a JSON string of params.
  // Makes it easy to instrument new CTAs in HTML without touching JS.
  function bindAutoEvents(root) {
    (root || document).querySelectorAll('[data-na-event]').forEach((el) => {
      if (el.__naEventBound) return;
      el.__naEventBound = true;
      el.addEventListener('click', function() {
        const name = el.getAttribute('data-na-event');
        let params = {};
        const raw = el.getAttribute('data-na-params');
        if (raw) { try { params = JSON.parse(raw); } catch (e) {} }
        trackEvent(name, Object.assign({ source_page: sourcePage(), device_type: deviceType() }, params));
      }, { passive: true });
    });
  }
  if (typeof document !== 'undefined') {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', function(){ bindAutoEvents(); });
    } else {
      bindAutoEvents();
    }
  }

  // ── Expose ──────────────────────────────────────────────────
  g.NA = g.NA || {};
  g.NA.track       = trackEvent;
  g.NA.events      = events;
  g.NA.bindAutoEvents = bindAutoEvents;
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
