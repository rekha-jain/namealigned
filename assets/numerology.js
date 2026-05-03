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
// make reduce(chalSum(fullName)) === moolank  → 100% alignment.
// Rule: never add new words / initials, only add letters within
// the first name (extra vowel, soft consonant, doubled letter).
function generateAlignedCorrectedNames(fullName, moolank){
  var parts=fullName.trim().split(/\s+/);
  var firstName=parts[0], restStr=parts.slice(1).join(' ');
  var firstSum=chalSum(firstName), restSum=chalSum(restStr);
  var total=firstSum+restSum;

  // Smallest targetSum >= total where reduce(targetSum)===moolank
  var target=null;
  for(var t=total;t<=total+100;t++){ if(reduce(t)===moolank){target=t;break;} }
  if(!target) return {corrections:[],delta:0,target:total,currentSum:total};
  var delta=target-total;
  if(delta===0) return {corrections:[],delta:0,target:total,currentSum:total,alreadyAligned:true};

  // Phonetic addition pool, apply(name_lowercase) → string|null
  var ADDS=[
    {v:1,apply:function(n){return n+'a';}},                                    // A at end
    {v:1,apply:function(n){                                                    // I at first vowel-consonant boundary
      var m=n.match(/([aeiou])([^aeiou])/i);
      return m?n.slice(0,m.index+1)+'i'+n.slice(m.index+1):null;
    }},
    {v:1,apply:function(n){                                                    // Y before final vowel
      var m=n.match(/([^aeiou])([aeiou]+)$/i);
      return m?n.slice(0,m.index+1)+'y'+n.slice(m.index+1):n+'y';
    }},
    {v:2,apply:function(n){                                                    // double ending vowel
      return /[aeiou]$/i.test(n)?n+n.slice(-1):n+'aa';
    }},
    {v:2,apply:function(n){var ki=n.lastIndexOf('k');                          // double last K
      return ki>=0?n.slice(0,ki+1)+'k'+n.slice(ki+1):null;}},
    {v:2,apply:function(n){var ri=n.lastIndexOf('r');                          // double last R
      return ri>=0?n.slice(0,ri+1)+'r'+n.slice(ri+1):null;}},
    {v:3,apply:function(n){var si=n.lastIndexOf('s');                          // double last S
      return si>=0?n.slice(0,si+1)+'s'+n.slice(si+1):null;}},
    {v:3,apply:function(n){var li=n.lastIndexOf('l');                          // double last L
      return li>=0?n.slice(0,li+1)+'l'+n.slice(li+1):null;}},
    {v:4,apply:function(n){var mi=n.lastIndexOf('m');                          // double last M
      return mi>=0?n.slice(0,mi+1)+'m'+n.slice(mi+1):null;}},
    {v:4,apply:function(n){var ti=n.lastIndexOf('t');                          // double last T
      return ti>=0?n.slice(0,ti+1)+'t'+n.slice(ti+1):null;}},
    {v:5,apply:function(n){                                                    // H after first vowel
      var m=n.match(/[aeiou]/i);
      return m?n.slice(0,m.index+1)+'h'+n.slice(m.index+1):null;
    }},
    {v:5,apply:function(n){var hi=n.indexOf('h');                              // double first H
      return hi>=0?n.slice(0,hi)+'h'+n.slice(hi):null;}},
    {v:5,apply:function(n){var ni=n.lastIndexOf('n');                          // double last N
      return ni>=0?n.slice(0,ni+1)+'n'+n.slice(ni+1):null;}},
    {v:6,apply:function(n){                                                    // AH ending
      return /[aeiou]$/i.test(n)?n.slice(0,-1)+'ah':n+'ah';
    }},
    {v:7,apply:function(n){                                                    // H-inner + double-end-vowel (5+2=7 combined)
      var m=n.match(/[aeiou]/i);
      var h=m?n.slice(0,m.index+1)+'h'+n.slice(m.index+1):'h'+n;
      return /[aeiou]$/i.test(h)?h+h.slice(-1)+'a':h+'aa';
    }},
    {v:8,apply:function(n){                                                    // H-inner + triple A
      var m=n.match(/[aeiou]/i);
      var h=m?n.slice(0,m.index+1)+'h'+n.slice(m.index+1):'h'+n;
      return h+'aaa';
    }},
  ];

  function cap(s){return s.charAt(0).toUpperCase()+s.slice(1);}
  var results=[],seen=new Set([firstName.toLowerCase()]);

  // Try single additions matching delta exactly
  ADDS.forEach(function(a){
    if(a.v!==delta||results.length>=3) return;
    var r=a.apply(firstName.toLowerCase());
    if(!r||seen.has(r.toLowerCase())) return;
    var capped=cap(r),nt=chalSum(capped)+restSum;
    if(reduce(nt)!==moolank) return;
    seen.add(r.toLowerCase());
    results.push({firstName:capped,fullName:restStr?capped+' '+restStr:capped,
      newFirstSum:chalSum(capped),restSum:restSum,newTotal:nt,nameNum:moolank});
  });

  // Try pairs of additions summing to delta
  for(var i=0;i<ADDS.length&&results.length<3;i++){
    for(var j=0;j<ADDS.length&&results.length<3;j++){
      if(ADDS[i].v+ADDS[j].v!==delta) continue;
      var s1=ADDS[i].apply(firstName.toLowerCase());
      if(!s1) continue;
      var s2=ADDS[j].apply(s1);
      if(!s2||seen.has(s2.toLowerCase())) continue;
      var capped2=cap(s2),nt2=chalSum(capped2)+restSum;
      if(reduce(nt2)!==moolank) continue;
      seen.add(s2.toLowerCase());
      results.push({firstName:capped2,fullName:restStr?capped2+' '+restStr:capped2,
        newFirstSum:chalSum(capped2),restSum:restSum,newTotal:nt2,nameNum:moolank});
    }
  }

  return {corrections:results,delta:delta,target:target,currentSum:total};
}
