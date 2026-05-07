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

  // Hooks are GENTLE invitations, never demands. They're optional —
  // most turns won't include one. Goal: never feel like prying.
  const HOOK = {
    career: ["If anything wants to be named about the work, I'm here for it — no rush.", "Share as much or as little about the work as feels right."],
    love: ["Whatever you'd like to share about this — or not — is welcome.", "I'll meet you wherever you are with this. No pressure to explain."],
    family: ["Family stuff often takes time to put into words — take yours.", "Whatever feels safe to share is enough."],
    friend: ["No need to spell it out — just being with the feeling is enough."],
    health: ["Rest the question if it's heavy. I'll be here when you want to come back to it."],
    self: ["You don't have to have words for it yet — being with it counts.", "Whatever rises is welcome. No need to perform clarity."],
    future: ["Ask anything specific about the road ahead — I'll answer warmly."],
    spiritual: ["Sit with it gently. The asking is already part of the answer."],
    general: ["Ask whatever you'd like — I'll meet it with care.", "Whatever's on your heart, share it as it comes."],
  };

  // Warm closers — alternative to hooks. Used when pushback is detected,
  // or randomly chosen so most replies end with warmth rather than a question.
  const WARM_CLOSE = [
    "I'm here, however you'd like to use me.",
    "Take this gently — there's no rush.",
    "Whatever you bring next, I'll meet you in it.",
    "Sit with this as long as you need.",
    "I'm with you in this.",
    "You're not alone in the asking.",
  ];

  // Plain-language read for direct/pushback questions about the
  // road ahead. Used when user says 'just tell me' / 'what's in
  // the stars' / 'next 12 months'. Warm, specific, no probing.
  const DIRECT_FUTURE = [
    "The next 12 months read in three movements. The first quarter is quiet groundwork — small, unglamorous decisions that turn out to matter. Mid-year brings a visible shift in either work or a close relationship — a clarity you've been waiting for. The final stretch feels like consolidation: you'll be standing somewhere noticeably steadier than you are now. Nothing dramatic, but the cumulative effect is real.",
    "Looking ahead a year: expect an early-year recalibration — a few things you've been carrying will quietly fall away. A meaningful opening (a person, a role, a decision) appears around the middle, often through an unexpected channel. By late year, what feels uncertain right now will have a name and a direction. The arc is gentle but unmistakably forward.",
    "The 12 months ahead carry a slow-then-fast rhythm. The first months ask for patience — things are moving underground. Around mid-year, a single decision or conversation reorganises the picture. The last third is where the year shows what it was building toward — usually clearer relationships, clearer work, clearer self. You'll look back and see it was all preparation.",
  ];

  // ── Elaboration responses (when user asks "what do you mean") ──
  // Keyed off the LAST topic Aura was speaking about. These don't
  // re-ask a hook — they explain what was meant in plainer language
  // and offer a follow-up reflection or example.
  const ELABORATION = {
    career: [
      "I mean the gap between what you can see is possible and how slowly the world catches up. You've often outgrown a role or a label months before it shows up in your title or pay — that's the lag I'm pointing at.",
      "Translated plainly: your career energy reads like you've quietly raised your own bar, but the external markers (recognition, money, scope) haven't caught up yet. That's not failure, that's a normal lag.",
    ],
    love: [
      "I mean the part of love that's working underneath conscious thought — the way you read your partner's mood before they say a word, or the small editing you do in conversations to avoid friction. That's what's actually shaping the relationship right now, more than any one event.",
      "Plainly: there's a pattern in how you love that's quietly running. Not bad, not loud, but it shapes the relationship more than the dramatic moments do.",
    ],
    family: [
      "I mean the role you got assigned in your family system years ago — the responsible one, the easy one, the rebel — that role isn't who you are anymore, but the family is still relating to you as if it is. The friction you feel is that mismatch.",
      "Translated: family operates on patterns set when you were younger. You've changed; the pattern hasn't fully updated. The discomfort is that update happening, not something going wrong.",
    ],
    friend: [
      "I mean some friendships were companionable for a particular life-stage, and you're past that stage now. That's not a betrayal of the friendship — it's seasons. Some will translate to the next stage, some won't, and both are okay.",
    ],
    health: [
      "I mean your nervous system has been outputting more than it's been allowed to recover from. Tiredness with roots beyond sleep — emotional output, decision fatigue, holding-it-together energy.",
      "Translated: you can't out-sleep emotional exhaustion. The body is asking for predictable rhythm and recovery, not just more rest.",
    ],
    self: [
      "I mean you're between identities — the older version of yourself doesn't fully fit anymore, but the newer version hasn't fully arrived. The 'lost' feeling isn't lostness, it's the gap. Most people skip noticing this and rush to be definitive again; the noticing itself is growth.",
      "Translated: you're not stuck, you're shedding. The discomfort is the in-between, and in-betweens are temporary by definition.",
    ],
    future: [
      "I mean the timeline you're asking about isn't fixed — there are several real possibilities ahead, depending on small decisions you'll make in the next few weeks. The future is closer than 'someday' but more responsive than 'destined'.",
    ],
    spiritual: [
      "I mean the spiritual life rarely arrives with a sign or thunderbolt. It arrives in how you greet the next ordinary moment with more presence than the last. That's not metaphor — that's the actual mechanism.",
    ],
    general: [
      "Let me put that more plainly: the pattern I'm sensing isn't a single dramatic event, it's a recurring small one. Small repeated things shape lives more than rare big ones do.",
      "I'll translate: there's a question circling that you haven't fully named yet, and the energy around it is the unnamed-ness, more than the question itself.",
    ],
  };

  // Specific hook → reflective elaboration map. Used when the user
  // quotes back a hook Aura asked. Plain-English unpack of the
  // question + an invitation to actually answer it.
  const HOOK_UNPACKS = [
    { match: /if you couldn.?t fail/i,
      reply: "That question isn't a strategy puzzle — it's a permission test. Most people answer it as if there's a 'right' answer hiding somewhere. There isn't. The exercise is to notice what comes up first before you edit it. Whatever surfaces in the first 5 seconds usually says more about you than the polished answer that follows. So — when you ask yourself it for real, what's the first thing that came up, even if it didn't make sense?" },
    { match: /conversation you.?ve been avoiding/i,
      reply: "I mean the one specific conversation that's been sitting in your gut for weeks — the one you've half-rehearsed, half-rationalised, never started. You usually know exactly which one I mean. The asking itself is what loosens it." },
    { match: /weighing on you most/i,
      reply: "Plain version: which thing — when you wake up and your mind is too quiet to perform — surfaces first? Not the most urgent or important. The most undealt-with. That one." },
    { match: /more emotional or practical/i,
      reply: "I'm asking which kind of answer would actually help. Practical answers fix circumstances; emotional answers fix how you're holding the circumstances. They feel similar but they're different work. Which one would let you sleep tonight?" },
    { match: /role, or the recognition/i,
      reply: "I'm asking whether the discomfort is about the work itself (role) or about being seen for it (recognition). Both are valid; the fix for each is different. One asks for a different job, the other asks for visibility within this one." },
    { match: /trusted what you already feel/i,
      reply: "I mean the small voice that already knows — the one you've been outvoting with logic, advice from others, fear of being wrong. If you stopped editing what you already feel, what would the next move be?" },
    { match: /what part of who you are now wasn.?t true a year ago/i,
      reply: "Pick a small specific thing. A preference, a tolerance, a 'no' you didn't have last year. Naming it makes the becoming visible to yourself, which is most of the work." },
  ];

  // Detect when the user is pushing back, asking for a direct answer,
  // redirecting, or showing they don't want to be probed further. In
  // these cases Aura should drop the hook entirely and answer warmly
  // and plainly. This is the fix for Aura feeling pry-ish.
  function detectPushback(text){
    const t = (text||'').toLowerCase().trim();
    return /\b(nothing|not really|no,|no\.|no thanks|stop asking|don.?t ask|just tell|tell me (more |)clearly|more clearly|specifically|be (more |)specific|can you (just |please |)(tell|let me know|say|explain)|i (just |)want to know|what.?s (in|ahead|going)|whats (in|ahead|going)|in the stars|next \d|coming \d|12 months|year ahead|i don.?t want to|rather not|prefer not|skip|move on|get to the point|enough questions)\b/.test(t);
  }

  // Detect referent / clarification intents that should NOT start a
  // new topic but instead elaborate on the last response.
  function isReferent(text){
    const t = (text||'').toLowerCase().trim();
    return /\b(what (do|does) (you|that|this) mean|what (do|does) you mean by (this|that)|explain( that)?|elaborate|tell me more|say more|go deeper|what.s that|i don.?t (get|understand)|huh|come again|in plain (english|words))\b/.test(t)
      || (t.length < 25 && /(this|that|it)\??/.test(t) && !/\?$/.test(t)===false);
  }

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

  // Pick a hook that hasn't been used in the last 2 turns. Prevents
  // the "asking the same probing question 3 times in a row" feel.
  function pickFreshHook(topic, state){
    const pool = HOOK[topic] || HOOK.general;
    const recent = (state && state.recentHooks) || [];
    const fresh = pool.filter(h => !recent.includes(h));
    return pick(fresh.length ? fresh : pool);
  }

  // ── Main response composer ───────────────────────────────────
  // direct=true → user wants a warm, plain answer with no probing
  // hooks. Triggered by detectPushback() upstream.
  function compose(intent, tone, profile, state, direct){
    const topic = intent.topic || 'general';
    const v = pick(VALIDATION[topic] || VALIDATION.general);
    const i = pick(INTERPRETATION[topic] || INTERPRETATION.general);
    const f = pick(FUTURE[topic] || FUTURE.general);
    const m = pick(METAPHOR[topic] || METAPHOR.general);

    // Numerology overlay (used at most 30% of the time when present)
    const overlay = numerologyOverlay(profile);
    const useOverlay = overlay && Math.random() < 0.45;

    // Tone-aware micro-adjustment — warm, accepting opener
    let prefix = '';
    if (tone === 'sad')        prefix = "I hear you, and what you're carrying is real. ";
    else if (tone === 'angry') prefix = "I'm here for the heat — no judgement. ";
    else if (tone === 'anxious')prefix = "Take a breath with me. You're safe in this conversation. ";
    else if (tone === 'exhausted')prefix = "You're tired, and that's allowed to be true. ";
    else if (tone === 'confused')prefix = "It's okay not to know yet — I'll meet you in the not-knowing. ";

    const parts = [prefix + v, i];
    if (useOverlay) parts.push(overlay);

    // For direct/pushback turns: skip metaphor + skip hook,
    // give the future read clearly, then close warmly.
    if (direct) {
      // For broad future-questions, use the rich 12-month read.
      const askingFuture = topic === 'future' || /future|year|month|ahead|next|stars/i.test(state && state.lastUserText || '');
      if (askingFuture) {
        parts.push(pick(DIRECT_FUTURE));
      } else {
        parts.push(f);
      }
      parts.push(pick(WARM_CLOSE));
      if (state) { state.lastTopic = topic; state.lastHook = ''; }
      return parts.filter(Boolean).join(' ');
    }

    parts.push(f);

    // Skip metaphor sometimes for variety
    const useMetaphor = Math.random() < 0.5;
    if (useMetaphor) parts.push(m);

    // Hook is now OPTIONAL (~40% chance). Most turns end with a warm
    // close instead of a probing question. Avoid repeating recent hooks.
    const useHook = Math.random() < 0.4;
    let h = '';
    if (useHook) {
      h = pickFreshHook(topic, state);
      parts.push(h);
    } else {
      parts.push(pick(WARM_CLOSE));
    }

    // Remember the hook + topic so the next turn can elaborate on it
    if (state) {
      state.lastHook  = h;
      state.lastTopic = topic;
      if (h) state.recentHooks = (state.recentHooks || []).concat([h]).slice(-3);
    }
    return parts.filter(Boolean).join(' ');
  }

  // Build an elaboration response for the LAST topic (when user asks
  // 'what do you mean'). Tries to match a specific hook the user is
  // quoting first; falls back to the topic-level elaboration.
  function elaborate(text, state, profile){
    const lastTopic = state.lastTopic || 'general';
    const lastHook  = state.lastHook  || '';
    const t = (text||'').toLowerCase();

    // Did the user echo / quote the previous hook? If so, unpack it.
    if (lastHook) {
      for (const u of HOOK_UNPACKS) {
        // Match if the user echoed the hook OR the hook itself matches
        if (u.match.test(t) || u.match.test(lastHook)) {
          return u.reply;
        }
      }
    }
    // Topic-level elaboration as fallback.
    const lines = ELABORATION[lastTopic] || ELABORATION.general;
    let body = pick(lines);

    // Add a soft personal touch when name is known
    if (profile && profile.firstName && Math.random() < 0.5) {
      body = `${profile.firstName}, ${body[0].toLowerCase()}${body.slice(1)}`;
    }
    // Open invitation to keep going
    const invites = [
      "Does that land closer to what you were sensing?",
      "Want to go further on any one piece of that?",
      "Which part of that resonates the most right now?",
    ];
    return body + ' ' + pick(invites);
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

  // ── AI mode (Gemini via /api/aura) ───────────────────────────
  // The browser POSTs to our Vercel serverless function which holds
  // the Gemini API key server-side. Safety intents are blocked
  // upstream and NEVER sent to the AI. On any failure we fall back
  // to the rule-based composer so the chat never breaks.

  function buildHistory(state){
    const hist = (state && state.history) || [];
    return hist.slice(-6); // last 3 exchanges
  }

  function recordHistory(state, role, content){
    state.history = (state.history || []).concat([{role, content}]).slice(-12);
  }

  async function respondViaApi(text, profile, state){
    const ctrl = new AbortController();
    const tmo = setTimeout(() => ctrl.abort(), 14000);
    try {
      const r = await fetch('/api/aura', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: text,
          profile: {
            firstName: profile && profile.firstName || '',
            birthNum:  profile && profile.birthNum  || null,
          },
          history: buildHistory(state),
        }),
        signal: ctrl.signal,
      });
      clearTimeout(tmo);
      if (!r.ok) throw new Error('api ' + r.status);
      const data = await r.json();
      const out = (data && data.reply || '').trim();
      if (!out) throw new Error('empty');
      return out;
    } finally {
      clearTimeout(tmo);
    }
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
      const tone   = detectTone(text);
      const state  = loadState();

      // CONTEXT FIRST: if the user is clearly asking 'what do you
      // mean' / 'explain that' / quoting back a hook, elaborate on
      // the previous turn instead of starting a new topic. This is
      // the fix for: 'what do you mean by this?' getting treated
      // as a fresh greeting + generic answer.
      if (state.lastTopic && isReferent(text)) {
        const reply = elaborate(text, state, profile);
        recordTurn(state, { id: 'referent', topic: state.lastTopic }, tone);
        // lastTopic / lastHook stay sticky so a 3rd 'tell me more'
        // also works
        saveState(state);
        return reply;
      }

      const intent = detectIntent(text);

      // Hard-blocked safety topics: return canned response, do NOT compose.
      if (intent.block) {
        recordTurn(state, intent, tone); saveState(state);
        return blockedResponse(intent);
      }
      // Special intents that don't need the full composer.
      // Note: skip the 'greeting' intent if we're already mid-conversation
      // and the user is just continuing — prevents the 'Welcome back. I'm
      // Aura — a quiet companion...' re-greeting that breaks immersion.
      const recentlyTalking = state.lastTurnAt && (Date.now() - state.lastTurnAt) < 30 * 60 * 1000;

      if (intent.id === 'rude')        { recordTurn(state, intent, tone); saveState(state); return rudeResponse(); }
      if (intent.id === 'greeting' && !recentlyTalking) {
        recordTurn(state, intent, tone); saveState(state); return greetingResponse(profile);
      }
      if (intent.id === 'thanks')      { recordTurn(state, intent, tone); saveState(state); return thanksResponse(); }
      if (intent.id === 'who_are_you') { recordTurn(state, intent, tone); saveState(state); return whoAreYouResponse(); }

      // If we're in the middle of a topic and the user gives a very
      // short follow-up that has no clear new topic keywords, treat
      // it as continuation of the last topic.
      let workingIntent = intent;
      if (state.lastTopic && intent.id === 'general' && (text||'').trim().length < 60) {
        workingIntent = { id: state.lastTopic, topic: state.lastTopic };
      }

      // Standard composed response with optional recurring-topic preface.
      let preface = '';
      const topic = recurringTopic(state);
      if (topic && topic === workingIntent.id && state.visits > 1 && Math.random() < 0.4 && !recentlyTalking) {
        const friendly = topic.replace('_',' ');
        preface = `You've been circling ${friendly} energy a lot lately — I notice. `;
      }

      // Stash user text so compose() can detect future-asking phrasing
      state.lastUserText = text;

      // If the user is pushing back / asking for a direct answer, drop
      // the probing hook and answer warmly + plainly.
      const direct = detectPushback(text);

      recordTurn(state, workingIntent, tone);
      const composed = compose(workingIntent, tone, profile, state, direct);
      saveState(state);  // saves lastHook/lastTopic written by compose

      return preface + composed;
    },

    /**
     * respondAsync(userText, profile) → Promise<string>
     * AI-first path. Safety intents intercepted upstream and never
     * sent to the AI. On any failure, falls back to rule-based.
     */
    async respondAsync(text, profile){
      profile = profile || {};
      const state = loadState();
      const tone  = detectTone(text);

      // SAFETY FIRST — block before any AI call.
      const intent = detectIntent(text);
      if (intent.block) {
        recordTurn(state, intent, tone);
        recordHistory(state, 'user', text);
        recordHistory(state, 'assistant', intent.reply);
        saveState(state);
        return intent.reply;
      }

      // AI path — Gemini via our serverless function
      try {
        const reply = await respondViaApi(text, profile, state);
        if (!reply) throw new Error('empty');
        recordTurn(state, intent, tone);
        recordHistory(state, 'user', text);
        recordHistory(state, 'assistant', reply);
        state.lastTopic = intent.topic || 'general';
        state.lastUserText = text;
        saveState(state);
        return reply;
      } catch (err) {
        // Network / auth / timeout — quietly fall back.
        // Console-log only; the user shouldn't see it.
        try { console.warn('[Aura] AI fallback to rules:', err && err.message); } catch(e){}
        return this.respond(text, profile);
      }
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
