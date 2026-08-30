/* ═══════════════════════════════════════════════════════════════
   NUMEROLOGY ENGINE, Chaldean system (shared across all pages)
   ═══════════════════════════════════════════════════════════════ */

const CHALDEAN={A:1,B:2,C:3,D:4,E:5,F:8,G:3,H:5,I:1,J:1,K:2,L:3,M:4,N:5,O:7,P:8,Q:1,R:2,S:3,T:4,U:6,V:6,W:6,X:5,Y:1,Z:7};

function chalSum(n){let s=0;for(let c of n.toUpperCase())if(CHALDEAN[c])s+=CHALDEAN[c];return s;}
function reduce(n){while(n>9){let s=0;for(let d of String(n))s+=+d;n=s;}return n;}
function getBirthNum(dob){return reduce(parseInt(dob.split('-')[2]));}
function getDestinyNum(dob){let s=0;for(let c of dob.replace(/-/g,''))s+=+c;return reduce(s);}
function getNameNum(name){const raw=chalSum(name.replace(/\s/g,''));return{raw,reduced:reduce(raw)};}
function getPlanet(n){return['','Sun','Moon','Jupiter','Rahu','Mercury','Venus','Ketu','Saturn','Mars'][n]||'Sun';}
function getPersonalYear(dob,year){let s=0;const p=dob.split('-');for(let c of(p[1]+p[2]+String(year)))s+=+c;return reduce(s);}
// ── LO SHU GRID ───────────────────────────────────────────────
// Repetition carries meaning in Lo Shu, so counts are the primary result and
// the presence Set is derived from them. getLoshuNums used to build the Set
// directly, which silently discarded repeats; it is kept for callers that only
// need present-vs-missing.
function getLoshuCounts(dob){const c={1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0};for(let ch of dob.replace(/-/g,''))if(ch!=='0'&&c[ch]!==undefined)c[ch]++;return c;}
function getLoshuNums(dob){const c=getLoshuCounts(dob),p=new Set();for(let n=1;n<=9;n++)if(c[n])p.add(n);return p;}
function getLoshuMissing(dob){const c=getLoshuCounts(dob),m=[];for(let n=1;n<=9;n++)if(!c[n])m.push(n);return m;}

const LOSHU_GRID=[[4,9,2],[3,5,7],[8,1,6]];

// The eight straight lines the 4|9|2 / 3|5|7 / 8|1|6 layout actually contains.
// A line fully present is an arrow of strength; the same line fully absent is
// the corresponding arrow of weakness.
const LOSHU_LINES=[
  {cells:[4,9,2],axis:'Top row',    strength:['Arrow of the Mind','Planning, memory and imagination work together.'],            weakness:['Arrow of Poor Memory','Thoughts scatter before they finish forming.']},
  {cells:[3,5,7],axis:'Middle row', strength:['Arrow of Emotional Balance','Feeling, centre and reflection are all available.'], weakness:['Arrow of Scepticism','Learns by trial and error rather than trust.']},
  {cells:[8,1,6],axis:'Bottom row', strength:['Arrow of Practicality','Ideas reliably become finished things.'],                 weakness:['Arrow of Disorder','Follow-through needs external structure.']},
  {cells:[4,3,8],axis:'Left column',strength:['Arrow of Planning','Naturally organises work into steps.'],                       weakness:['Arrow of Confusion','Order has to be imposed deliberately.']},
  {cells:[9,5,1],axis:'Middle column',strength:['Arrow of Determination','Decides and holds the decision.'],                     weakness:['Arrow of Hesitation','Choices get revisited long after they are made.']},
  {cells:[2,7,6],axis:'Right column',strength:['Arrow of Activity','Emotion converts into visible output.'],                     weakness:['Arrow of Passivity','Waits for momentum instead of starting it.']},
  {cells:[4,5,6],axis:'Diagonal',   strength:['Arrow of Compassion','Reads other people generously and accurately.'],            weakness:['Arrow of Hypersensitivity','Takes correction harder than it is meant.']},
  {cells:[2,5,8],axis:'Diagonal',   strength:['Arrow of Spiritual Insight','Comfortable with what cannot be proven.'],           weakness:['Arrow of Frustration','Effort and reward feel chronically out of step.']},
];

const LOSHU_PLANES=[
  {cells:[4,9,2],name:'Mental plane',   note:'How the person thinks, plans and imagines.'},
  {cells:[3,5,7],name:'Emotional plane',note:'Emotional sensitivity, balance and inner life.'},
  {cells:[8,1,6],name:'Physical plane', note:'How effectively the person acts in the material world.'},
];

function getLoshuArrows(counts){
  const strength=[],weakness=[];
  for(const L of LOSHU_LINES){
    const present=L.cells.filter(n=>counts[n]>0).length;
    if(present===3)      strength.push({cells:L.cells,axis:L.axis,name:L.strength[0],note:L.strength[1]});
    else if(present===0) weakness.push({cells:L.cells,axis:L.axis,name:L.weakness[0],note:L.weakness[1]});
  }
  return {strength,weakness};
}

