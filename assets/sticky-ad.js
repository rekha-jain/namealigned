/* ═══════════════════════════════════════════════════════════════
   STICKY AD, floating card pinned to the bottom of the screen
   ───────────────────────────────────────────────────────────────
   Loaded with one tag before </body> on content pages:
     <script src="/assets/sticky-ad.js?v=..." defer></script>

   - Default: free name analysis → /analyzer. Slides in after the
     reader scrolls a little, so it never covers the first screen.
   - /analyzer: hidden until the free results show (#page2 visible),
     then promotes the paid full report → /report (50% off).
   - Pages with the blog sidebar ad (.article-sidebar) already have a
     desktop ad, so the card shows on mobile only there.
   - Replaces any hand-coded .sticky-cta so every page looks the same.
   - Dismissible (×), remembered for the browser session.
   ═══════════════════════════════════════════════════════════════ */
(function () {
  'use strict';

  var DISMISS_KEY = 'na_sticky_ad_dismissed';
  var SCROLL_TRIGGER = 320;   // px scrolled before the free-analysis card appears
  var path = window.location.pathname.replace(/\.html$/, '').replace(/\/$/, '') || '/';
  var isAnalyzer = path === '/analyzer';

  try { if (sessionStorage.getItem(DISMISS_KEY) === '1') return; } catch (e) {}

  var css = [
    '.na-ad{position:fixed;left:12px;right:12px;bottom:12px;z-index:9990;display:flex;justify-content:center;pointer-events:none;',
      'transform:translateY(140%);opacity:0;transition:transform .5s cubic-bezier(.2,.9,.3,1.2),opacity .4s ease}',
    '.na-ad.na-ad-in{transform:none;opacity:1}',
    '.na-ad-card{pointer-events:auto;position:relative;display:flex;align-items:center;gap:14px;width:100%;max-width:880px;',
      'padding:12px 14px 12px 12px;border-radius:18px;color:#f0ece0;font-family:"DM Sans",system-ui,-apple-system,sans-serif;',
      'background:radial-gradient(120% 160% at 0% 0%,#3b2470 0%,#2a1a5c 45%,#160f38 100%);',
      'border:1px solid rgba(240,180,41,.45);',
      'box-shadow:0 18px 40px rgba(14,9,40,.45),0 0 0 1px rgba(255,255,255,.04) inset,0 0 28px rgba(240,180,41,.18)}',
    '.na-ad-icon{flex-shrink:0;width:44px;height:44px;border-radius:50%;display:grid;place-items:center;font-size:20px;color:#1a0533;',
      'background:linear-gradient(135deg,#f5d060,#f0b429);box-shadow:0 0 0 4px rgba(240,180,41,.18),0 6px 16px rgba(240,180,41,.35)}',
    '.na-ad-text{flex:1;min-width:0}',
    '.na-ad-badge{display:inline-block;margin-bottom:3px;padding:2px 8px;border-radius:999px;font-size:10px;font-weight:700;letter-spacing:.08em;',
      'text-transform:uppercase;color:#1a0533;background:#f0b429}',
    '.na-ad-title{font-family:"Playfair Display",Georgia,serif;font-size:17px;font-weight:700;line-height:1.25;color:#fff}',
    '.na-ad-sub{margin-top:2px;font-size:12.5px;line-height:1.4;color:rgba(240,236,224,.72)}',
    '.na-ad-price{margin-top:3px;font-size:13px;color:rgba(240,236,224,.8)}',
    '.na-ad-price s{opacity:.55;margin-right:4px}',
    '.na-ad-price b{color:#f5d060;font-weight:700;margin-right:8px}',
    '.na-ad-btn{position:relative;overflow:hidden;flex-shrink:0;display:inline-flex;align-items:center;gap:6px;padding:12px 20px;border-radius:999px;',
      'font-size:14.5px;font-weight:700;color:#1a0533;text-decoration:none;white-space:nowrap;',
      'background:linear-gradient(135deg,#f5d060 0%,#f0b429 60%,#e8a317 100%);',
      'box-shadow:0 8px 22px rgba(240,180,41,.45);transition:transform .15s ease,box-shadow .15s ease}',
    '.na-ad-btn:hover{transform:translateY(-2px);box-shadow:0 12px 28px rgba(240,180,41,.6);color:#1a0533}',
    '.na-ad-btn::after{content:"";position:absolute;top:0;left:-60%;width:40%;height:100%;',
      'background:linear-gradient(100deg,transparent,rgba(255,255,255,.65),transparent);transform:skewX(-20deg);animation:naAdShine 4.5s ease-in-out 1.2s infinite}',
    '@keyframes naAdShine{0%,70%{left:-60%}100%{left:130%}}',
    '.na-ad-x{position:absolute;top:-9px;right:-9px;width:24px;height:24px;border-radius:50%;border:1px solid rgba(255,255,255,.25);',
      'background:#160f38;color:rgba(255,255,255,.75);font-size:14px;line-height:1;cursor:pointer;display:grid;place-items:center;padding:0}',
    '.na-ad-x:hover{color:#fff;border-color:rgba(255,255,255,.5)}',
    '.na-btn-short{display:none}',
    'body.na-has-ad{padding-bottom:calc(var(--na-ad-h,80px) + 20px)}',
    'body.na-has-ad #aura-fab{bottom:calc(var(--na-ad-h,80px) + 22px)!important}',
    '@media(max-width:700px){',
      '.na-ad{left:8px;right:8px;bottom:8px}',
      '.na-ad-card{gap:10px;padding:10px;border-radius:16px}',
      '.na-ad-icon{width:36px;height:36px;font-size:16px}',
      '.na-ad-title{font-size:15px}',
      '.na-ad-sub{display:none}',
      '.na-ad-btn{padding:10px 14px;font-size:13.5px}',
      '.na-btn-long{display:none}.na-btn-short{display:inline}',
    '}',
    '@media(min-width:701px){body.na-ad-mobile-only .na-ad{display:none}',
      'body.na-ad-mobile-only.na-has-ad{padding-bottom:0}body.na-ad-mobile-only.na-has-ad #aura-fab{bottom:12px!important}}',
    '@media(prefers-reduced-motion:reduce){.na-ad{transition:none}.na-ad-btn::after{animation:none}}',
    '@media print{.na-ad{display:none!important}body.na-has-ad{padding-bottom:0}}'
  ].join('');

  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    return e;
  }

  function build(opts) {
    var wrap = el('div', 'na-ad');
    wrap.setAttribute('role', 'complementary');
    wrap.setAttribute('aria-label', 'Promotion');
    var card = el('div', 'na-ad-card');

    card.appendChild(el('div', 'na-ad-icon', opts.icon));

    var text = el('div', 'na-ad-text');
    if (opts.badge) text.appendChild(el('span', 'na-ad-badge', opts.badge));
    text.appendChild(el('div', 'na-ad-title', opts.title));
    if (opts.sub) text.appendChild(el('div', 'na-ad-sub', opts.sub));
    if (opts.price) {
      var p = el('div', 'na-ad-price');
      opts.price.forEach(function (pair) {
        p.appendChild(el('s', null, pair[0]));
        p.appendChild(el('b', null, pair[1]));
      });
      text.appendChild(p);
    }
    card.appendChild(text);

    var a = el('a', 'na-ad-btn');
    a.href = opts.href;
    a.appendChild(el('span', 'na-btn-long', opts.button));
    a.appendChild(el('span', 'na-btn-short', opts.buttonShort || opts.button));
    a.addEventListener('click', function () {
      if (window.trackEvent) window.trackEvent('sticky_ad_click', { page: path, target: opts.href });
    });
    card.appendChild(a);

    var x = el('button', 'na-ad-x', '×');
    x.type = 'button';
    x.setAttribute('aria-label', 'Close');
    x.addEventListener('click', function () {
      try { sessionStorage.setItem(DISMISS_KEY, '1'); } catch (e) {}
      wrap.classList.remove('na-ad-in');
      document.body.classList.remove('na-has-ad');
      setTimeout(function () { wrap.remove(); }, 450);
    });
    card.appendChild(x);

    wrap.appendChild(card);
    return wrap;
  }

  // Keep page padding and the Aura button clear of the card at any height.
  function trackHeight(card) {
    var set = function () {
      document.documentElement.style.setProperty('--na-ad-h', card.offsetHeight + 'px');
    };
    set();
    window.addEventListener('resize', set);
  }

  function show(opts) {
    if (document.querySelector('.na-ad')) return;
    var wrap = build(opts);
    document.body.appendChild(wrap);
    if (opts.mobileOnly) document.body.classList.add('na-ad-mobile-only');
    trackHeight(wrap.firstChild);
    requestAnimationFrame(function () {
      requestAnimationFrame(function () {
        wrap.classList.add('na-ad-in');
        document.body.classList.add('na-has-ad');
      });
    });
  }

  function init() {
    var style = el('style');
    style.id = 'na-sticky-ad-css';
    style.textContent = css;
    document.head.appendChild(style);

    // One consistent design everywhere: drop older hand-coded bars.
    document.querySelectorAll('.sticky-cta').forEach(function (n) { n.remove(); });

    if (isAnalyzer) {
      var page2 = document.getElementById('page2');
      if (!page2) return;
      var reportAd = {
        icon: '✦',
        badge: '50% off today',
        title: 'Unlock your complete report',
        sub: '3 name-correction options · 5-year forecast · career & love',
        price: [['$5', '$2.50'], ['₹499', '₹249']],
        button: 'Unlock my report →',
        buttonShort: 'Unlock →',
        href: '/report'
      };
      var check = function () { if (getComputedStyle(page2).display !== 'none') show(reportAd); };
      check();
      new MutationObserver(check).observe(page2, { attributes: true, attributeFilter: ['style', 'class'] });
      return;
    }

    var freeAd = {
      icon: '✦',
      title: 'Is your name working for you?',
      sub: 'Free Chaldean name analysis · 60 seconds · no sign-up',
      button: 'Check my name free →',
      buttonShort: 'Check free →',
      href: '/analyzer',
      mobileOnly: !!document.querySelector('.article-sidebar')
    };
    var onScroll = function () {
      if (window.scrollY > SCROLL_TRIGGER) {
        window.removeEventListener('scroll', onScroll);
        show(freeAd);
      }
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
