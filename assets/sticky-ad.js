/* ═══════════════════════════════════════════════════════════════
   STICKY AD, fixed bottom bar that stays put while the page scrolls
   ───────────────────────────────────────────────────────────────
   Loaded with one tag before </body> on content pages:
     <script src="/assets/sticky-ad.js?v=..." defer></script>

   - Default: "Free name analysis" → /analyzer (desktop + mobile).
   - /analyzer: hidden until the free results show (#page2 visible),
     then promotes the paid full report → /report.
   - Pages with the blog sidebar ad (.article-sidebar) already have a
     desktop ad, so the bar shows on mobile only there.
   - Pages that hand-code their own .sticky-cta keep it; we just make
     it visible on desktop too.
   - Dismissible (×), remembered for the browser session.
   ═══════════════════════════════════════════════════════════════ */
(function () {
  'use strict';

  var DISMISS_KEY = 'na_sticky_ad_dismissed';
  var path = window.location.pathname.replace(/\.html$/, '').replace(/\/$/, '') || '/';
  var isAnalyzer = path === '/analyzer';

  function dismissed() {
    try { return sessionStorage.getItem(DISMISS_KEY) === '1'; } catch (e) { return false; }
  }
  if (dismissed()) return;

  var css = [
    '.sticky-cta.na-sticky-all{display:flex}',
    '.sticky-cta{align-items:center;justify-content:space-between;gap:.75rem;padding:.7rem 1rem;z-index:9990;box-shadow:0 -6px 24px rgba(10,8,32,.12)}',
    '.na-sticky-inner{display:flex;align-items:center;justify-content:space-between;gap:1rem;width:100%;max-width:1100px;margin:0 auto}',
    '.na-sticky-actions{display:flex;align-items:center;gap:.5rem;flex-shrink:0}',
    '.na-sticky-x{background:none;border:0;color:var(--text3,#888);font-size:20px;line-height:1;cursor:pointer;padding:4px 6px}',
    '.na-sticky-x:hover{color:var(--text,#222)}',
    '.na-btn-short{display:none}',
    'body.na-has-sticky{padding-bottom:calc(var(--na-sticky-h,70px) + 4px)}',
    'body.na-has-sticky #aura-fab{bottom:calc(var(--na-sticky-h,70px) + 8px)}',
    '@media(max-width:700px){.sticky-cta[data-na-sticky] .sticky-cta-text span{display:none}.na-btn-long{display:none}.na-btn-short{display:inline}.sticky-cta[data-na-sticky]{padding:.6rem .85rem}}',
    '@media(min-width:701px){body.na-sticky-mobile-only.na-has-sticky{padding-bottom:0}body.na-sticky-mobile-only.na-has-sticky #aura-fab{bottom:12px}}',
    '@media print{.sticky-cta{display:none!important}body.na-has-sticky{padding-bottom:0}}'
  ].join('');

  function addStyles() {
    var s = document.createElement('style');
    s.id = 'na-sticky-ad-css';
    s.textContent = css;
    document.head.appendChild(s);
  }

  function build(opts) {
    var bar = document.createElement('div');
    bar.className = 'sticky-cta' + (opts.mobileOnly ? '' : ' na-sticky-all');
    bar.setAttribute('role', 'complementary');
    bar.setAttribute('aria-label', 'Promotion');
    bar.innerHTML =
      '<div class="na-sticky-inner">' +
        '<div class="sticky-cta-text"><strong></strong><span></span></div>' +
        '<div class="na-sticky-actions">' +
          '<a class="btn btn-gold btn-sm"></a>' +
          '<button type="button" class="na-sticky-x" aria-label="Close">×</button>' +
        '</div>' +
      '</div>';
    bar.querySelector('strong').textContent = opts.title;
    bar.querySelector('span').textContent = opts.sub;
    var a = bar.querySelector('a');
    a.href = opts.href;
    a.innerHTML = '<span class="na-btn-long"></span><span class="na-btn-short"></span>';
    a.querySelector('.na-btn-long').textContent = opts.button;
    a.querySelector('.na-btn-short').textContent = opts.buttonShort || opts.button;
    a.addEventListener('click', function () {
      if (window.trackEvent) window.trackEvent('sticky_ad_click', { page: path, target: opts.href });
    });
    bar.querySelector('.na-sticky-x').addEventListener('click', function () {
      try { sessionStorage.setItem(DISMISS_KEY, '1'); } catch (e) {}
      bar.remove();
      document.body.classList.remove('na-has-sticky', 'na-sticky-mobile-only');
    });
    return bar;
  }

  function show(opts) {
    if (document.querySelector('.sticky-cta[data-na-sticky]')) return;
    var bar = build(opts);
    bar.setAttribute('data-na-sticky', '1');
    document.body.appendChild(bar);
    document.body.classList.add('na-has-sticky');
    if (opts.mobileOnly) document.body.classList.add('na-sticky-mobile-only');
    trackHeight(bar);
  }

  // Keep page padding and the Aura button clear of the bar at any height.
  function trackHeight(bar) {
    var set = function () {
      document.documentElement.style.setProperty('--na-sticky-h', bar.offsetHeight + 'px');
    };
    set();
    window.addEventListener('resize', set);
  }

  function init() {
    addStyles();

    // Page already hand-codes a mobile .sticky-cta (home, about): show it everywhere.
    var existing = document.querySelector('.sticky-cta');
    if (existing) {
      existing.classList.add('na-sticky-all');
      document.body.classList.add('na-has-sticky');
      trackHeight(existing);
      return;
    }

    var mobileOnly = !!document.querySelector('.article-sidebar');

    if (isAnalyzer) {
      var reportAd = {
        title: 'Your complete report',
        sub: '3 name-correction options · 5-year forecast · career & love',
        button: 'Get it · $2.50 / ₹249 →',
        buttonShort: '$2.50 / ₹249 →',
        href: '/report',
        mobileOnly: false
      };
      var page2 = document.getElementById('page2');
      if (!page2) return;
      var check = function () { if (getComputedStyle(page2).display !== 'none') show(reportAd); };
      check();
      new MutationObserver(check).observe(page2, { attributes: true, attributeFilter: ['style', 'class'] });
      return;
    }

    show({
      title: 'Free name analysis',
      sub: 'Takes 60 seconds · No account',
      button: 'Start →',
      href: '/analyzer',
      mobileOnly: mobileOnly
    });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
