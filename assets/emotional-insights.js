/**
 * Emotional Insights Library
 *
 * Screenshot-worthy single-sentence emotional observations, keyed by
 * Chaldean birth number (1..9). Each number has 8 distinct insights;
 * the renderer picks 2-3 randomly per page load so re-visits feel fresh.
 *
 * Voice rules for every insight:
 *   - Second person ("you" / "your"), present tense
 *   - 1 to 2 short sentences max
 *   - Psychologically believable, never deterministic
 *   - No numerology jargon (no "moolank", no "ruling planet")
 *   - Emotionally resonant, the kind of line you would screenshot
 *     and send to a friend with "this is me"
 *
 * Usage:
 *   <div class="emotional-insights" data-number="6" data-count="3"></div>
 *   <script src="/assets/emotional-insights.js" defer></script>
 *
 * The script auto-mounts on DOMContentLoaded.
 */

(function(){
  'use strict';

  // Each number gets 8 emotionally distinct, screenshot-worthy lines.
  // Drawn from the felt experience of the planet's archetype, in
  // everyday emotional language.
  const INSIGHTS = {
    1: [
      'You appear self-sufficient long before you actually feel it.',
      'Your hardest conversations are the ones where you have to ask for help.',
      'You carry leadership even in rooms that did not ask you to lead.',
      'You move faster than the people who love you, and you feel that gap.',
      'Compliments land as confirmation, not surprise. You already knew, but quietly.',
      'You can tell when someone wants you to be smaller. You usually become larger instead.',
      'Loneliness for you is not the absence of people, it is the absence of equals.',
      'You make decisions in silence, then announce them. The decision was made long before the announcement.',
    ],
    2: [
      'You feel the temperature of a room before anyone has spoken.',
      'You read tone before you read words. The unsaid parts reach you first.',
      'You forgive faster than your body does. Your mind moves on, your shoulders remember.',
      'You can hold space for someone for hours without them realising they were held.',
      'You take other people\'s moods home with you, even when you tried not to.',
      'The smallest tone shift in a message you love can sit with you all evening.',
      'You apologise for being emotional, then quietly notice no one else apologises for being cold.',
      'Your peace is harder won than other people realise. You protect it because you had to build it.',
    ],
    3: [
      'You explain things to make them real, including to yourself.',
      'You are warmest in public and quietest at home. Both versions are you.',
      'You are good company. You sometimes need to remember you are also good alone.',
      'You teach by accident. People learn from you in conversations you forgot.',
      'Your honesty arrives wrapped in humour, and people miss the honest part.',
      'You light up other people\'s rooms and forget to light your own.',
      'Your saying yes is louder than your no. It costs you more than it should.',
      'You can be the funniest person in the room and the loneliest, on the same evening.',
    ],
    4: [
      'You notice things other people will only see in three months.',
      'Being called paranoid by people you were right about is exhausting in a specific way.',
      'You hold back the obvious thing in meetings because no one wants to hear it.',
      'Your unusual angle is the value, and also why you sometimes feel like the outsider.',
      'You build the thing first and explain it after. Words come late for you.',
      'You change your mind in public, which other people find threatening. It is just how you think.',
      'The rules you broke at twenty are the foundations you respect at thirty-five.',
      'You are not difficult. You are early, and being early can look like difficulty.',
    ],
    5: [
      'You have seventeen tabs open in your mind right now. Pick two.',
      'You enjoy your own conversations, including the ones in your head.',
      'You start things quickly. You finish them when something matches the original spark.',
      'You can talk to almost anyone. You are picky about who you stay quiet with.',
      'You think while moving. Stillness for you is harder than action.',
      'You absorb information at a rate that exhausts you and you keep doing it anyway.',
      'You leave conversations early sometimes because your mind already left.',
      'You can hold five different worlds at once. The cost is that none of them fully holds you.',
    ],
    6: [
      'You confuse care with self-care more often than you realise.',
      'You smooth other people\'s rough edges and quietly carry your own.',
      'You can tell when a room is uncomfortable. You usually rearrange it before anyone notices.',
      'You make beautiful spaces because beauty steadies you, not because it is decoration.',
      'You say yes to comfort over honesty in small ways, until the honesty has nowhere to go.',
      'You apologise for needs you have not even named yet.',
      'You love through routine. The Tuesday meal, the morning text, the small habits.',
      'You can love someone, see their pattern clearly, and still keep showing up.',
    ],
    7: [
      'You can sit in silence with the right person and feel more met than after an hour of words.',
      'You stand slightly outside groups by design, not because you were not invited.',
      'Your inner life has more rooms than most people\'s outer life does.',
      'You ask questions other people consider rude. You consider them honest.',
      'You meet someone once and either feel everything or feel nothing. Rarely a middle.',
      'Your most useful work happens when no one is looking.',
      'You will dissolve a relationship before you will dilute it.',
      'The lonely parts of your life are not failures. They are how you metabolise the world.',
    ],
    8: [
      'You measure things in years where other people measure in weeks.',
      'You carry responsibilities other people would have set down by now.',
      'You appear emotionally steady while internally carrying real pressure.',
      'You wait. You wait longer than other people would wait. Then you move, and it sticks.',
      'You can hold a hard truth without flinching, but the soft ones move you more than people realise.',
      'You take a long time to build trust, and a longer time to take it back once given.',
      'You sometimes mistake endurance for love. Other times you are simply right.',
      'You have a private grief that most people would not guess exists. You manage it well.',
    ],
    9: [
      'You fight for people who are not yet in the room.',
      'Your anger is rarely about the present moment. The present is just where it landed.',
      'You will lose sleep over an injustice that did not happen to you.',
      'You love at temperature. Lukewarm is not a setting your heart has.',
      'You replay arguments in your head, winning the version you did not get to say out loud.',
      'You burn out because you cannot stand watching wrong things continue.',
      'You are not aggressive. You are alive in a culture that is uncomfortable with aliveness.',
      'You will protect people who never asked to be protected, and resent them for not noticing.',
    ],
  };

  // Insights keyed by compatibility pair (a < b). Two short lines per pair,
  // psychologically believable, screenshot-worthy.
  // For pairs not listed here, we fall back to a generic dual-archetype insight.
  const PAIR_INSIGHTS = {
    '1-2': [
      'One of you decides quickly and announces. The other already knew but waited to be asked.',
      'When this works, it works as a fortress and a hearth at the same time.',
    ],
    '1-9': [
      'You both bring heat. The relationship needs at least one quiet room to cool down in.',
      'You will either build something visible together, or argue about whose name goes first.',
    ],
    '2-7': [
      'You can sit in silence together and feel met. Most pairings cannot do that.',
      'Your hardest moments come when you both retreat at once. Build a small daily way to reach back.',
    ],
    '2-9': [
      'One of you needs to be reassured. The other speaks in heat. Translation matters here.',
      'When you do not speak the same emotional language, you have to actually translate, not assume.',
    ],
    '3-6': [
      'You make each other look better in every room you both enter.',
      'The hard truths still need to be said, even when the surface is already warm.',
    ],
    '3-9': [
      'When you both want the floor at once, take turns. The relationship gets quieter that way, not less alive.',
      'You are at your best with a shared mission. Without one, you can mistake each other for the project.',
    ],
    '4-8': [
      'This pairing amplifies both of you. With awareness it goes deep. Without it goes heavy.',
      'You will earn this relationship. It will not happen by accident.',
    ],
    '5-7': [
      'One of you wants to talk it through now. The other needs the night to find the words.',
      'You see the world in different speeds. The trick is not to mistake speed for depth or depth for distance.',
    ],
    '6-9': [
      'When you fight, one of you wants to restore harmony and the other wants to finish the conversation. Both are right.',
      'This love stays alive when it stays sensorial. Stop tending and it fades faster than expected.',
    ],
    '7-8': [
      'Both of you take the relationship seriously from day one. Neither plays games. That is rarer than people realise.',
      'Build small joys in deliberately. This pairing forgets to play.',
    ],
    '8-9': [
      'You move at different speeds and both of you are right about your speed.',
      'Give each other separate rooms to lead in. Then bring the wins back to the shared table.',
    ],
  };

  // Render helper. Picks `count` distinct insights for the given number,
  // wraps them in screenshot-worthy cards.
  function renderInsightsFor(number, count, container) {
    if (!container) return;
    const list = INSIGHTS[number] || INSIGHTS[6];
    const n = Math.min(count || 3, list.length);
    const picked = shuffle(list.slice()).slice(0, n);
    container.innerHTML = picked.map((line, i) => insightCardHTML(line, number, i)).join('');
    // Attach copy / share handlers to each card if utilities exist.
    container.querySelectorAll('[data-insight-copy]').forEach((btn) => {
      btn.addEventListener('click', (e) => {
        const text = btn.getAttribute('data-insight-text') || '';
        if (navigator.clipboard && text) {
          navigator.clipboard.writeText(text + ' — namealigned.com').catch(() => {});
        }
        btn.textContent = 'Copied';
        setTimeout(() => { btn.textContent = 'Copy'; }, 1400);
        if (typeof gtag === 'function') {
          gtag('event', 'insight_copied', { number: number, insight_index: i });
        }
      });
    });
    container.querySelectorAll('[data-insight-whatsapp]').forEach((btn) => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        const text = btn.getAttribute('data-insight-text') || '';
        const msg = encodeURIComponent('Read this and tell me if you see yourself: "' + text + '" — namealigned.com');
        window.open('https://wa.me/?text=' + msg, '_blank');
        if (typeof gtag === 'function') {
          gtag('event', 'share_whatsapp', { source: 'insight_card', number: number });
        }
      });
    });
  }

  function renderPairInsightsFor(a, b, container) {
    if (!container) return;
    const [lo, hi] = a < b ? [a, b] : [b, a];
    const key = lo + '-' + hi;
    const lines = PAIR_INSIGHTS[key] || [
      'You read each other on different frequencies. The work is the translation, and the translation is worth doing.',
      'Compatibility is not a score. It is what happens when both of you stop guessing and start asking.',
    ];
    container.innerHTML = lines.map((line, i) => insightCardHTML(line, lo, i)).join('');
    container.querySelectorAll('[data-insight-whatsapp]').forEach((btn) => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        const text = btn.getAttribute('data-insight-text') || '';
        const msg = encodeURIComponent('Compatibility check for us, this part hit: "' + text + '" — namealigned.com/love-compatibility-numerology');
        window.open('https://wa.me/?text=' + msg, '_blank');
        if (typeof gtag === 'function') {
          gtag('event', 'share_whatsapp', { source: 'pair_insight', pair: lo + '-' + hi });
        }
      });
    });
  }

  function insightCardHTML(line, number, idx) {
    const safe = escapeHTML(line);
    return (
      '<div class="insight-card" data-number="' + number + '">' +
        '<blockquote class="insight-quote">' + safe + '</blockquote>' +
        '<div class="insight-actions">' +
          '<button class="insight-btn insight-btn-copy" type="button" data-insight-copy data-insight-text="' + safe + '" aria-label="Copy insight">Copy</button>' +
          '<button class="insight-btn insight-btn-wa" type="button" data-insight-whatsapp data-insight-text="' + safe + '" aria-label="Send on WhatsApp">Send on WhatsApp</button>' +
        '</div>' +
      '</div>'
    );
  }

  function escapeHTML(s) {
    return String(s || '')
      .replace(/&/g, '&amp;').replace(/</g, '&lt;')
      .replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#39;');
  }

  function shuffle(arr) {
    for (let i = arr.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [arr[i], arr[j]] = [arr[j], arr[i]];
    }
    return arr;
  }

  // Auto-mount on any element with .emotional-insights[data-number].
  function autoMount() {
    document.querySelectorAll('.emotional-insights[data-number]').forEach((el) => {
      const n = parseInt(el.getAttribute('data-number'), 10);
      const c = parseInt(el.getAttribute('data-count'), 10) || 3;
      if (n >= 1 && n <= 9) renderInsightsFor(n, c, el);
    });
    document.querySelectorAll('.emotional-pair-insights[data-pair]').forEach((el) => {
      const pair = (el.getAttribute('data-pair') || '').split('-').map(Number);
      if (pair.length === 2) renderPairInsightsFor(pair[0], pair[1], el);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', autoMount);
  } else {
    autoMount();
  }

  // Expose for explicit programmatic calls (e.g. from analyzer.js).
  window.NA_Insights = {
    renderFor: renderInsightsFor,
    renderPair: renderPairInsightsFor,
    INSIGHTS: INSIGHTS,
    PAIR_INSIGHTS: PAIR_INSIGHTS,
  };
})();