function getLoshuPlanes(counts){
  return LOSHU_PLANES.map(p=>{
    const filled=p.cells.filter(n=>counts[n]>0).length;
    return {...p,filled,state:filled===3?'complete':filled===0?'empty':'partial'};
  });
}

const FRIENDLY={1:[1,2,3,4,9],2:[1,2,4,7,8],3:[1,3,6,9],4:[1,2,4,6,8],5:[1,3,5,6,9],6:[3,4,5,6,9],7:[1,2,7],8:[2,4,6,8],9:[1,3,5,6,9]};
const PREFERRED=[1,3,5,6,9];
const CAUTION_NAME_NUMS=[4,8];

// ── COMPOUND NUMBER INTELLIGENCE ──────────────────────────────
// q ratings (used by the alignment scorer):
//   'g' = highly supportive       ─ traditional Chaldean fortune compounds
//   'n' = balanced / neutral
//   'b' = challenging             ─ growth-oriented, requires conscious handling
// Labels are deliberately framed as patterns to work with, not omens.
// We never use words like "doomed", "ruin", "danger". Every label
// names a pattern + the inner strength that pattern develops.
const CD={
  10:{q:'g',l:'Wheel of Fortune · Cycles & Reinvention'},
  11:{q:'b',l:'Hidden Patterns · Discernment Required'},
  12:{q:'b',l:'Sacrifice Patterns · Boundary Building'},
  13:{q:'b',l:'Transformational Change · Renewal'},
  14:{q:'g',l:'Magnetic Movement · Travel & Connection'},
  15:{q:'g',l:'The Occultist · Magnetic Influence'},
  16:{q:'b',l:'Sudden Shifts · Resilience Building'},
  17:{q:'g',l:'Star of the Magi · Peace & Love ★'},
  18:{q:'b',l:'Material vs Spiritual Tension'},
  19:{q:'g',l:'The Sun · Most Fortunate Number ★'},
  20:{q:'n',l:'The Awakening · Reflective Judgement'},
  21:{q:'g',l:'Crown of the Magi · Brilliant Success ★'},
  22:{q:'b',l:'Surface vs Depth · Discernment'},
  23:{q:'g',l:'Royal Star of the Lion · Great Fortune ★'},
  24:{q:'g',l:'Love · Money · Creative Power'},
  25:{q:'n',l:'Strength Gained Through Lessons'},
  26:{q:'b',l:'Partnership Recalibration · Self-Trust'},
  27:{q:'g',l:'The Sceptre · Authority & Command'},
  28:{q:'b',l:'Promising Start · Steady Persistence Needed'},
  29:{q:'b',l:'Decision Patterns · Trust Building'},
  30:{q:'n',l:'Thoughtful Reflection · Decisions'},
  31:{q:'b',l:'Solitude Cycles · Inner Strength'},
  32:{q:'g',l:'Magic Power · Unexpected Help ★'},
  33:{q:'g',l:'Spiritual Wisdom & Guidance'},
  34:{q:'g',l:'Spiritual Power · Inner Strength'},
  35:{q:'b',l:'Idealism vs Pragmatism Balance'},
  36:{q:'g',l:'Noble Character · True Leadership'},
  37:{q:'g',l:'Love Life & Friendship · Success'},
  38:{q:'b',l:'Partnership Recalibration · Self-Definition'},
  39:{q:'n',l:'Artistic Vision & Inspiration'},
  40:{q:'n',l:'Spiritual Completion · Order'},
  41:{q:'g',l:'Industrious Success · Ambition'},
  42:{q:'g',l:'Creative Partnerships · Growth'},
  43:{q:'b',l:'Transformational Change Patterns'},
  44:{q:'b',l:'Boundaries Around Excess · Restraint'},
  45:{q:'g',l:'Idealism & Noble Service'},
  46:{q:'g',l:'Leadership & Authority Success'},
  47:{q:'g',l:'Spiritual Protection · Blessings'},
  48:{q:'b',l:'Resistance Patterns · Resilience'},
  49:{q:'n',l:'Humanitarian Vision · Wisdom'},
  50:{q:'g',l:'New Cycle · Fresh Beginnings'},
  51:{q:'g',l:'Power to Lead · The Sword'},
  52:{q:'g',l:'Communication Gifts · Eloquence'}
};

const PLANET_ATTRS={
  1:{color:'Gold · Orange · Red',gem:'Ruby',day:'Sunday',metal:'Gold',element:'Fire'},
  2:{color:'White · Silver · Cream',gem:'Pearl · Moonstone',day:'Monday',metal:'Silver',element:'Water'},
  3:{color:'Yellow · Cream · Violet',gem:'Yellow Sapphire',day:'Thursday',metal:'Gold',element:'Ether'},
  4:{color:'Blue · Electric · Grey',gem:'Hessonite (Gomed)',day:'Saturday',metal:'Mixed',element:'Air'},
  5:{color:'Green · Light Grey',gem:'Emerald',day:'Wednesday',metal:'Bronze',element:'Earth'},
  6:{color:'Pink · White · Pastel Blue',gem:'Diamond · White Sapphire',day:'Friday',metal:'Silver',element:'Water'},
  7:{color:'Violet · Purple · Grey',gem:"Cat's Eye",day:'Monday',metal:'Mixed',element:'Air'},
  8:{color:'Black · Dark Blue · Dark Grey',gem:'Blue Sapphire',day:'Saturday',metal:'Iron · Lead',element:'Air'},
  9:{color:'Red · Crimson · Deep Orange',gem:'Red Coral (Moonga)',day:'Tuesday',metal:'Copper',element:'Fire'},
};

