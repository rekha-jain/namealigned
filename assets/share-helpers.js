/**
 * Share helpers for NameAligned.
 *
 * Goal: emotional compulsion to send, not generic "share this".
 * WhatsApp is the primary channel for our Indian audience.
 *
 * Markup pattern:
 *   <div class="share-strip"
 *        data-emotion-headline="..."
 *        data-emotion-prompt="..."
 *        data-share-text="..."
 *        data-share-url="..."></div>
 *
 * Auto-mounts on DOMContentLoaded.
 *
 * GA4 events emitted: share_whatsapp, share_copy, share_native
 */

(function(){
  'use strict';

  function buildStrip(el) {
    const headline = el.getAttribute('data-emotion-headline') || 'Send this to them?';
    const prompt   = el.getAttribute('data-emotion-prompt')   || 'See if they recognise themselves.';
    const text     = el.getAttribute('data-share-text')       || '';
    const urlInput = el.getAttribute('data-share-url')        || (typeof window !== 'undefined' ? window.location.href : '');
    const source   = el.getAttribute('data-share-source')     || 'unknown';

    const fullMessage = text ? (text + ' ' + urlInput) : urlInput;
    const waHref = 'https://wa.me/?text=' + encodeURIComponent(fullMessage);

    el.innerHTML = (
      '<h3>' + escapeHTML(headline) + '</h3>' +
      '<p>' + escapeHTML(prompt) + '</p>' +
      '<div class="share-buttons">' +
        '<a class="wa" href="' + waHref + '" target="_blank" rel="noopener" data-share-method="whatsapp">' +
          '<span aria-hidden="true">WA</span> Send on WhatsApp' +
        '</a>' +
        '<button class="copy" type="button" data-share-method="copy">Copy link</button>' +
        (navigator.share ? '<button class="copy" type="button" data-share-method="native">More</button>' : '') +
      '</div>'
    );

    // Wire events.
    const waBtn = el.querySelector('[data-share-method="whatsapp"]');
    if (waBtn) {
      waBtn.addEventListener('click', () => {
        emitShare('whatsapp', source);
      });
    }

    const copyBtn = el.querySelector('[data-share-method="copy"]');
    if (copyBtn) {
      copyBtn.addEventListener('click', () => {
        const target = fullMessage;
        const fallback = () => {
          const ta = document.createElement('textarea');
          ta.value = target; ta.style.position = 'fixed'; ta.style.top = '-9999px';
          document.body.appendChild(ta); ta.select();
          try { document.execCommand('copy'); } catch (e) {}
          document.body.removeChild(ta);
        };
        if (navigator.clipboard) {
          navigator.clipboard.writeText(target).catch(fallback);
        } else {
          fallback();
        }
        const original = copyBtn.textContent;
        copyBtn.textContent = 'Copied';
        setTimeout(() => { copyBtn.textContent = original; }, 1400);
        emitShare('copy', source);
      });
    }

    const nativeBtn = el.querySelector('[data-share-method="native"]');
    if (nativeBtn) {
      nativeBtn.addEventListener('click', () => {
        if (navigator.share) {
          navigator.share({ title: headline, text: text || prompt, url: urlInput })
            .then(() => emitShare('native', source))
            .catch(() => {});
        }
      });
    }
  }

  function emitShare(method, source) {
    if (typeof gtag === 'function') {
      gtag('event', method === 'whatsapp' ? 'share_whatsapp' :
                    method === 'copy'     ? 'share_copy'     :
                                            'share_native', {
        source: source,
      });
    }
  }

  function escapeHTML(s){
    return String(s || '')
      .replace(/&/g,'&amp;').replace(/</g,'&lt;')
      .replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&#39;');
  }

  function autoMount() {
    document.querySelectorAll('.share-strip[data-share-text], .share-strip[data-emotion-headline]')
      .forEach(buildStrip);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', autoMount);
  } else {
    autoMount();
  }

  window.NA_Share = { build: buildStrip };
})();
