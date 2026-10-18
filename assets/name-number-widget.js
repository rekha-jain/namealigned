(function () {
  'use strict';

  var LETTER_VALUES = {
    A: 1, B: 2, C: 3, D: 4, E: 5, F: 8, G: 3, H: 5, I: 1,
    J: 1, K: 2, L: 3, M: 4, N: 5, O: 7, P: 8, Q: 1, R: 2,
    S: 3, T: 4, U: 6, V: 6, W: 6, X: 5, Y: 1, Z: 7
  };

  var PLANETS = {
    1: 'Sun', 2: 'Moon', 3: 'Jupiter', 4: 'Rahu', 5: 'Mercury',
    6: 'Venus', 7: 'Ketu', 8: 'Saturn', 9: 'Mars'
  };

  var MEANINGS = {
    1: 'direction, visibility, and self-leadership',
    2: 'sensitivity, intuition, and emotional attunement',
    3: 'expression, learning, and generous confidence',
    4: 'structure, disruption, and unconventional problem solving',
    5: 'movement, language, and adaptive intelligence',
    6: 'beauty, care, and relationship harmony',
    7: 'analysis, privacy, and spiritual inquiry',
    8: 'discipline, responsibility, and long-range ambition',
    9: 'courage, intensity, and protective action'
  };

  function reduceNumber(total) {
    var value = Math.abs(total);
    while (value > 9) {
      value = String(value).split('').reduce(function (sum, digit) {
        return sum + Number(digit);
      }, 0);
    }
    return value || 0;
  }

  function calculateName(name) {
    var letters = String(name || '').toUpperCase().replace(/[^A-Z]/g, '').split('');
    var parts = letters.map(function (letter) {
      return { letter: letter, value: LETTER_VALUES[letter] || 0 };
    });
    var compound = parts.reduce(function (sum, part) {
      return sum + part.value;
    }, 0);
    return {
      parts: parts,
      compound: compound,
      reduced: reduceNumber(compound)
    };
  }

  function injectStyles() {
    if (document.getElementById('namealigned-widget-style')) return;
    var style = document.createElement('style');
    style.id = 'namealigned-widget-style';
    style.textContent = [
      '.na-widget{box-sizing:border-box;max-width:440px;border:1px solid rgba(109,78,209,.22);border-radius:14px;background:#fff;color:#19142d;box-shadow:0 12px 32px rgba(35,25,78,.08);font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;overflow:hidden}',
      '.na-widget *{box-sizing:border-box}',
      '.na-widget__head{padding:18px 18px 12px;background:linear-gradient(135deg,#20154c,#5c3fc7);color:#fff}',
      '.na-widget__kicker{font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:#f5d060;font-weight:800;margin-bottom:6px}',
      '.na-widget .na-widget__title{font-family:Georgia,"Times New Roman",serif;font-size:22px;line-height:1.18;margin:0;padding:0;color:#fff!important;font-weight:700;border:0;background:none;text-transform:none;letter-spacing:normal}',
      '.na-widget .na-widget__kicker{color:#f5d060!important}',
      '.na-widget p,.na-widget span,.na-widget label{text-transform:none;letter-spacing:normal}',
      '.na-widget__body{padding:16px 18px 18px}',
      '.na-widget__label{display:block;font-size:13px;color:#5f5677;font-weight:700;margin-bottom:7px}',
      '.na-widget__row{display:flex;gap:8px}',
      '.na-widget__input{flex:1;min-width:0;border:1px solid rgba(109,78,209,.25);border-radius:9px;padding:11px 12px;font-size:15px;color:#19142d;background:#fff}',
      '.na-widget__button{border:0;border-radius:9px;background:#f0b429;color:#15110b;font-size:14px;font-weight:800;padding:0 14px;cursor:pointer;white-space:nowrap}',
      '.na-widget__button:hover{background:#d99e19}',
      '.na-widget__result{display:none;margin-top:14px;border:1px solid rgba(6,182,212,.2);border-radius:11px;background:#faf8ff;padding:13px 14px}',
      '.na-widget__result.is-visible{display:block}',
      '.na-widget__numbers{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px;margin-bottom:10px}',
      '.na-widget__metric{background:#fff;border:1px solid rgba(109,78,209,.12);border-radius:9px;padding:10px}',
      '.na-widget__metric span{display:block;font-size:11px;text-transform:uppercase;letter-spacing:.08em;color:#796f92;font-weight:800;margin-bottom:4px}',
      '.na-widget__metric strong{display:block;font-family:Georgia,"Times New Roman",serif;font-size:26px;line-height:1;color:#6d4ed1}',
      '.na-widget__text{font-size:13.5px;line-height:1.55;color:#3b344f;margin:0}',
      '.na-widget__breakdown{font-size:12px;line-height:1.6;color:#6b617e;margin-top:9px;word-break:break-word}',
      '.na-widget__empty{font-size:12.5px;color:#a33d3d;margin-top:8px;display:none}',
      '.na-widget__empty.is-visible{display:block}',
      '.na-widget__credit{border-top:1px solid rgba(109,78,209,.13);padding:10px 18px;background:#fbfaf7;font-size:12px;color:#776f85}',
      '.na-widget__credit a{color:#6d4ed1;font-weight:800;text-decoration:none}',
      '.na-widget__link{display:inline-block;margin-top:9px;font-size:13px;font-weight:800;color:#6d4ed1;text-decoration:none}',
      '@media(max-width:420px){.na-widget__row{flex-direction:column}.na-widget__button{padding:11px 14px}.na-widget__numbers{grid-template-columns:1fr}}'
    ].join('');
    document.head.appendChild(style);
  }

  function renderWidget(host, index) {
    if (host.getAttribute('data-namealigned-ready') === 'true') return;
    host.setAttribute('data-namealigned-ready', 'true');

    var widget = document.createElement('section');
    widget.className = 'na-widget';
    widget.setAttribute('aria-label', 'NameAligned Chaldean name number widget');
    widget.innerHTML = [
      '<div class="na-widget__head">',
      '<div class="na-widget__kicker">Free Chaldean calculator</div>',
      '<h2 class="na-widget__title">Find your name number</h2>',
      '</div>',
      '<div class="na-widget__body">',
      '<label class="na-widget__label" for="na-widget-name-' + index + '">Name to calculate</label>',
      '<div class="na-widget__row">',
      '<input class="na-widget__input" id="na-widget-name-' + index + '" type="text" autocomplete="name" placeholder="Type a name">',
      '<button class="na-widget__button" type="button">Calculate</button>',
      '</div>',
      '<div class="na-widget__empty" role="status">Please enter at least one letter.</div>',
      '<div class="na-widget__result" aria-live="polite">',
      '<div class="na-widget__numbers">',
      '<div class="na-widget__metric"><span>Compound total</span><strong data-compound>0</strong></div>',
      '<div class="na-widget__metric"><span>Name number</span><strong data-reduced>0</strong></div>',
      '</div>',
      '<p class="na-widget__text" data-summary></p>',
      '<div class="na-widget__breakdown" data-breakdown></div>',
      '</div>',
      '</div>',
      '<div class="na-widget__credit">Powered by <a href="https://www.namealigned.com/name-numerology-calculator?utm_source=embed-widget&utm_medium=referral&utm_campaign=name-number-widget" target="_blank" rel="noopener">NameAligned.com</a></div>'
    ].join('');

    var input = widget.querySelector('.na-widget__input');
    var button = widget.querySelector('.na-widget__button');
    var result = widget.querySelector('.na-widget__result');
    var empty = widget.querySelector('.na-widget__empty');
    var compoundEl = widget.querySelector('[data-compound]');
    var reducedEl = widget.querySelector('[data-reduced]');
    var summaryEl = widget.querySelector('[data-summary]');
    var breakdownEl = widget.querySelector('[data-breakdown]');

    function update() {
      var calculation = calculateName(input.value);
      if (!calculation.parts.length) {
        result.classList.remove('is-visible');
        empty.classList.add('is-visible');
        return;
      }
      empty.classList.remove('is-visible');
      result.classList.add('is-visible');
      compoundEl.textContent = String(calculation.compound);
      reducedEl.textContent = String(calculation.reduced);
      summaryEl.textContent = 'Name number ' + calculation.reduced + ' is linked with ' + PLANETS[calculation.reduced] + ', carrying themes of ' + MEANINGS[calculation.reduced] + '.';
      breakdownEl.textContent = calculation.parts.map(function (part) {
        return part.letter + '=' + part.value;
      }).join(' + ');
    }

    button.addEventListener('click', update);
    input.addEventListener('keydown', function (event) {
      if (event.key === 'Enter') update();
    });
    input.addEventListener('input', function () {
      if (result.classList.contains('is-visible')) update();
    });

    host.appendChild(widget);
  }

  // ── Date-based widgets: birthday number and personal year ──────
  var YEAR_THEMES = {
    1: 'new beginnings and launching', 2: 'patience and partnership', 3: 'creativity and expansion',
    4: 'hard work and foundations', 5: 'change, travel and freedom', 6: 'home, love and responsibility',
    7: 'reflection and inner wisdom', 8: 'ambition, money and recognition', 9: 'completion and release'
  };
  var UTM = 'utm_source=embed-widget&utm_medium=referral&utm_campaign=';

  function digitSum(str) {
    return String(str).replace(/\D/g, '').split('').reduce(function (a, d) { return a + Number(d); }, 0);
  }

  function ordinal(n) {
    var s = ['th', 'st', 'nd', 'rd'], v = n % 100;
    return n + (s[(v - 20) % 10] || s[v] || s[0]);
  }

  function renderDateWidget(host, index, type) {
    if (host.getAttribute('data-namealigned-ready') === 'true') return;
    host.setAttribute('data-namealigned-ready', 'true');
    var isYear = type === 'personal-year';
    var creditPath = isYear ? 'personal-year-calculator' : 'birthday-numbers';
    var widget = document.createElement('section');
    widget.className = 'na-widget';
    widget.setAttribute('aria-label', isYear ? 'NameAligned personal year calculator' : 'NameAligned birthday number calculator');
    widget.innerHTML = [
      '<div class="na-widget__head">',
      '<div class="na-widget__kicker">Free Chaldean calculator</div>',
      '<h2 class="na-widget__title">' + (isYear ? 'Find your personal year' : 'Find your birthday number') + '</h2>',
      '</div>',
      '<div class="na-widget__body">',
      '<label class="na-widget__label" for="na-widget-date-' + type + '-' + index + '">Date of birth</label>',
      '<div class="na-widget__row">',
      '<input class="na-widget__input" id="na-widget-date-' + type + '-' + index + '" type="date">',
      '<button class="na-widget__button" type="button">Calculate</button>',
      '</div>',
      '<div class="na-widget__empty" role="status">Please choose a date of birth.</div>',
      '<div class="na-widget__result" aria-live="polite">',
      '<div class="na-widget__numbers">',
      '<div class="na-widget__metric"><span>' + (isYear ? 'Personal year now' : 'Born on the') + '</span><strong data-a>0</strong></div>',
      '<div class="na-widget__metric"><span>' + (isYear ? 'From next birthday' : 'Birth number') + '</span><strong data-b>0</strong></div>',
      '</div>',
      '<p class="na-widget__text" data-summary></p>',
      '<a class="na-widget__link" data-more target="_blank" rel="noopener"></a>',
      '</div>',
      '</div>',
      '<div class="na-widget__credit">Powered by <a href="https://www.namealigned.com/' + creditPath + '?' + UTM + type + '-widget" target="_blank" rel="noopener">NameAligned.com</a></div>'
    ].join('');

    var input = widget.querySelector('.na-widget__input');
    var result = widget.querySelector('.na-widget__result');
    var empty = widget.querySelector('.na-widget__empty');
    var aEl = widget.querySelector('[data-a]'), bEl = widget.querySelector('[data-b]');
    var summaryEl = widget.querySelector('[data-summary]'), more = widget.querySelector('[data-more]');

    function update() {
      var v = input.value;
      if (!/^\d{4}-\d{2}-\d{2}$/.test(v)) {
        result.classList.remove('is-visible'); empty.classList.add('is-visible'); return;
      }
      empty.classList.remove('is-visible'); result.classList.add('is-visible');
      var parts = v.split('-'), month = Number(parts[1]), day = Number(parts[2]);
      if (isYear) {
        // Personal year runs birthday to birthday.
        var now = new Date(), y = now.getFullYear();
        var cy = now < new Date(y, month - 1, day) ? y - 1 : y;
        var cur = reduceNumber(digitSum(parts[1] + parts[2] + cy));
        var next = reduceNumber(digitSum(parts[1] + parts[2] + (cy + 1)));
        aEl.textContent = String(cur); bEl.textContent = String(next);
        summaryEl.textContent = 'You are in Personal Year ' + cur + ' (' + PLANETS[cur] + '): a year of ' + YEAR_THEMES[cur] + '. It changes to Personal Year ' + next + ' on your next birthday.';
        more.href = 'https://www.namealigned.com/personal-year-number-' + cur + '-meaning?' + UTM + 'personal-year-widget';
        more.textContent = 'What Personal Year ' + cur + ' means →';
      } else {
        var birth = reduceNumber(day);
        aEl.textContent = ordinal(day); bEl.textContent = String(birth);
        summaryEl.textContent = 'Born on the ' + ordinal(day) + ', your Birth Number is ' + birth + ', ruled by ' + PLANETS[birth] + ', with themes of ' + MEANINGS[birth] + '.';
        more.href = 'https://www.namealigned.com/birthday-number-' + day + '-meaning?' + UTM + 'birthday-number-widget';
        more.textContent = 'Read the meaning of the ' + ordinal(day) + ' →';
      }
    }
    widget.querySelector('.na-widget__button').addEventListener('click', update);
    input.addEventListener('change', function () { if (result.classList.contains('is-visible')) update(); });
    host.appendChild(widget);
  }

  function init() {
    injectStyles();
    var hosts = document.querySelectorAll('[data-namealigned-widget="name-number"]');
    Array.prototype.forEach.call(hosts, renderWidget);
    ['birthday-number', 'personal-year'].forEach(function (type) {
      var dh = document.querySelectorAll('[data-namealigned-widget="' + type + '"]');
      Array.prototype.forEach.call(dh, function (h, i) { renderDateWidget(h, i, type); });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