const CAREER_DOMAINS={
  1:['Leadership & Management','Government & Politics','Entrepreneurship','Armed Forces','Gold & Gemstone Trade'],
  2:['Hospitality & Food','Counselling & Psychology','Nursing & Caregiving','Arts & Music','Real Estate'],
  3:['Education & Teaching','Law & Justice','Banking & Finance','Philosophy','Spirituality & Religion'],
  4:['Engineering & Architecture','IT & Technology','Research & Analysis','Logistics','Real Estate Development'],
  5:['Media & Journalism','Sales & Marketing','Travel & Tourism','Stock Trading','Digital Startups'],
  6:['Fashion & Design','Entertainment & Film','Hospitality','Cosmetics & Beauty','Social Work'],
  7:['Research & Science','Spirituality & Healing','Writing & Literature','Astrology & Mysticism','Philosophy'],
  8:['Finance & Banking','Law & Courts','Mining & Heavy Industry','Import/Export','Real Estate Investment'],
  9:['Military & Defense','Surgery & Medicine','Sports & Athletics','Politics','Social Activism & NGO'],
};

const COMPAT_PARTNERS={
  1:{best:[1,2,4,9],good:[3,5,6],avoid:[7,8]},
  2:{best:[1,2,7],good:[4,6,8],avoid:[3,5,9]},
  3:{best:[3,6,9],good:[1,5],avoid:[2,4,8]},
  4:{best:[1,2,4,8],good:[6,7],avoid:[3,5,9]},
  5:{best:[1,5,9],good:[3,6],avoid:[2,4,8]},
  6:{best:[3,6,9],good:[1,4,5],avoid:[2,7,8]},
  7:{best:[2,7],good:[1,4,6],avoid:[3,5,8,9]},
  8:{best:[2,4,6,8],good:[1,7],avoid:[3,5,9]},
  9:{best:[1,3,5,9],good:[6,7],avoid:[2,4,8]},
};

const YEAR_THEMES={
  1:'New beginnings · Planting seeds · Launching ventures',
  2:'Patience · Partnerships · Emotional refinement',
  3:'Creativity · Expansion · Communication · Joy',
  4:'Hard work · Discipline · Building foundations',
  5:'Change · Freedom · Travel · Transformation',
  6:'Home · Responsibility · Love · Healing',
  7:'Introspection · Spiritual depth · Inner wisdom',
  8:'Power · Ambition · Financial growth · Recognition',
  9:'Completion · Release · Harvest · Major endings'
};

const REMEDIES={
  1:['Wear gold, orange or red on Sundays to strengthen Sun energy','Face East for important decisions, Sun amplifies eastward','Keep a ruby or red jasper on your desk','Spend 10 minutes in morning sunlight before your workday'],
  2:['Wear white or silver on Mondays to strengthen Moon energy','Journal emotions each evening, Moon energy loves clarity','Keep a pearl or moonstone near your bed','Drink water from a silver vessel'],
  3:['Wear yellow on Thursdays to strengthen Jupiter energy','Teach or share knowledge on Thursdays, Jupiter rewards generosity','Keep a yellow sapphire or citrine in your workspace','Donate books or educational material on Thursdays'],
  4:['Channel Rahu energy into innovation, not routine','Wear deep blue or grey on Saturdays','Avoid starting ventures on dates that add to 4 or 8','Keep hessonite (gomed) only after consulting a gemologist'],
  5:['Wear green on Wednesdays to strengthen Mercury energy','Speak and write with precision on Wednesdays','Keep an emerald or green tourmaline on your desk','Donate green vegetables or books on Wednesdays'],
  6:['Wear white or pale pink on Fridays to strengthen Venus energy','Spend Fridays in creative work, art, music, cooking','Keep a diamond or white sapphire on your person','Offer white flowers in your home on Fridays'],
  7:['Meditate 20 minutes daily, Ketu rewards inner stillness','Wear violet or grey on Mondays','Visit a body of water weekly for grounding','Keep a cat\'s eye after consulting a gemologist'],
  8:['Build daily routines, Saturn rewards discipline above all','Wear black or dark blue on Saturdays','Donate iron or black sesame on Saturdays','Avoid new launches on dates summing to 8'],
  9:['Exercise on Tuesdays, Mars responds to physical action','Wear red or coral on Tuesdays','Keep red coral set in copper, worn on right ring finger','Offer red flowers on Tuesdays'],
};

const MISSING_MEANINGS={
  1:'Self-confidence, leadership',2:'Sensitivity, intuition',3:'Creativity, communication',
  4:'Discipline, organisation',5:'Freedom, adaptability',6:'Responsibility, harmony',
  7:'Spirituality, introspection',8:'Ambition, material success',9:'Compassion, completion'
};

