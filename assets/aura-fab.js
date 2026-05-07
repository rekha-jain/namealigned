/* ═══════════════════════════════════════════════════════════════
   AURA FAB — floating "Chat with Aura" pill, site-wide
   ─────────────────────────────────────────────────────────────
   Loaded from a single tag at the bottom of every production
   page. Auto-skips itself on /ask-aura (no point), respects a
   localStorage 'dismiss until next session' flag, and stays out
   of the way on print.
   ═══════════════════════════════════════════════════════════════ */
(function(){
  'use strict';

  // Skip on the chat page itself, and on share-card/staging utility pages
  const path = location.pathname.replace(/\/$/, '').toLowerCase();
  const SKIP_PATHS = ['/ask-aura', '/share-card', '/staging-report', '/sitemap-pages'];
  if (SKIP_PATHS.some(p => path === p)) return;

  // Per-session dismiss flag — pill returns next visit, never gone forever
  if (sessionStorage.getItem('aura_fab_dismissed') === '1') return;

  // Build the pill
  const root = document.createElement('div');
  root.id = 'aura-fab';
  root.innerHTML = `
    <a href="/ask-aura" class="aura-fab-pill" aria-label="Open Aura">
      <span class="aura-fab-orb" aria-hidden="true"></span>
      <span class="aura-fab-text">Ask Aura</span>
    </a>
    <button class="aura-fab-x" aria-label="Hide Aura for this session">×</button>
  `;
  const style = document.createElement('style');
  style.textContent = `
    #aura-fab {
      position: fixed;
      bottom: 12px;
      right: 12px;
      z-index: 9998;
      display: flex;
      align-items: center;
      gap: 6px;
      animation: auraFabIn .35s ease .8s both;
    }
    @keyframes auraFabIn {
      from { opacity: 0; transform: translateY(14px); }
      to   { opacity: 1; transform: translateY(0); }
    }
    .aura-fab-pill {
      display: inline-flex;
      align-items: center;
      gap: 7px;
      padding: 5px 12px 5px 5px;
      border-radius: 24px;
      background: linear-gradient(135deg, #1a0e52 0%, #3a1d80 60%, #2a1538 100%);
      color: #f0ece0;
      text-decoration: none;
      font-family: 'Inter', system-ui, -apple-system, sans-serif;
      box-shadow: 0 6px 18px rgba(26, 14, 82, .35), 0 2px 5px rgba(0, 0, 0, .22);
      border: 1px solid rgba(245, 208, 96, .35);
      transition: transform .15s ease, box-shadow .15s ease;
    }
    .aura-fab-pill:hover {
      transform: translateY(-2px);
      box-shadow: 0 10px 24px rgba(26, 14, 82, .45), 0 4px 10px rgba(0, 0, 0, .3);
      color: #fff;
    }
    .aura-fab-orb {
      flex-shrink: 0;
      width: 24px;
      height: 24px;
      border-radius: 50%;
      background-image: url('/assets/aura-portrait.jpg?v=3');
      background-color: #c9a227;
      background-position: center;
      background-size: cover;
      background-repeat: no-repeat;
      border: 1px solid rgba(245, 208, 96, .65);
      box-shadow: 0 0 10px rgba(245, 208, 96, .50);
      animation: auraOrbPulse 3.6s ease-in-out infinite;
    }
    @keyframes auraOrbPulse {
      0%, 100% { box-shadow: 0 0 10px rgba(245, 208, 96, .45); }
      50%      { box-shadow: 0 0 16px rgba(245, 208, 96, .80); }
    }
    .aura-fab-text {
      font-size: 12.5px;
      font-weight: 600;
      letter-spacing: .02em;
      color: #f0ece0;
      line-height: 1;
    }
    .aura-fab-x {
      width: 24px;
      height: 24px;
      border-radius: 50%;
      border: 1px solid rgba(255, 255, 255, .15);
      background: rgba(10, 8, 32, .85);
      color: rgba(255, 255, 255, .55);
      font-size: 14px;
      line-height: 1;
      cursor: pointer;
      padding: 0;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      font-family: inherit;
    }
    .aura-fab-x:hover {
      color: #fff;
      background: rgba(10, 8, 32, .95);
      border-color: rgba(255, 255, 255, .35);
    }
    @media (max-width: 560px) {
      #aura-fab { bottom: 10px; right: 10px; }
      .aura-fab-pill { padding: 4px 10px 4px 4px; }
      .aura-fab-text { font-size: 12px; }
    }
    /* Don't compete with mobile sticky CTA — but only on mobile,
       where the sticky CTA bar actually shows. On desktop the sticky
       CTA is hidden so the pill should sit in the corner. */
    @media (max-width: 700px) {
      .sticky-cta ~ #aura-fab,
      body:has(.sticky-cta) #aura-fab { bottom: 76px; }
    }
    @media print { #aura-fab { display: none !important; } }
  `;

  document.head.appendChild(style);
  document.body.appendChild(root);

  // Dismiss handler
  root.querySelector('.aura-fab-x').addEventListener('click', () => {
    sessionStorage.setItem('aura_fab_dismissed', '1');
    root.style.transition = 'opacity .25s ease, transform .25s ease';
    root.style.opacity = '0';
    root.style.transform = 'translateY(14px)';
    setTimeout(() => root.remove(), 280);
  });

  // Track open
  const pill = root.querySelector('.aura-fab-pill');
  pill.addEventListener('click', () => {
    if (typeof gtag === 'function') gtag('event', 'aura_fab_clicked', { source_path: path });
  });
})();
