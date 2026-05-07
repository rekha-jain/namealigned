/* ═══════════════════════════════════════════════════════════════
   AURA — rule-based mystical companion (MVP, no LLM)
   ═══════════════════════════════════════════════════════════════
   Architecture is intentionally swappable so phase 2 can replace
   `Aura.respond()` with an LLM call without rewriting the chat UI
   or memory layer. Inputs/outputs are stable contracts:

     Aura.respond(userText, profile) → string

   Where `profile` is whatever's in localStorage (name, dob,
   birthNum, etc.) — purely additive personalisation.

   Memory layer: localStorage (`aura_state`) — visit count, last
   intents, mood history, profile fragments. Read on init, written
   after each turn.
   ═══════════════════════════════════════════════════════════════ */
(function(){
  'use strict';

  // ── Random helpers ────────────────────────────────────────────
  const pick = (arr) => arr[Math.floor(Math.random() * arr.length)];
  const rand = (min, max) => Math.floor(Math.random() * (max - min + 1)) + min;

  // ── Intent / topic detection ──────────────────────────────────
  // Each intent maps to a bag of keyword stems. First-match wins.
  // Order matters — more specific intents come first.
  const INTENTS = [
    { id: 'safety_blocked',  bag: ['suicide','kill myself','end my life','want to die','self harm'], block: true,
      reply: "I hear you carrying something heavy. I'm not the right place for what you're going through right now — please reach out to a person you trust or a helpline like iCall (9152987821) or AASRA (9820466726). You matter, and your story isn't done."
    },
    { id: 'safety_medical',  bag: ['cancer','tumor','disease','will i die','how long will i live','my illness','my disease','heart attack','stroke'], block: true,
      reply: "That's a question only a doctor can answer responsibly — and you deserve that level of care, not a cosmic guess. I can sit with the energy of waiting, or the fear underneath it, but the medical answer needs a real human in scrubs."
    },
    { id: 'safety_legal',    bag: ['will i win the case','lawsuit win','court case','jail','arrest','divorce settlement amount'], block: true,
      reply: "Legal outcomes need a lawyer, not a cosmic read. I can sit with the emotional weight of waiting on a verdict, but specifics belong to someone with case files."
    },
    { id: 'safety_money',    bag: ['stock pick','should i buy bitcoin','lottery numbers','horse race','share price','will i become rich'], block: true,
      reply: "Specific financial bets aren't something I'd guide on — money decisions deserve a planner who knows your numbers, not your stars. I can talk about your relationship with money though, if that helps."
    },
    { id: 'career',   bag: ['job','promotion','promote','career','work','boss','manager','salary','raise','increment','business','startup','founder','client','interview','resign','quit','fire','laid off'], topic: 'career' },
    { id: 'love',     bag: ['love','partner','marriage','marry','wife','husband','boyfriend','girlfriend','crush','soulmate','dating','breakup','break up','divorce','ex','relationship','romance','heartbreak','cheated','left me','rejected'], topic: 'love' },
    { id: 'family',   bag: ['mother','father','mom','dad','parent','sibling','brother','sister','child','son','daughter','family','in-law','in law','inlaw'], topic: 'family' },
    { id: 'friendship', bag: ['friend','friendship','best friend','colleague','coworker'], topic: 'friend' },
    { id: 'health',   bag: ['health','tired','exhausted','burnout','burn out','anxiety','anxious','panic','depressed','depression','sleep','insomnia'], topic: 'health' },
    { id: 'self',     bag: ['lost','stuck','confused','unsure','no purpose','meaning','why am i','who am i','myself','self','identity','direction','lonely','alone','empty','worthless','self-worth','self worth'], topic: 'self' },
    { id: 'future',   bag: ['future','will i','when will','how long','next year','this year','soon','what happens'], topic: 'future' },
    { id: 'spiritual',bag: ['spiritual','soul','karma','past life','god','universe','energy','aura','destiny','fate','sign','signs'], topic: 'spiritual' },
    { id: 'unlucky',  bag: ['unlucky','bad luck','curse','jinx','everything goes wrong','nothing works'], topic: 'self' },
    { id: 'rude',     bag: ['stupid','dumb','fake','scam','useless','idiot','sucks','bullshit','fuck','shit','wtf','liar','lying','rubbish','nonsense'], rude: true },
    { id: 'greeting', bag: ['hi','hello','hey','namaste','aura','good morning','good evening','good night'] },
    { id: 'thanks',   bag: ['thank you','thanks','grateful','appreciate'] },
    { id: 'who_are_you', bag: ['who are you','what are you','are you ai','are you real','are you human'] },
  ];

  function detectIntent(text){
    const t = (text||'').toLowerCase();
    for (const intent of INTENTS) {
      if (intent.bag.some(k => t.includes(k))) return intent;
    }
    return { id: 'general', topic: 'general' };
  }

  // ── Emotional tone detection (overlay on top of intent) ──────
  function detectTone(text){
    const t = (text||'').toLowerCase();
    if (/\b(scared|afraid|fear|anxious|worried|panic|nervous)\b/.test(t)) return 'anxious';
    if (/\b(tired|exhausted|drained|burnt|burnout|empty|spent)\b/.test(t)) return 'exhausted';
    if (/\b(angry|furious|frustrated|annoyed|hate|fed up)\b/.test(t)) return 'angry';
    if (/\b(sad|crying|hurt|broken|heartbroken|miserable|alone|lonely)\b/.test(t)) return 'sad';
    if (/\b(confused|lost|don.?t know|stuck|unsure|mixed up)\b/.test(t)) return 'confused';
    if (/\b(excited|happy|grateful|amazing|finally|wonderful)\b/.test(t)) return 'positive';
    if (/[?]/.test(t)) return 'questioning';
    return 'neutral';
  }

  // ── Block libraries (modular, recombinable) ──────────────────
  const VALIDATION = {
    career: [
      "Your energy around work feels weighted right now — like you're carrying a question you haven't fully named.",
      "There's a low hum of restlessness in your career field — the kind that means you've outgrown something.",
      "I'm picking up a quiet kind of impatience. The work you're doing is fine, but a part of you is asking for more.",
      "Your work energy reads as in-between — not stuck, not flowing, just rearranging.",
    ],
    love: [
      "Your heart energy is doing more than you're consciously aware of — there's a lot moving underneath.",
      "I sense a tenderness around love right now. Something's either softening or recalibrating.",
      "Your relationship field feels active — not chaotic, but in motion. The energy isn't flat.",
      "There's a quiet ache here, the kind that lives in old patterns asking to be released.",
    ],
    family: [
      "Family energy carries the longest patterns — and yours feels like one of those is asking for re-examination.",
      "I'm sensing something inherited in this — not a wound, just a pattern that's run its course.",
      "Your family field reads as gentle but layered. Old roles, current selves, all in the same room.",
    ],
    friend: [
      "Friendships are the quiet measure of where you're growing — and your circle feels like it's shifting weight.",
      "I sense some friendships expanding and others quietly closing. That's not a tragedy, that's seasons.",
    ],
    health: [
      "Your nervous system feels like it's been holding too much for too long.",
      "There's an exhaustion in your energy that isn't just about sleep — it's about emotional output that hasn't matched intake.",
      "I can sense the tiredness has roots beneath the obvious causes.",
    ],
    self: [
      "Your aura feels like it's reorganising — not lost, just between identities.",
      "There's a real sincerity in how you're sitting with yourself right now. Most people avoid this depth.",
      "You're carrying more than you let yourself acknowledge.",
      "Your inner field reads as transitional — old answers don't fit, new ones haven't fully arrived.",
    ],
    future: [
      "Your timeline feels open — there are several real possibilities ahead, not one fixed road.",
      "The future you're asking about is closer than you think, but it's arriving on its own pace.",
    ],
    spiritual: [
      "Your spiritual field is unusually open right now — that's both a gift and an asking.",
      "I sense a part of you that's been waiting for a real question, and you're starting to ask it.",
    ],
    general: [
      "Your energy reads thoughtfully today — there's something circling, even if it hasn't fully named itself yet.",
      "There's a stillness around your question that means it matters to you, even if it sounds casual.",
      "I sense more underneath this than the words alone — there's a real ask here.",
    ],
  };

  const INTERPRETATION = {
    career: [
      "The cosmic pattern is pointing toward visibility — your work has been quieter than its real weight.",
      "Recognition energy is building, but slowly. Saturn-led growth: late, then certain.",
      "What you're building is working; the lag is in how the world catches up with what you can already see.",
      "You're in a setup phase. The harvest is next year's question, not this month's.",
    ],
    love: [
      "Mercury and Venus are doing quiet work here — communication and aesthetic rhythm both want attention.",
      "The pattern is asking for honesty, not strategy. Whatever you've been editing in conversation needs to come out.",
      "An old emotional template is loosening — you can feel it in how you respond differently lately.",
      "This relationship phase is teaching boundaries through gentle pressure, not crisis.",
    ],
    family: [
      "An old role is being quietly retired. You're not the version of yourself the family system was built around.",
      "What feels like distance is actually individuation — necessary, even when uncomfortable.",
    ],
    friend: [
      "Friend circles tend to mirror who you're becoming. The shift you're feeling is recognition, not loss.",
      "Some friendships ask to deepen now; some ask to be honoured and released.",
    ],
    health: [
      "The body is asking for a rhythm it can trust — the same time daily, the same handful of habits, repeated.",
      "Your energetic battery is recharging through stillness, not through more doing.",
    ],
    self: [
      "You're in the middle of an internal recalibration — slower than you'd like, more permanent than it feels.",
      "The question of meaning is itself a sign that meaning is on its way; the empty asks are usually closer than full ones.",
      "You're shedding an older version of yourself faster than you're meeting the new one. The gap is uncomfortable but temporary.",
    ],
    future: [
      "The next 90 days carry a clarity arrival — something currently fuzzy will sharpen.",
      "Cycles like this one tend to break open when you least expect, often through a small unrelated event.",
    ],
    spiritual: [
      "The spiritual life rarely arrives through dramatic sign — it arrives through your patience with ordinary moments.",
      "Whatever practice keeps reappearing in your thoughts is the one to start with.",
    ],
    general: [
      "The pattern around you isn't dramatic, just persistent — small adjustments compound more than one big move would.",
      "What's coming next looks like clarity through narrowing — fewer paths, but the right ones.",
    ],
  };

  const FUTURE = {
    career:    ["Within the next 2–4 months, a recognition or opening is likely to surface.", "Your visibility cycle is climbing — by next quarter, momentum should feel different."],
    love:     ["Within 60–90 days, an emotional clarity is likely — either deepening or honest closure.", "The love-energy timeline you're in is short; expect the question to answer itself within 3 months."],
    family:   ["This pattern usually resolves through small honest conversations, not big confrontations.", "A shift in how a key family relationship feels is likely within the next season."],
    friend:   ["The next few months will tell you which friendships are foundational and which were companionable.", "An unexpected reconnection is likely soon."],
    health:   ["A two-week reset would shift more than you'd predict.", "The next few weeks favour gentleness; pushing harder works against you."],
    self:    ["The recalibration period typically holds 6–10 weeks; you're partway through.", "Your new self is closer than the inner narrative suggests."],
    future:   ["The clarity you're asking about is statistically close — within the same season.", "The wait is shorter than the asking suggests."],
    spiritual:["A practice will choose you within weeks if you stay open.", "The spiritual answer arrives in fragments first, then in pattern."],
    general:  ["The next steady stretch should feel different from the one you've been in.", "Movement opens gradually rather than all at once."],
  };

  const METAPHOR = {
    career: ["This phase feels like a bow being pulled back — the release is what you'll remember, not the tension.", "You're in the slow part of a curve; the steep part is just out of view."],
    love: ["The heart's tide is going out before it comes back in; that's not loss, that's rhythm.", "Two souls learning each other's frequency is rarely silent work."],
    family: ["Family is the soil — sometimes it composts what no longer serves, before the next season grows.", "Some inherited rooms need to be walked out of, not redecorated."],
    friend: ["Some seasons close one circle gently to make room for a different shape of circle.", "Friendships have tides too — yours is in a turning."],
    health: ["The body is the slowest, most honest oracle you have.", "You're not running out — you're being asked to refill."],
    self: ["You're between identities the way a snake is between skins — uncomfortable, necessary, beautiful afterward.", "The ground feels uncertain because it's been freshly turned."],
    future: ["The unknown isn't empty; it's just unwritten.", "The path looks unclear because you're standing too close to a curve."],
    spiritual: ["The mystical isn't far away — it's the depth of how you greet the next ordinary thing.", "Your soul's questions don't shout; they hum, and you listen better in quiet."],
    general: ["This isn't a dead end — it's a long pause before a new sentence.", "You're holding a question shaped like a key; it'll fit the door soon."],
  };

  const HOOK = {
    career: ["What part of your work feels most unresolved right now?", "If you couldn't fail, what would you actually want next?", "Is this more about the role, or the recognition?"],
    love: ["What's the conversation you've been avoiding?", "If you trusted what you already feel, what would change?", "Does this feel more like a beginning or a long-overdue ending?"],
    family: ["Which family pattern keeps showing up as your own?", "Whose approval are you still waiting for?"],
    friend: ["Which friendship feels foundational right now, and which feels seasonal?"],
    health: ["What rhythm feels most missing in your week?", "If your body could speak in one sentence, what would it say?"],
    self: ["What part of who you are now wasn't true a year ago?", "What's the question you haven't dared to fully ask yourself yet?", "What would change if you trusted what you already know?"],
    future: ["What outcome would feel like the universe was paying attention?", "If you could fast-forward 90 days and ask one question, what would it be?"],
    spiritual: ["What practice keeps reappearing in your mind?", "Which experience in the past year felt almost-spiritual?"],
    general: ["What's been weighing on you most lately?", "Does this question feel more emotional or practical?", "Tell me the part you didn't say first."],
  };

  // ── Numerology personalisation overlays ──────────────────────
  // When profile.birthNum / nameNum exist, Aura weaves a planet-
  // anchored line into the response.
  const PLANET_BY_NUM = ['','Sun','Moon','Jupiter','Rahu','Mercury','Venus','Ketu','Saturn','Mars'];
  const NUM_TRAITS = {
    1:'Sun-led — leadership without permission, and visibility that finds you whether you want it or not.',
    2:'Moon-led — emotionally porous, partnership-oriented, deeply intuitive.',
    3:'Jupiter-led — expressive, expansive, drawn to teaching and abundance.',
    4:'Rahu-led — unconventional, ahead of the consensus, often misread before you are understood.',
    5:'Mercury-led — fast, adaptive, communicative, hard to confine.',
    6:'Venus-led — relational, aesthetic, devoted, emotionally fluent.',
    7:'Ketu-led — depth-oriented, contemplative, more comfortable with questions than answers.',
    8:'Saturn-led — disciplined, long-game, authority earned through endurance.',
    9:'Mars-led — courageous, decisive, energy that runs hot and protective.',
  };
  function numerologyOverlay(profile){
    if (!profile || !profile.birthNum) return null;
    const planet = PLANET_BY_NUM[profile.birthNum] || '';
    const trait  = NUM_TRAITS[profile.birthNum] || '';
    return profile.firstName
      ? `${profile.firstName}, your Birth Number ${profile.birthNum} (${planet}) is ${trait}`
      : `Your Birth Number ${profile.birthNum} (${planet}) is ${trait}`;
  }

  // ── Special-case responders ──────────────────────────────────
  function greetingResponse(profile){
    const opener = profile && profile.firstName
      ? `Hello, ${profile.firstName}.`
      : pick(['Hello, traveller.','Hi there.','Hello.','Welcome back.']);
    const middle = pick([
      "I'm Aura — a quiet companion for the questions that don't fit easily into a Google search.",
      "I'm Aura — your cosmic confidante. Tell me what's on your mind today, and I'll meet it where it is.",
      "I'm Aura. I read the energy beneath words. What's circling for you today?",
    ]);
    return `${opener} ${middle}`;
  }
  function whoAreYouResponse(){
    return "I'm Aura — a mystical companion designed to help you sit with questions you don't fully know how to ask yet. I read intent and emotion, draw on Chaldean numerology when you share your details, and reflect back the patterns I sense. I don't predict the future like a fortune-teller — I help you notice what your own intuition is already saying.";
  }
  function thanksResponse(){
    return pick([
      "You're welcome. Come back when you need to think out loud.",
      "Always. The conversation continues whenever you do.",
      "Anytime. The questions matter more than the answers.",
    ]);
  }
  function rudeResponse(){
    return pick([
      "Storm-cloud aura detected ⚡. Something underneath the frustration usually has the real story — what's actually heavy today?",
      "That energy felt sharp 🌙. I'm not offended — I just notice when the heat is masking something tender. Want to tell me what's actually going on?",
      "Strong words 🔥. There's almost always a quieter feeling under sharp ones — what's the real thing?",
    ]);
  }
  function blockedResponse(intent){
    return intent.reply;
  }

  // ── Main response composer ───────────────────────────────────
  function compose(intent, tone, profile){
    const topic = intent.topic || 'general';
    const v = pick(VALIDATION[topic] || VALIDATION.general);
    const i = pick(INTERPRETATION[topic] || INTERPRETATION.general);
    const f = pick(FUTURE[topic] || FUTURE.general);
    const m = pick(METAPHOR[topic] || METAPHOR.general);
    const h = pick(HOOK[topic] || HOOK.general);

    // Numerology overlay (used at most 30% of the time when present)
    const overlay = numerologyOverlay(profile);
    const useOverlay = overlay && Math.random() < 0.45;

    // Tone-aware micro-adjustment
    let prefix = '';
    if (tone === 'sad')        prefix = 'I want to start by saying — that\'s a real thing you\'re carrying. ';
    else if (tone === 'angry') prefix = 'There\'s heat in this, and that\'s OK. ';
    else if (tone === 'anxious')prefix = 'Take a breath with me first. ';
    else if (tone === 'exhausted')prefix = 'Even before I answer — yes, you\'re tired, and that\'s real. ';

    // Compose ~3-5 sentences total. Skip metaphor sometimes for variety.
    const useMetaphor = Math.random() < 0.6;
    const parts = [prefix + v, i];
    if (useOverlay) parts.push(overlay);
    parts.push(f);
    if (useMetaphor) parts.push(m);
    parts.push(h);
    return parts.filter(Boolean).join(' ');
  }

  // ── Memory layer (localStorage) ──────────────────────────────
  const STORAGE_KEY = 'aura_state_v1';
  function loadState(){
    try { return JSON.parse(localStorage.getItem(STORAGE_KEY)) || {}; }
    catch(e){ return {}; }
  }
  function saveState(state){
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(state)); } catch(e){}
  }
  function recordTurn(state, intent, tone){
    state.visits = (state.visits || 0) + 1;
    state.lastTurnAt = Date.now();
    state.recentIntents = (state.recentIntents || []).concat([intent.id]).slice(-10);
    state.recentTones   = (state.recentTones || []).concat([tone]).slice(-10);
  }
  function recurringTopic(state){
    if (!state.recentIntents || state.recentIntents.length < 4) return null;
    const counts = {};
    for (const i of state.recentIntents) counts[i] = (counts[i]||0)+1;
    let top = null, topN = 0;
    for (const k in counts) if (counts[k] > topN){ top = k; topN = counts[k]; }
    return topN >= 3 ? top : null;
  }

  // ── Public API (the swappable contract) ──────────────────────
  window.Aura = {
    /**
     * respond(userText, profile) → string
     * Profile is optional and additive: { firstName, dob, birthNum, destNum, nameNum }.
     * Phase 2 can replace this body with an LLM call without touching the chat UI.
     */
    respond(text, profile){
      profile = profile || {};
      const intent = detectIntent(text);
      const tone   = detectTone(text);
      const state  = loadState();

      // Hard-blocked safety topics: return canned response, do NOT compose.
      if (intent.block) {
        recordTurn(state, intent, tone); saveState(state);
        return blockedResponse(intent);
      }
      // Special intents that don't need the full composer.
      if (intent.id === 'rude')        { recordTurn(state, intent, tone); saveState(state); return rudeResponse(); }
      if (intent.id === 'greeting')    { recordTurn(state, intent, tone); saveState(state); return greetingResponse(profile); }
      if (intent.id === 'thanks')      { recordTurn(state, intent, tone); saveState(state); return thanksResponse(); }
      if (intent.id === 'who_are_you') { recordTurn(state, intent, tone); saveState(state); return whoAreYouResponse(); }

      // Standard composed response with optional recurring-topic preface.
      let preface = '';
      const topic = recurringTopic(state);
      if (topic && topic === intent.id && state.visits > 1 && Math.random() < 0.5) {
        const friendly = topic.replace('_',' ');
        preface = `You've been circling ${friendly} energy a lot lately — I notice. `;
      }

      recordTurn(state, intent, tone);
      saveState(state);

      return preface + compose(intent, tone, profile);
    },

    /** Persist profile (called from the chat page when user provides DOB/name). */
    saveProfile(profile){
      const state = loadState();
      state.profile = Object.assign({}, state.profile, profile);
      saveState(state);
    },
    loadProfile(){ return (loadState().profile) || null; },
    clear(){ try { localStorage.removeItem(STORAGE_KEY); } catch(e){} },

    /** Debug-only: surface state to the page console. */
    _state: () => loadState(),
  };
})();