// ── ALIGNMENT SCORING (weighted, transparent, explainable) ──
// Replaces the previous binary "100% if friendly else 40%" logic
// that produced theoretically inconsistent rollups (e.g. two 100%
// dimensions averaging to a 38% overall). The new model scores
// six dimensions independently, weights them, and returns a single
// integer percentage. All sub-scores are exposed via
// compatPctBreakdown() so the renderer can show *why* the number
// is what it is — a key trust requirement.
//
// Weights (sum to 100):
//   Compound Quality     30   — symbolic weight of the unreduced
//                                name compound (e.g. 26, 41)
//   Name × Birth Number       20   — root-number friendship with birth
//   Name × Life Path Number      20   — root-number friendship with destiny
//   Planetary Harmony    12   — three-way triangle of name/birth/
//                                destiny rulers
//   Phonetic Stability    8   — heaviness of the compound (very
//                                high compounds carry more karmic
//                                load and are harder to "wear")
//   Amplification        10   — resonance/repetition between the
//                                three numbers (e.g. 2-2-2 trio)
//
// Per product direction: floor at 35 (avoid dramatic catastrophic
// scores; numerology is meant to be informative, not fear-based)
// and ceiling at 99 (perfect 100 reserved for nameNum===moolank).

function _scoreCompoundQuality(compound){
  const e = CD[compound];
  if (!e) return 75;                 // unmapped compound (>52 etc.) — treat neutrally
  if (e.q === 'g') return 92;
  if (e.q === 'n') return 75;
  return 58;                         // 'b' — challenging but never < ~half
}
function _scoreRootHarmony(a, b){
  if (a === b) return 100;
  if ((FRIENDLY[b]||[]).includes(a)) return 85;
  return 62;                         // not friendly — but no dramatic drop
}
function _scorePlanetaryHarmony(nameNum, moolank, destNum){
  const pairs = [[nameNum,moolank],[nameNum,destNum],[moolank,destNum]];
  let score = 0;
  pairs.forEach(([x,y]) => {
    if (x === y) score += 1;
    else if ((FRIENDLY[y]||[]).includes(x)) score += 1;
  });
  return [55, 68, 82, 95][score];    // 0/1/2/3 friendly pairs
}
function _scorePhoneticStability(compound){
  if (compound <= 22) return 90;
  if (compound <= 33) return 80;
  if (compound <= 44) return 72;
  return 64;                          // very heavy compound — harder to carry
}
function _scoreAmplification(nameNum, moolank, destNum){
  const distinct = new Set([nameNum, moolank, destNum]).size;
  if (distinct === 1) return 95;     // perfect resonance (rare, very strong)
  if (distinct === 2) return 82;     // two-way amplification
  return _scorePlanetaryHarmony(nameNum, moolank, destNum);
}

const _WEIGHTS = { cq:30, nm:20, nb:20, ph:12, ps:8, amp:10 };

function compatPctBreakdown(nameNum, nameRaw, birthNum, destNum){
  const cq  = _scoreCompoundQuality(nameRaw);
  const nm  = _scoreRootHarmony(nameNum, birthNum);
  const nb  = _scoreRootHarmony(nameNum, destNum);
  const ph  = _scorePlanetaryHarmony(nameNum, birthNum, destNum);
  const ps  = _scorePhoneticStability(nameRaw);
  const amp = _scoreAmplification(nameNum, birthNum, destNum);
  const w = _WEIGHTS;
  // Phase 4a recalibration: floor raised to 45 (so "below 45%" is
  // genuinely rare and reserved for transformational profiles, per
  // product direction). Ceiling stays at 99 — the candidate
  // generator overrides to 100 only when nameNum===moolank, which
  // is the report's "fully resonant" convention.
  const overall = Math.round(Math.max(45, Math.min(99,
    (cq*w.cq + nm*w.nm + nb*w.nb + ph*w.ph + ps*w.ps + amp*w.amp) / 100
  )));
  const compoundEntry = CD[nameRaw];
  return {
    overall,
    components: [
      { key:'cq',  label:'Compound Quality',
        sub: compoundEntry ? `${nameRaw} · ${compoundEntry.l}` : `${nameRaw} · Neutral resonance`,
        score:cq,  weight:w.cq },
      { key:'nm',  label:`Name (${nameNum}) × Birth Number (${birthNum})`,
        sub: _harmonyLabel(nameNum, birthNum),
        score:nm,  weight:w.nm },
      { key:'nb',  label:`Name (${nameNum}) × Life Path Number (${destNum})`,
        sub: _harmonyLabel(nameNum, destNum),
        score:nb,  weight:w.nb },
      { key:'ph',  label:'Planetary Harmony',
        sub: 'Three-way balance across name, birth & destiny rulers',
        score:ph,  weight:w.ph },
      { key:'ps',  label:'Phonetic Stability',
        sub: nameRaw <= 22 ? 'Light, easy-to-carry compound'
           : nameRaw <= 33 ? 'Moderate compound, settled'
           : nameRaw <= 44 ? 'Heavier compound, asks for steadiness'
           : 'Very heavy compound, asks for conscious handling',
        score:ps,  weight:w.ps },
      { key:'amp', label:'Amplification',
        sub: (new Set([nameNum,birthNum,destNum]).size === 1)
           ? 'All three numbers resonate — strong amplification'
           : (new Set([nameNum,birthNum,destNum]).size === 2)
           ? 'Two numbers resonate — partial amplification'
           : 'Three distinct vibrations — depends on harmony',
        score:amp, weight:w.amp },
    ],
  };
}

