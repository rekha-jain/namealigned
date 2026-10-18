/* ═══════════════════════════════════════════════════════════════
   EMAIL CAPTURE for the free tools
   ───────────────────────────────────────────────────────────────
   Adds an "Email me this result" box under a tool's result once it
   shows, and saves the visitor to Supabase `leads` through the same
   /api/capture-lead endpoint the free analysis uses.

   One tag before </body> on a tool page:
     <script src="/assets/email-capture.js?v=..." defer></script>
   Needs assets/numerology.js on the page for the numbers.
   ═══════════════════════════════════════════════════════════════ */
(function () {
  'use strict';

  var path = window.location.pathname.replace(/\.html$/, '').replace(/\/$/, '');

  // anchor: result element; name/dob/mobile: input selectors (null when the
  // tool does not ask, in which case the box asks for the name itself).
  var TOOLS = {
    '/lo-shu-grid-calculator':        { source: 'lo-shu-grid',   anchor: '#loshuOut',      dob: '#loshuDob', name: null,       mobile: null },
    '/mobile-number-numerology':      { source: 'mobile-number', anchor: '#mobOut',        dob: '#mobDob',   name: null,       mobile: '#mobPhone' },
    '/love-compatibility-numerology': { source: 'compatibility', anchor: '#partnerResult', dob: '#youDob',    name: '#youName', mobile: null },
    '/business-name-numerology':      { source: 'business-name', anchor: '#bizResult',     dob: '#bizDob',    name: null,       mobile: null }
  };
  var cfg = TOOLS[path];
  if (!cfg) return;

  var css = [
    '.na-ec{margin-top:1.25rem;padding:1.1rem 1.2rem;border-radius:14px;text-align:left;font-family:"DM Sans",system-ui,sans-serif;',
      'background:linear-gradient(135deg,rgba(124,58,237,.07),rgba(245,196,81,.08));border:1px solid rgba(124,58,237,.22)}',
    '.na-ec h4{margin:0 0 .25rem;font-family:"Playfair Display",Georgia,serif;font-size:17px;color:var(--text,#1a1340)}',
    '.na-ec p{margin:0 0 .75rem;font-size:13px;line-height:1.5;color:var(--text2,#4a4560)}',
    '.na-ec-row{display:flex;gap:.5rem;flex-wrap:wrap}',
    '.na-ec input{flex:1 1 180px;min-width:0;padding:.65rem .8rem;border-radius:10px;border:1px solid rgba(124,58,237,.3);font-size:14px;background:#fff;color:#1a1340}',
    '.na-ec button{flex:0 0 auto;padding:.65rem 1.1rem;border:0;border-radius:999px;font-weight:700;font-size:14px;cursor:pointer;color:#1a0533;',
      'background:linear-gradient(135deg,#f5d060,#f0b429);box-shadow:0 4px 14px rgba(240,180,41,.35)}',
    '.na-ec button[disabled]{opacity:.6;cursor:default}',
    '.na-ec-msg{margin-top:.55rem;font-size:12.5px}',
    '.na-ec-done{font-size:14px;color:#15803d;font-weight:600}'
  ].join('');

  function val(sel) {
    var el = sel && document.querySelector(sel);
    return el ? String(el.value || '').trim() : '';
  }

  function savePrefill(data) {
    try {
      var cur = JSON.parse(sessionStorage.getItem('na_prefill') || '{}');
      sessionStorage.setItem('na_prefill', JSON.stringify(Object.assign(cur, data)));
    } catch (e) {}
  }

  function build() {
    var box = document.createElement('div');
    box.className = 'na-ec';
    var askName = !cfg.name || !val(cfg.name);
    box.innerHTML =
      '<h4>✉️ Email me this result</h4>' +
      '<p>Get your Chaldean numbers and this reading in your inbox, so you can come back to it. No spam.</p>' +
      '<div class="na-ec-row">' +
        (askName ? '<input type="text" class="na-ec-name" placeholder="Your name (as you use it daily)" autocomplete="name">' : '') +
        '<input type="email" class="na-ec-email" placeholder="your@email.com" autocomplete="email">' +
        '<button type="button">Send it to me →</button>' +
      '</div>' +
      '<div class="na-ec-msg" aria-live="polite"></div>';

    var btn = box.querySelector('button');
    var msg = box.querySelector('.na-ec-msg');

    btn.addEventListener('click', function () {
      var name = askName ? String(box.querySelector('.na-ec-name').value || '').trim() : val(cfg.name);
      var email = String(box.querySelector('.na-ec-email').value || '').trim();
      var dob = val(cfg.dob);
      msg.style.color = '#b91c1c';
      if (!name) { msg.textContent = 'Please enter your name.'; return; }
      if (!dob) { msg.textContent = 'Please add your date of birth in the form above first.'; return; }
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) { msg.textContent = 'Please enter a valid email address.'; return; }

      var nums = {};
      try {
        if (dob && typeof getBirthNum === 'function') {
          nums.birthNum = getBirthNum(dob);
          nums.destNum = getDestinyNum(dob);
        }
        if (typeof getNameNum === 'function') {
          var n = getNameNum(name);
          nums.nameNum = n.reduced;
          if (dob && typeof compatPct === 'function') nums.pct = compatPct(n.reduced, n.raw, nums.birthNum, nums.destNum);
        }
      } catch (e) {}

      btn.disabled = true; btn.textContent = 'Sending…'; msg.textContent = '';
      fetch('/api/capture-lead', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: name, dob: dob || null, email: email,
          mobile: cfg.mobile ? val(cfg.mobile) : undefined,
          birthNum: nums.birthNum, destNum: nums.destNum, nameNum: nums.nameNum, pct: nums.pct,
          source: cfg.source
        })
      })
        .then(function (r) { return r.json().catch(function () { return {}; }).then(function (d) { return { ok: r.ok, d: d }; }); })
        .then(function (res) {
          if (!res.ok || !res.d.success) throw new Error(res.d.error || 'Could not send right now.');
          savePrefill({ name: name, dob: dob, email: email });
          if (window.naIdentify) window.naIdentify(email, { name: name });
          if (window.naTrack) window.naTrack('Email Captured', { location: cfg.source });
          if (window.NA && NA.track) NA.track('email_captured', { location: cfg.source });
          box.innerHTML = '<div class="na-ec-done">✓ Sent. Check your inbox (and spam, just in case).</div>';
        })
        .catch(function (e) {
          btn.disabled = false; btn.textContent = 'Send it to me →';
          msg.textContent = e.message || 'Could not send right now. Please try again.';
        });
    });
    return box;
  }

  function init() {
    var anchor = document.querySelector(cfg.anchor);
    if (!anchor) return;
    var style = document.createElement('style');
    style.textContent = css;
    document.head.appendChild(style);

    var box = null;
    var check = function () {
      var shown = anchor.offsetHeight > 0 && anchor.textContent.trim().length > 0;
      if (shown && !box) {
        box = build();
        anchor.insertAdjacentElement('afterend', box);
      }
    };
    new MutationObserver(check).observe(anchor, { childList: true, subtree: true, attributes: true, attributeFilter: ['class', 'style'] });
    check();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
