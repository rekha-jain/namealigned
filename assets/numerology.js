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
function getLoshuNums(dob){const p=new Set();for(let c of dob.replace(/-/g,''))if(c!=='0')p.add(+c);return p;}

const FRIENDLY={1:[1,2,3,4,9],2:[1,2,4,7,8],3:[1,3,6,9],4:[1,2,4,6,8],5:[1,3,5,6,9],6:[3,4,5,6,9],7:[1,2,7],8:[2,4,6,8],9:[1,3,5,6,9]};
const PREFERRED=[1,3,5,6,9];
const CAUTION_NAME_NUMS=[4,8];

const CD={
  10:{q:'g',l:'Wheel of Fortune · Rise & Fall'},11:{q:'b',l:'Hidden Dangers · Treachery'},
  12:{q:'b',l:'The Victim · Sacrifice'},13:{q:'b',l:'Change & Revolution'},
  14:{q:'g',l:'Magnetic Movement · Travel'},15:{q:'g',l:'The Occultist · Magic Power'},
  16:{q:'b',l:'Tower Struck by Lightning ⚡'},17:{q:'g',l:'Star of the Magi · Peace & Love ★'},
  18:{q:'b',l:'Materialism Battles Spirit'},19:{q:'g',l:'The Sun · Most Fortunate Number ★'},
  20:{q:'n',l:'The Awakening · Judgment'},21:{q:'g',l:'Crown of the Magi · Brilliant Success ★'},
  22:{q:'b',l:'Submission · Fool\'s Gold'},23:{q:'g',l:'Royal Star of the Lion · Great Fortune ★'},
  24:{q:'g',l:'Love · Money · Creative Power'},25:{q:'n',l:'Strength Gained Through Strife'},
  26:{q:'b',l:'Partnerships Bring Loss · Ruin'},27:{q:'g',l:'The Sceptre · Authority & Command'},
  28:{q:'b',l:'Promising Start · Hidden Dangers'},29:{q:'b',l:'Vacillation · Uncertainty · Doubt'},
  30:{q:'n',l:'Thoughtful Reflection · Decisions'},31:{q:'b',l:'Solitude · Isolation from Others'},
  32:{q:'g',l:'Magic Power · Unexpected Help ★'},33:{q:'g',l:'Spiritual Wisdom & Guidance'},
  34:{q:'g',l:'Spiritual Power · Inner Strength'},35:{q:'b',l:'Idealism vs Materialism · Loss'},
  36:{q:'g',l:'Noble Character · True Leadership'},37:{q:'g',l:'Love Life & Friendship · Success'},
  38:{q:'b',l:'Partnerships Cause Problems'},39:{q:'n',l:'Artistic Vision & Inspiration'},
  40:{q:'n',l:'Spiritual Completion · Order'},41:{q:'g',l:'Industrious Success · Ambition'},
  42:{q:'g',l:'Creative Partnerships · Growth'},43:{q:'b',l:'Revolution · Conflict · Upheaval'},
  44:{q:'b',l:'Excess & Downfall · Overreach'},45:{q:'g',l:'Idealism & Noble Service'},
  46:{q:'g',l:'Leadership & Authority Success'},47:{q:'g',l:'Spiritual Protection · Blessings'},
  48:{q:'b',l:'Strong Opposition · Conflict'},49:{q:'n',l:'Humanitarian Vision · Wisdom'},
  50:{q:'g',l:'New Cycle · Fresh Beginnings'},51:{q:'g',l:'Power to Lead · The Sword'},
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

function compatPct(nameNum,nameRaw,birthNum,destNum){
  const bf=FRIENDLY[birthNum]||[],df=FRIENDLY[destNum]||[];
  const bothFriendly=bf.includes(nameNum)&&df.includes(nameNum);
  const oneFriendly=bf.includes(nameNum)||df.includes(nameNum);
  const compound=CD[nameRaw];
  let score=15;
  if(bothFriendly)score+=35;else if(oneFriendly)score+=15;
  if(PREFERRED.includes(nameNum))score+=22;
  if(compound?.q==='g')score+=25;else if(compound?.q==='b')score-=12;
  return Math.max(5,Math.min(98,score));
}

function getAlignmentStatus(pct){
  return pct>=75?'aligned':pct>=50?'neutral':'misaligned';
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
  if(reduce(total)===moolank) return {corrections:[],delta:0,target:total,currentSum:total,alreadyAligned:true};

  // Phonetic operation pool, ordered by naturalness for Indian
  // names. Each op takes a lowercase string and returns a candidate
  // string (or null if the op cannot apply to this stem).
  var OPS=[
    function(n){ return n+'a'; },                                                    // 0  append A
    function(n){ return /[aeiou]$/i.test(n) ? n+n.slice(-1) : null; },               // 1  double final vowel
    function(n){ return n+'h'; },                                                    // 2  append H
    function(n){ return n+'i'; },                                                    // 3  append I
    function(n){ return n+'y'; },                                                    // 4  append Y
    function(n){                                                                     // 5  H after first vowel
      var m=n.match(/[aeiou]/i);
      return m ? n.slice(0,m.index+1)+'h'+n.slice(m.index+1) : null;
    },
    function(n){                                                                     // 6  Y before final vowel
      var m=n.match(/([^aeiou])([aeiou]+)$/i);
      return m ? n.slice(0,m.index+1)+'y'+n.slice(m.index+1) : null;
    },
    function(n){                                                                     // 7  I before final vowel
      var m=n.match(/([^aeiou])([aeiou]+)$/i);
      return m ? n.slice(0,m.index+1)+'i'+n.slice(m.index+1) : null;
    },
    function(n){ return /[aeiou]$/i.test(n) ? n.slice(0,-1)+'ah' : n+'ah'; },        // 8  ...AH ending
    function(n){ return n+'aa'; },                                                   // 9  append AA
    function(n){ return n+'k'; },                                                    // 10 append K
    function(n){ return n+'l'; },                                                    // 11 append L
    function(n){ return n+'r'; },                                                    // 12 append R
    function(n){ return n+'s'; },                                                    // 13 append S
    function(n){ return n+'n'; },                                                    // 14 append N
    function(n){                                                                     // 15 double final consonant
      var m=n.match(/([^aeiou])$/i);
      return m ? n+m[1] : null;
    },
    function(n){                                                                     // 16 prepend A (vowel-safe)
      return /^[aeiou]/i.test(n) ? null : 'a'+n;
    },
    function(n){ return n+'aaa'; },                                                  // 17 append AAA
    function(n){ return n+'aha'; },                                                  // 18 append AHA
    function(n){ return n+'ee'; },                                                   // 19 append EE
  ];

  var lower=firstName.toLowerCase();
  var seen=new Set([lower]);
  var pool=[];

  function consider(variant){
    if(!variant) return;
    var lc=variant.toLowerCase();
    if(seen.has(lc)) return;
    var capped=lc.charAt(0).toUpperCase()+lc.slice(1);
    var nf=chalSum(capped);
    var nt=nf+restSum;
    var reduced=reduce(nt);
    // Convention: name-number === moolank means full resonance (100%).
    // Otherwise use the same compatPct scorer used for the user's
    // current name so the numbers are directly comparable.
    var pct = (reduced===moolank) ? 100 : compatPct(reduced, nt, moolank, destNum);
    if(pct < 70) return;
    seen.add(lc);
    pool.push({
      firstName: capped,
      fullName: restStr ? capped+' '+restStr : capped,
      newFirstSum: nf,
      restSum: restSum,
      newTotal: nt,
      nameNum: reduced,
      alignmentPct: pct
    });
  }

  // Pass 1, single op (most natural)
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

  // Rank: higher score first; on ties, shorter name (more natural).
  pool.sort(function(a,b){
    if(b.alignmentPct !== a.alignmentPct) return b.alignmentPct - a.alignmentPct;
    return a.firstName.length - b.firstName.length;
  });

  var top3 = pool.slice(0, 3);
  return {corrections: top3, delta: target-total, target: target, currentSum: total};
}