// Back-compat: callers that only need the overall number still work.
function compatPct(nameNum, nameRaw, birthNum, destNum){
  return compatPctBreakdown(nameNum, nameRaw, birthNum, destNum).overall;
}

function _harmonyLabel(a, b){
  if (a === b) return 'Identical resonance — strongest possible match';
  if ((FRIENDLY[b]||[]).includes(a)) return 'Friendly planetary interaction';
  return 'Neutral interaction — no strong friction or support';
}

// Legacy 3-tier status (kept for backwards compat with any caller
// that still expects 'aligned'/'neutral'/'misaligned'). Prefer
// getAlignmentTier() below for new code.
function getAlignmentStatus(pct){
  return pct>=75?'aligned':pct>=55?'neutral':'misaligned';
}

// ── ALIGNMENT TIER SYSTEM (phase 4a) ──────────────────────────
// Seven psychological tiers with strengths-led, non-fear-based
// language. Each tier returns:
//   key:          machine-friendly id (used for CSS classes)
//   title:        2-3 word headline
//   icon:         single-glyph signature
//   tone:         supportive / balanced / observant — colour key
//   short:        one-line summary used in summary-box / share copy
//   description:  2-4 sentence framing per the spec
function getAlignmentTier(pct){
  if (pct >= 90) return {
    key:'tier-rare', tone:'supportive', icon:'✦',
    title:'Rare Natural Resonance',
    short:'Your name and birth vibrations work together with unusual ease.',
    description:'Your name and birth vibrations work together with unusual ease and reinforcement. Strengths tend to express naturally and consistently, though growth still comes through conscious self-awareness rather than comfort alone.'
  };
  if (pct >= 85) return {
    key:'tier-strong', tone:'supportive', icon:'★',
    title:'Strong Natural Alignment',
    short:'Your name actively supports your emotional patterns and life direction.',
    description:'Your name actively supports your emotional patterns, communication style and life direction. While no profile is without friction, your energetic structure generally creates momentum rather than resistance.'
  };
  if (pct >= 75) return {
    key:'tier-supportive', tone:'supportive', icon:'◈',
    title:'Supportive but Improvable',
    short:'Strong supportive patterns alongside a few areas of recurring tension.',
    description:'Your profile contains strong supportive patterns alongside a few recurring areas of tension or overcompensation. Life tends to work best when emotional awareness and conscious decision-making stay balanced.'
  };
  if (pct >= 65) return {
    key:'tier-mixed', tone:'balanced', icon:'◇',
    title:'Mixed but Workable Energies',
    short:'A blend of harmony and friction — some areas natural, others uneven.',
    description:'Your numbers contain both harmony and friction. Certain parts of your personality work very naturally, while others may feel inconsistent, emotionally tiring or difficult to sustain long-term without conscious adjustment.'
  };
  if (pct >= 55) return {
    key:'tier-friction', tone:'balanced', icon:'◉',
    title:'Noticeable Internal Friction',
    short:'Recurring tension between instincts, identity and direction — visible but workable.',
    description:'Your profile suggests recurring tension between emotional instincts, external identity or life direction. This does not block success, but it can create cycles of self-doubt, delayed clarity or emotionally draining patterns if left unconscious.'
  };
  if (pct >= 45) return {
    key:'tier-recalibration', tone:'observant', icon:'◐',
    title:'Friction-Heavy Patterns',
    short:'Stronger-than-average internal contradiction — growth comes through recalibration.',
    description:'Your numbers suggest stronger-than-average internal contradiction or emotional resistance patterns. Growth often comes through recalibration, stronger boundaries, emotional discernment and learning not to repeat exhausting cycles.'
  };
  return {
    key:'tier-transformational', tone:'observant', icon:'◓',
    title:'Intense Transformational Alignment',
    short:'A reinvention-led profile — growth comes through deep self-understanding.',
    description:'This range should remain uncommon. It does not mean your life is "bad" or that success is blocked. Instead, it usually reflects a personality structure carrying stronger internal contradictions, emotional intensity or transformational lessons than average. People in this range often go through deeper reinvention phases, learn important lessons through experience, and develop unusual self-awareness over time. Their growth tends to come less from comfort and more from understanding themselves at a deeper level.'
  };
}

// Nav toggle (shared)
function initNav(){
  const ham=document.getElementById('navHamburger');
  const mob=document.getElementById('navMobile');
  if(ham&&mob) ham.addEventListener('click',()=>mob.classList.toggle('open'));
}
document.addEventListener('DOMContentLoaded',initNav);

// FAQ toggle (shared)
function initFaq(){
  document.querySelectorAll('.faq-item').forEach(item=>{
    item.querySelector('.faq-q')?.addEventListener('click',()=>{
      item.classList.toggle('open');
    });
  });
}
document.addEventListener('DOMContentLoaded',initFaq);

