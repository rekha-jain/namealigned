// Swap an Anahata Acoustics thumbnail for the YouTube player on click.
(function () {
  document.addEventListener('click', function (e) {
    var btn = e.target.closest && e.target.closest('.na-video button');
    if (!btn) return;
    var box = btn.parentNode, id = box.getAttribute('data-id');
    if (!/^[\w-]{11}$/.test(id)) return;
    var f = document.createElement('iframe');
    f.src = 'https://www.youtube-nocookie.com/embed/' + id + '?autoplay=1&rel=0&playsinline=1';
    f.title = btn.getAttribute('aria-label') || 'Anahata Acoustics track';
    f.allow = 'autoplay; encrypted-media; picture-in-picture; fullscreen';
    f.allowFullscreen = true;
    box.innerHTML = '';
    box.appendChild(f);
    if (window.gtag) window.gtag('event', 'music_played', { video_id: id, page: location.pathname });
  });
})();
