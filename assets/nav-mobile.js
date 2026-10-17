// Phone menu toggle (shared). Binds #navHamburger to #navMobile once per
// page; builds #navMobile from .nav-links if a page has the hamburger only.
// numerology.js initNav() defers to this so the click is never bound twice.
(function(){
  function init(){
    var ham=document.getElementById('navHamburger');
    if(!ham||ham.dataset.navBound) return;
    var mob=document.getElementById('navMobile');
    var nav=ham.closest('nav')||document.body;
    if(!mob){
      var links=nav.querySelectorAll('.nav-links a');
      if(!links.length) return;
      mob=document.createElement('div');
      mob.className='nav-mobile';mob.id='navMobile';
      links.forEach(function(a){
        var m=document.createElement('a');
        m.href=a.getAttribute('href');m.textContent=a.textContent.trim();
        mob.appendChild(m);
      });
      nav.appendChild(mob);
    }
    ham.dataset.navBound='1';
    ham.setAttribute('role','button');
    ham.setAttribute('tabindex','0');
    ham.setAttribute('aria-label','Menu');
    ham.setAttribute('aria-controls','navMobile');
    ham.setAttribute('aria-expanded','false');
    function set(open){
      mob.classList.toggle('open',open);
      ham.setAttribute('aria-expanded',open?'true':'false');
    }
    ham.addEventListener('click',function(e){e.stopPropagation();set(!mob.classList.contains('open'));});
    ham.addEventListener('keydown',function(e){
      if(e.key==='Enter'||e.key===' '){e.preventDefault();set(!mob.classList.contains('open'));}
    });
    mob.addEventListener('click',function(e){if(e.target.closest('a')) set(false);});
    document.addEventListener('click',function(e){if(!nav.contains(e.target)) set(false);});
    document.addEventListener('keydown',function(e){if(e.key==='Escape') set(false);});
  }
  window.naInitNav=init;
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',init);
  else init();
})();