// ── NATURALNESS SCORER (phase 2) ─────────────────────────────
// Rates how natural a generated name spelling looks/sounds. Used
// to reject awkward outputs like "Aaravhl", "Mohanhk", "Jiyaaaa"
// that the previous algorithm produced because it optimised only
// for Chaldean alignment without considering whether the result
// is a name a human could actually use.
//
// Returns 20-100. Below ~55 = reject outright. Combined with
// alignment score (65/35 weighting) for final ranking.
function naturalnessScore(name){
  var lc = (name||'').toLowerCase();
  var score = 100;

  // 3+ same letter in a row (aaa, hhh, lll) — almost always awkward
  if (/(.)\1{2,}/.test(lc)) score -= 45;

  // 4+ vowels run (aaaa, eaie) — unreadable
  if (/[aeiou]{4,}/i.test(lc)) score -= 35;
  else if (/[aeiou]{3,}/i.test(lc)) score -= 12;

  // Final consonant cluster check. English / Indian names usually
  // end in a vowel, single consonant, or one of these clusters.
  var endingClusters = ['th','sh','ch','ck','ll','nn','ng','st','rd','rk','rt','rl','sk','rn','lt','mp','nd','rs','rm','lk','lm','ls','rp','ss','ff','mm','tt','ph','pt'];
  var clusterMatch = lc.match(/[bcdfghjklmnpqrstvwxyz]{2,}$/);
  if (clusterMatch){
    var c = clusterMatch[0];
    var last2 = c.slice(-2);
    if (c.length >= 3) score -= 30;                              // 3-letter ending cluster (vhl, nhk)
    if (endingClusters.indexOf(last2) === -1) score -= 20;       // unusual 2-letter ending (hl, hk, hr, hs)
  }

  // Awkward H placements: lh, mh, nh, rh — uncommon in Indian/English names
  // (kh, sh, ch, th, ph are fine; bh, dh, gh are also OK in Indian names).
  if (/[lmnr]h/.test(lc)) score -= 12;

  // Doubled hard consonants at start (bb-, dd-, gg-, rr-) read awkward
  if (/^(bb|dd|gg|kk|pp|tt|ff|rr|nn|mm|ll|ss|cc|jj|vv|ww|xx|zz)/.test(lc)) score -= 35;
  // Any doubled letter at the very start is rarely adoptable
  if (/^(.)\1/.test(lc)) score -= 20;

  // Doubled H mid-name ("hh") is almost always awkward
  if (/hh/.test(lc)) score -= 18;

  // Doubled v/k/x mid-name reads awkward
  if (/(vv|xx|kk|qq)/.test(lc)) score -= 12;

  // Mid-name H sandwiched between two consonants (ahkr, ehlt) — awkward
  if (/[bcdfgjklmnpqrstvwxyz]h[bcdfgjklmnpqrstvwxyz]/.test(lc)) score -= 10;

  // Soft, vowel-final endings get a small bonus (most natural)
  if (/[aeiouy]$/.test(lc)) score += 4;
  if (/(ya|ia|ja|ah|ai|ee|aa)$/.test(lc)) score += 2;

  // Hard consonant bolted onto a vowel ending (Purnimak, Jiyaal) —
  // changes pronunciation; users rarely adopt these.
  if (/[aeiou][klrs]$/.test(lc)) score -= 30;

  // Bonus: one doubled letter already in the spelling (Purrnima, Purnimaa)
  // reads as the same name with a soft elongation.
  if (/(.)\1/.test(lc) && !/(.)\1{2,}/.test(lc)) score += 8;

  return Math.max(20, Math.min(100, score));
}

// ── ALIGNED NAME CORRECTION ENGINE ───────────────────────────
// Tweaks FIRST NAME ONLY with phonetic additions (same sound) to
// improve Chaldean alignment. Brute-forces candidate strings via
// 1-, 2-, and 3-op composition over a phonetic pool, scores each
// candidate using compatPct (same scoring used elsewhere in the
// report), then returns exactly 3 candidates each scoring ≥ 70%.
// Higher-scoring candidates rank first; among equal scores the
// shorter (more natural) name wins.
//
// Note: compatPct caps at 98%, so we override to 100% when the
// candidate's reduced name-number equals moolank (perfect resonance
// — that's the report's existing convention for "fully aligned").
//
// Returns: {corrections:[...], delta, target, currentSum, alreadyAligned?}
// where each correction has alignmentPct ∈ [70, 100].
function generateAlignedCorrectedNames(fullName, moolank, destNum){
  var parts=fullName.trim().split(/\s+/);
  var firstName=parts[0], restStr=parts.slice(1).join(' ');
  var firstSum=chalSum(firstName), restSum=chalSum(restStr);
  var total=firstSum+restSum;
  if(destNum==null) destNum=moolank;

  // Smallest targetSum >= total where reduce → moolank (used only
  // for the legacy delta/target fields that the rendering layer
  // reads to phrase the "phonetic correction requires adding N"
  // fallback).
  var target=null;
  for(var t=total;t<=total+60;t++){ if(reduce(t)===moolank){target=t;break;} }
  if(target===null) target=total;

  // If the user's current name already scores very high on the
  // weighted alignment model, skip the optimisation section
  // entirely — there's nothing meaningful to improve. We use the
  // new compatPctBreakdown so the threshold is internally
  // consistent with the breakdown the user sees on the page.
  var currentNameNum = reduce(total);
  var currentScore = compatPctBreakdown(currentNameNum, total, moolank, destNum).overall;
  if (currentScore >= 95) {
    return {corrections:[],delta:0,target:total,currentSum:total,alreadyAligned:true};
  }

  // Phonetic operation pool, ordered by naturalness for Indian
  // names. Each op takes a lowercase string and returns a candidate
  // string (or null if the op cannot apply to this stem).
  // Prefer same-sound tweaks (double a letter already present, soft
  // vowel endings). Hard consonant appends (k/l/r/s) are last-resort
  // only — they change pronunciation and users rarely adopt them.
  var OPS=[
    function(n){ return n+'a'; },                                                    // 0  append A
    function(n){ return /[aeiou]$/i.test(n) ? n+n.slice(-1) : null; },               // 1  double final vowel
    function(n){ return n+'h'; },                                                    // 2  append H
    function(n){ return n+'i'; },                                                    // 3  append I
    function(n){ return n+'y'; },                                                    // 4  append Y
    function(n){ return n+'ya'; },                                                   // 5  soft ...ya (Purnimaya)
    function(n){ return n+'ia'; },                                                   // 6  soft ...ia
    function(n){                                                                     // 7  H after first vowel
      var m=n.match(/[aeiou]/i);
      return m ? n.slice(0,m.index+1)+'h'+n.slice(m.index+1) : null;
    },
    function(n){                                                                     // 8  Y before final vowel
      var m=n.match(/([^aeiou])([aeiou]+)$/i);
      return m ? n.slice(0,m.index+1)+'y'+n.slice(m.index+1) : null;
    },
    function(n){                                                                     // 9  I before final vowel
      var m=n.match(/([^aeiou])([aeiou]+)$/i);
      return m ? n.slice(0,m.index+1)+'i'+n.slice(m.index+1) : null;
    },
    function(n){ return /[aeiou]$/i.test(n) ? n.slice(0,-1)+'ah' : n+'ah'; },        // 10 ...AH ending
    function(n){ return n+'aa'; },                                                   // 11 append AA
    function(n){ return n+'n'; },                                                    // 12 append N (nasal, often soft)
    function(n){                                                                     // 13 double final consonant
      var m=n.match(/([^aeiou])$/i);
      return m ? n+m[1] : null;
    },
    function(n){                                                                     // 14 prepend A (vowel-safe)
      return /^[aeiou]/i.test(n) ? null : 'a'+n;
    },
    function(n){ return n+'ee'; },                                                   // 15 append EE
  ];
  // Last-resort ops: change the spoken ending. Only used if the soft
  // pool cannot fill 3 adoptible options.
  var HARD_OPS=[
    function(n){ return n+'k'; },
    function(n){ return n+'l'; },
    function(n){ return n+'r'; },
    function(n){ return n+'s'; },
    function(n){ return n+'aaa'; },
    function(n){ return n+'aha'; },
  ];

  var lower=firstName.toLowerCase();
  var seen=new Set([lower]);
  var pool=[];

  // True when variant is the base with exactly one existing letter
  // doubled (Purnima → Purrnima / Purnimaa). Highest adoptability.
  function isSameSoundDouble(base, variant){
    if(!variant || variant.length !== base.length + 1) return false;
    for(var i=0;i<variant.length;i++){
      if(variant.slice(0,i)+variant.slice(i+1) === base){
        var ch = variant[i];
        return (i>0 && variant[i-1]===ch) || (i<variant.length-1 && variant[i+1]===ch);
      }
    }
    return false;
  }

  function consider(variant){
    if(!variant) return;
    var lc=variant.toLowerCase();
    if(seen.has(lc)) return;
    // Keep changes small — users adopt +1–2 letters, not long stacks
    if(lc.length > lower.length + 2) return;
    // Block stacked soft endings (Priyayaya, Nehaiaia)
    if(/(ya){2,}|(ia){2,}|yaya|iaia|aayaa/.test(lc)) return;
    var capped=lc.charAt(0).toUpperCase()+lc.slice(1);
    var nf=chalSum(capped);
    var nt=nf+restSum;
    var reduced=reduce(nt);
    // Convention: name-number === moolank means full resonance (100%).
    // Otherwise use the same compatPct scorer used for the user's
    // current name so the numbers are directly comparable.
    var pct = (reduced===moolank) ? 100 : compatPct(reduced, nt, moolank, destNum);
    if(pct < 70) return;
    // Naturalness gate (phase 2). Reject candidates that look or
    // sound awkward (Aaravhl, Mohanhk, Jiyaaaa-class). Still keep
    // some headroom so we always have a pool to pick from.
    var nat = naturalnessScore(capped);
    if(isSameSoundDouble(lower, lc)) nat = Math.min(100, nat + 12);
    if(nat < 55) return;
    seen.add(lc);
    pool.push({
      firstName: capped,
      fullName: restStr ? capped+' '+restStr : capped,
      newFirstSum: nf,
      restSum: restSum,
      newTotal: nt,
      nameNum: reduced,
      alignmentPct: pct,
      naturalness: nat,
      sameSound: isSameSoundDouble(lower, lc),
      // Combined ranking: alignment matters most (paid promise) but
      // a beautiful name beats a slightly higher-aligned ugly one.
      // Same-sound doubles get a further nudge so Purrnima beats Purnimak.
      combinedScore: Math.round(pct*0.55 + nat*0.45) + (isSameSoundDouble(lower, lc) ? 8 : 0)
    });
  }

  // Pass 0 — same-sound letter doublings (highest priority for users).
  // Purnima → Purrnima, Purnimaa, Purnnima, Puurnima, etc.
  for(var di=0; di<lower.length; di++){
    if(di>0 && lower[di-1]===lower[di]) continue;
    if(di<lower.length-1 && lower[di+1]===lower[di]) continue;
    consider(lower.slice(0,di+1)+lower[di]+lower.slice(di+1));
  }

  // Pass 1, single soft op (most natural)
  for(var i=0;i<OPS.length;i++){ consider(OPS[i](lower)); }
  // Pass 2, two-op composition
  for(var i2=0;i2<OPS.length;i2++){
    var v1=OPS[i2](lower); if(!v1) continue;
    for(var j2=0;j2<OPS.length;j2++){ consider(OPS[j2](v1)); }
  }
  // Pass 3, three-op composition (only if we still need more variety)
  if(pool.length < 24){
    for(var i3=0;i3<OPS.length && pool.length<48;i3++){
      var w1=OPS[i3](lower); if(!w1) continue;
      for(var j3=0;j3<OPS.length && pool.length<48;j3++){
        var w2=OPS[j3](w1); if(!w2) continue;
        for(var k3=0;k3<OPS.length && pool.length<48;k3++){
          consider(OPS[k3](w2));
        }
      }
    }
  }

  // Rank: alignment first (paid promise), then same-sound doubles,
  // then combinedScore, then shorter name.
  pool.sort(function(a,b){
    if(b.alignmentPct !== a.alignmentPct) return b.alignmentPct - a.alignmentPct;
    if(!!b.sameSound !== !!a.sameSound) return b.sameSound ? 1 : -1;
    if(b.combinedScore !== a.combinedScore) return b.combinedScore - a.combinedScore;
    return a.firstName.length - b.firstName.length;
  });

  // Prefer a diverse top-3: if we already picked a same-sound double at
  // 100%, still surface soft endings (…ya / …aa) as option 2/3 rather
  // than three near-identical doubles that miss perfect alignment.
  function pickTop3(list){
    var out = [], seenRoots = new Set();
    // Pass A: perfect alignment first
    for(var i=0;i<list.length && out.length<3;i++){
      if(list[i].alignmentPct < 100) continue;
      var root = list[i].firstName.toLowerCase().replace(/(.)\1+/g,'$1');
      if(out.length>0 && seenRoots.has(root) && list[i].sameSound) continue;
      seenRoots.add(root);
      out.push(list[i]);
    }
    // Pass B: fill remaining with best remaining
    for(var j=0;j<list.length && out.length<3;j++){
      if(out.indexOf(list[j])>=0) continue;
      out.push(list[j]);
    }
    return out;
  }

  // If the soft pool left fewer than 3 candidates, fall back to hard
  // consonant / stretch ops so we still meet the "always 3 options"
  // contract. These change pronunciation and rank last.
  if (pool.length < 3) {
    var hardPool = OPS.concat(HARD_OPS);
    for (var ri = 0; ri < hardPool.length && pool.length < 6; ri++){
      var v = hardPool[ri](lower); if (!v) continue;
      var lc2 = v.toLowerCase();
      if (seen.has(lc2)) continue;
      var cap2 = lc2.charAt(0).toUpperCase() + lc2.slice(1);
      var nf2 = chalSum(cap2);
      var nt2 = nf2 + restSum;
      var rd2 = reduce(nt2);
      var pc2 = (rd2 === moolank) ? 100 : compatPct(rd2, nt2, moolank, destNum);
      if (pc2 < 70) continue;
      seen.add(lc2);
      pool.push({
        firstName: cap2,
        fullName: restStr ? cap2+' '+restStr : cap2,
        newFirstSum: nf2,
        restSum: restSum,
        newTotal: nt2,
        nameNum: rd2,
        alignmentPct: pc2,
        naturalness: naturalnessScore(cap2),
        sameSound: false,
        combinedScore: Math.round(pc2*0.55 + naturalnessScore(cap2)*0.45)
      });
    }
    pool.sort(function(a,b){
      if(b.alignmentPct !== a.alignmentPct) return b.alignmentPct - a.alignmentPct;
      if(!!b.sameSound !== !!a.sameSound) return b.sameSound ? 1 : -1;
      if(b.combinedScore !== a.combinedScore) return b.combinedScore - a.combinedScore;
      return a.firstName.length - b.firstName.length;
    });
  }

  var top3 = pickTop3(pool);
  return {corrections: top3, delta: target-total, target: target, currentSum: total};
}
