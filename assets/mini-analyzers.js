/* ═════════════════════════════════════════════════════════════════
   MINI-ANALYZERS — Partner / Child / Business
   Shared logic used by /analyzer (locked-card links) and the three
   standalone landing pages:
     /business-name-numerology
     /baby-name-numerology
     /love-compatibility-numerology

   Depends on: assets/numerology.js (CHALDEAN, FRIENDLY, PREFERRED,
   CD, CAUTION_NAME_NUMS, getBirthNum, getDestinyNum, getNameNum,
   getPlanet, reduce, compatPct).
   ════════════════════════════════════════════════════════════════ */

// trackEvent stub for landing pages where analyzer.html's logger isn't loaded.
// Use globalThis so a bare `trackEvent(...)` call inside this file resolves
// in both browser (globalThis === window) and any test/SSR environment.
if(typeof globalThis.trackEvent !== 'function'){
  globalThis.trackEvent = function(){ /* no-op */ };
}

// ── Archetype labels (Moolank → identity descriptor) ───────────────
const ARCHETYPES = {
  1:'The Trailblazer', 2:'The Empath',     3:'The Storyteller',
  4:'The Maverick',    5:'The Explorer',   6:'The Harmonizer',
  7:'The Seeker',      8:'The Architect',  9:'The Warrior'
};

// ── Tier helpers ───────────────────────────────────────────────────
function tierOf(pct){
  if(pct>=70) return {cls:'high',label:'STRONG HARMONY',icon:'✓'};
  if(pct>=45) return {cls:'mid', label:'WORKABLE',       icon:'~'};
  return       {cls:'low', label:'NEEDS AWARENESS', icon:'◇'};
}
function tierBrand(pct){
  if(pct>=70) return {cls:'high',label:'STRONG BRAND ALIGNMENT',icon:'✓'};
  if(pct>=45) return {cls:'mid', label:'WORKABLE VIBRATION',     icon:'~'};
  return       {cls:'low', label:'LOW BRAND ALIGNMENT',          icon:'◇'};
}
function tierChild(pct){
  if(pct>=70) return {cls:'high',label:'STRONGLY ALIGNED', icon:'✓'};
  if(pct>=45) return {cls:'mid', label:'WORKABLE',          icon:'~'};
  return       {cls:'low', label:'LOW ALIGNMENT',           icon:'◇'};
}

// ── Misc helpers ───────────────────────────────────────────────────
function firstWord(s){ return String(s||'').trim().split(/\s+/)[0]; }
function escapeAttr(s){ return String(s).replace(/"/g,'&quot;'); }

// ── Phonetic respellings — preserve pronunciation, shift vibration ──
function _phoneticTransforms(s){
  const out = new Set();
  const lo = s.toLowerCase();
  const isV = c => 'aeiou'.includes(c);
  const isC = c => 'bcdfghjklmnpqrstvwxz'.includes(c);
  const matchCase = (src, ch) => src===src.toUpperCase() ? ch.toUpperCase() : ch;

  for(let i=0;i<s.length;i++){
    if(!isV(lo[i])) continue;
    if(i>0 && lo[i-1]===lo[i]) continue;
    if(i<s.length-1 && lo[i+1]===lo[i]) continue;
    out.add(s.slice(0,i+1) + s[i] + s.slice(i+1));
  }
  for(let i=0;i<s.length;i++){
    if(lo[i]==='i') out.add(s.slice(0,i) + matchCase(s[i],'y') + s.slice(i+1));
    if(lo[i]==='y' && i>0) out.add(s.slice(0,i) + matchCase(s[i],'i') + s.slice(i+1));
  }
  for(let i=1;i<s.length-1;i++){
    if(isC(lo[i]) && isV(lo[i-1]) && isV(lo[i+1])){
      if(lo[i-1]===lo[i] || lo[i+1]===lo[i]) continue;
      if('hwxy'.includes(lo[i])) continue;
      out.add(s.slice(0,i+1) + s[i] + s.slice(i+1));
    }
  }
  if(s.length>=3 && isC(lo[lo.length-1])){
    out.add(s + 'e');
  }
  if(s.length>=2 && isV(lo[lo.length-1])){
    out.add(s + 'h');
  }
  const swaps = [['c','k'],['k','c'],['ph','f'],['f','ph'],['ck','k'],['z','s'],['s','z']];
  for(const [a,b] of swaps){
    let idx = -1;
    while((idx = lo.indexOf(a, idx+1)) !== -1){
      const head = s[idx]===s[idx].toUpperCase() ? b.toUpperCase() : b;
      const tail = b.length>1 ? b.slice(1) : '';
      out.add(s.slice(0,idx) + head + tail + s.slice(idx+a.length));
    }
  }
  if(s.length>=3){
    const last2 = lo.slice(-2);
    if(last2==='ie') out.add(s.slice(0,-2) + matchCase(s[s.length-2],'e') + s[s.length-1]);
    if(last2==='ee') out.add(s.slice(0,-2) + matchCase(s[s.length-2],'i') + matchCase(s[s.length-1],'e'));
    if(lo.slice(-1)==='y') out.add(s.slice(0,-1) + 'ee');
    if(lo.slice(-1)==='y') out.add(s.slice(0,-1) + 'ie');
  }
  return out;
}
function _isReadable(v){
  const lo = v.toLowerCase();
  if(/(.)\1\1/.test(lo)) return false;
  if(/[bcdfghjklmnpqrstvwxz]{4,}/.test(lo)) return false;
  if(/^(.)\1/.test(lo)) return false;
  if(/[aeiou]{3,}/.test(lo)) return false;
  return true;
}
function _applyToLongestWord(name, transformFn){
  const parts = name.split(/(\s+)/);
  let bestIdx = -1, bestLen = 0;
  for(let i=0;i<parts.length;i++){
    if(/^\s+$/.test(parts[i])) continue;
    if(parts[i].length > bestLen){ bestLen = parts[i].length; bestIdx = i; }
  }
  if(bestIdx === -1) return new Set();
  const wholeOut = new Set();
  for(const variant of transformFn(parts[bestIdx])){
    const copy = parts.slice();
    copy[bestIdx] = variant;
    wholeOut.add(copy.join(''));
  }
  for(const variant of transformFn(name)) wholeOut.add(variant);
  return wholeOut;
}
function suggestNameVariants(name, target, moo, bhag){
  const base = String(name||'').trim();
  if(!base) return [];
  const pass1 = _applyToLongestWord(base, _phoneticTransforms);
  const pass2 = new Set();
  let budget = 0;
  for(const v of pass1){
    if(budget++ > 60) break;
    for(const w of _applyToLongestWord(v, _phoneticTransforms)) pass2.add(w);
  }
  const all = new Set([...pass1, ...pass2]);
  all.delete(base);
  const scored = [];
  for(const v of all){
    if(!_isReadable(v)) continue;
    if(v.length < 2) continue;
    const {raw, reduced} = getNameNum(v);
    if(reduced !== target) continue;
    const compound = (typeof CD!=='undefined' && CD[raw]) ? CD[raw] : null;
    if(compound && compound.q==='b') continue;
    const baseScore = compatPct(reduced, raw, moo, bhag);
    const isPerfect = (reduced === moo) && (!compound || compound.q !== 'b');
    const displayScore = isPerfect ? 100 : baseScore;
    const lenPenalty = Math.max(0, Math.abs(v.length - base.length) - 2);
    scored.push({name:v, reduced, raw, score:displayScore, compound, lenPenalty, isPerfect});
  }
  scored.sort((a,b)=>
    (b.isPerfect?1:0) - (a.isPerfect?1:0)
    || b.score - a.score
    || a.lenPenalty - b.lenPenalty
    || a.name.length - b.name.length
  );
  const seen = new Set(), out = [];
  for(const x of scored){
    const key = x.name.toLowerCase();
    if(seen.has(key)) continue;
    seen.add(key);
    out.push(x);
    if(out.length===3) break;
  }
  return out;
}
function suggestBrandVariants(name, moo, bhag){
  return suggestNameVariants(name, moo, moo, bhag);
}

// ── Brand helpers ──────────────────────────────────────────────────
function bestBrandTargets(moo){
  const friends = FRIENDLY[moo] || [];
  const ranked = [];
  for(let n=1;n<=9;n++){
    if(CAUTION_NAME_NUMS.includes(n)) continue;
    let s = 0;
    if(PREFERRED.includes(n)) s += 10;
    if(friends.includes(n))   s += 12;
    if(n === moo)             s += 4;
    ranked.push({n, s});
  }
  ranked.sort((a,b)=>b.s-a.s);
  return ranked.slice(0,3).map(x=>x.n);
}

const BRAND_FOCUS = {
  1:{ headline:'Lead from the front', body:'Sun energy wins with founder-led brand voice, bold positioning and category leadership. Avoid hiding behind committees.' },
  2:{ headline:'Build on relationships', body:'Moon energy converts through trust and storytelling. Lean into customer testimonials, partnerships and emotional copy — not feature lists.' },
  3:{ headline:'Teach to sell', body:'Jupiter energy expands through advisory positioning, content and education. Thought-leadership > paid ads. Webinars, frameworks, books work.' },
  4:{ headline:'Disruptive angles', body:'Rahu energy thrives on unconventional GTM — alternative channels, contrarian positioning, technology-led plays. Avoid me-too markets.' },
  5:{ headline:'Move fast, distribute wide', body:'Mercury energy wins through speed, communication and multi-channel sales. Short cycles, frequent launches, sharp copy.' },
  6:{ headline:'Design and repeat-buy', body:'Venus energy converts through aesthetics, lifestyle branding and customer experience. Premium positioning and repeat-purchase models compound best.' },
  7:{ headline:'Niche depth, not mass', body:'Ketu energy rewards specialist positioning. Pick a narrow domain and own it — research, mysticism, healing, deep tech. Avoid mass-market plays.' },
  8:{ headline:'Play the long game', body:'Saturn energy compounds slowly. B2B contracts, systems, infrastructure, real estate — businesses that reward patience and process discipline.' },
  9:{ headline:'Compete and conquer', body:'Mars energy wins in competitive arenas — sports, defence, surgery, trades, performance. Direct positioning, action-oriented brand voice.' }
};

// ── Child helpers ──────────────────────────────────────────────────
function bestChildTargets(moo){
  const friends = FRIENDLY[moo] || [];
  const ranked = [];
  for(let n=1;n<=9;n++){
    if(CAUTION_NAME_NUMS.includes(n)) continue;
    let s = 0;
    if(n === moo)              s += 14;
    if(friends.includes(n))    s += 10;
    if(PREFERRED.includes(n))  s += 6;
    ranked.push({n, s});
  }
  ranked.sort((a,b)=>b.s-a.s);
  return ranked.slice(0,3).map(x=>x.n);
}

const CHILD_FOCUS = {
  1:{ headline:'Independence and clarity', body:'Sun children thrive when given leadership opportunities, decision-making space, and a clear sense of purpose. Avoid suppressing their natural authority — channel it.' },
  2:{ headline:'Emotional safety first', body:'Moon children are sensitive and intuitive. Stable home rhythms, gentle correction, and creative outlets (music, art, water-based activities) bring out their best.' },
  3:{ headline:'Learning and expression', body:'Jupiter children love to teach and absorb knowledge early. Books, philosophy, debate clubs, and travel feed their growth. They mature through wisdom, not pressure.' },
  4:{ headline:'Structure with surprise', body:'Rahu children need structure, but get bored fast. Mix routine with novelty — tech projects, unusual hobbies, problem-solving challenges. Watch for restlessness.' },
  5:{ headline:'Movement and variety', body:'Mercury children learn through doing, talking and travelling. Multiple interests at once is healthy. Sports, languages, performance — keep their nervous system engaged.' },
  6:{ headline:'Beauty and belonging', body:'Venus children blossom in aesthetic, harmonious environments. Art, design, music, gardening, gentle social spaces. They protect those they love early.' },
  7:{ headline:'Solitude and depth', body:'Ketu children need quiet time and books. Don\'t over-schedule. They mature through introspection — research, nature, mysticism, niche obsessions.' },
  8:{ headline:'Patience and self-trust', body:'Saturn children mature slowly but powerfully. Avoid comparing them to faster peers. They reward patience with discipline and long-arc achievement.' },
  9:{ headline:'Action and courage', body:'Mars children need physical outlets and clear missions. Sports, martial arts, social causes. Channel their fire into purpose or it turns into temper.' }
};

function powerDaysFor(moo){
  const days = [];
  for(let d=1;d<=31;d++) if(reduce(d)===moo) days.push(d);
  return days;
}

// ── Toolkit builders ───────────────────────────────────────────────
function buildBusinessToolkit(moo, bhag, brandName){
  const targets = bestBrandTargets(moo);
  const variants = suggestBrandVariants(brandName, moo, bhag);
  const focus = BRAND_FOCUS[moo] || BRAND_FOCUS[1];
  const days = powerDaysFor(moo);
  const founderPlanet = getPlanet(moo);
  const currentReduced = getNameNum(brandName).reduced;

  const variantsHtml = variants.length ? `
    <div style="margin-bottom:.9rem">
      <div style="font-family:sans-serif;font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:#6d4ed1;font-weight:700;margin-bottom:.5rem">✦ Stronger brand-name variants</div>
      <div style="display:flex;flex-direction:column;gap:.45rem">
        ${variants.map(v=>`
          <div style="display:flex;align-items:center;justify-content:space-between;gap:.6rem;background:rgba(124,58,237,.06);border:1px solid rgba(124,58,237,.18);border-radius:8px;padding:.55rem .75rem">
            <span style="font-family:'Playfair Display',Georgia,serif;font-size:15.5px;font-weight:700;color:var(--text)">${v.name}</span>
            <span style="font-family:sans-serif;font-size:11.5px;color:var(--text2);text-align:right;line-height:1.35">
              <strong style="color:#7c3aed">${v.score}%</strong> · Brand ${v.reduced} (${getPlanet(v.reduced)})
              ${v.compound ? `<br><span style="font-size:10.5px;color:var(--text3);font-style:italic">CD ${v.raw}: ${v.compound.l.split('·')[0].trim()}</span>` : ''}
            </span>
          </div>
        `).join('')}
      </div>
      <p style="font-family:sans-serif;font-size:11px;color:var(--text3);margin:.4rem 0 0;line-height:1.45;font-style:italic">Each variant above hits 100% Chaldean alignment — same pronunciation as your input, vibrationally locked to your founder Moolank ${moo}.</p>
    </div>
  ` : (currentReduced === moo ? `
    <div style="margin-bottom:.9rem;background:rgba(76,175,132,.10);border:1px solid rgba(76,175,132,.3);border-radius:8px;padding:.65rem .85rem;font-family:sans-serif;font-size:12.5px;color:var(--text);line-height:1.55">
      ✓ Your brand name <strong>already locks to your founder Moolank ${moo}</strong>. Focus on positioning and timing below.
    </div>
  ` : `
    <div style="margin-bottom:.9rem;background:rgba(245,196,81,.08);border:1px dashed rgba(245,196,81,.4);border-radius:8px;padding:.65rem .85rem;font-family:sans-serif;font-size:12.5px;color:var(--text);line-height:1.55">
      ✦ No phonetic tweak of "<strong>${brandName}</strong>" reaches 100% alignment with your founder Moolank ${moo} (${founderPlanet}). A different brand name may serve better — try one that reduces to <strong>${targets.join(', ')}</strong>, or use the founder-friendly numbers below as targets when brainstorming.
    </div>
  `);

  return `
    <div style="background:linear-gradient(160deg,rgba(124,58,237,.04),rgba(245,196,81,.04));border:1px solid rgba(245,196,81,.3);border-radius:12px;padding:1rem 1rem .85rem;margin-bottom:1rem">
      <div style="font-family:'Playfair Display',Georgia,serif;font-size:15.5px;font-weight:700;color:var(--text);margin-bottom:.6rem;letter-spacing:.01em">🎯 Brand-Building Toolkit</div>

      ${variantsHtml}

      <div style="margin-bottom:.85rem">
        <div style="font-family:sans-serif;font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:#6d4ed1;font-weight:700;margin-bottom:.35rem">✦ Founder-friendly brand numbers</div>
        <p style="font-family:sans-serif;font-size:12.5px;color:var(--text);line-height:1.55;margin:0">For a Moolank ${moo} (${founderPlanet}) founder, target a brand that reduces to <strong>${targets.join(', ')}</strong>. Avoid 4 and 8 — they slow business cash flow.</p>
      </div>

      <div style="margin-bottom:.85rem">
        <div style="font-family:sans-serif;font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:#6d4ed1;font-weight:700;margin-bottom:.35rem">✦ Power days for launches &amp; signings</div>
        <p style="font-family:sans-serif;font-size:12.5px;color:var(--text);line-height:1.55;margin:0">Use <strong>${days.join(', ')}</strong> of any month for incorporation, launches, contract signings or major announcements — they amplify ${founderPlanet} energy.</p>
      </div>

      <div>
        <div style="font-family:sans-serif;font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:#6d4ed1;font-weight:700;margin-bottom:.35rem">✦ ${focus.headline}</div>
        <p style="font-family:sans-serif;font-size:12.5px;color:var(--text);line-height:1.55;margin:0">${focus.body}</p>
      </div>
    </div>
  `;
}

function buildChildToolkit(moo, bhag, childName){
  const targets = bestChildTargets(moo);
  const focus = CHILD_FOCUS[moo] || CHILD_FOCUS[1];
  const days = powerDaysFor(moo);
  const corePlanet = getPlanet(moo);

  return `
    <div style="background:linear-gradient(160deg,rgba(124,58,237,.04),rgba(245,196,81,.04));border:1px solid rgba(245,196,81,.3);border-radius:12px;padding:1rem 1rem .85rem;margin-bottom:1rem">
      <div style="font-family:'Playfair Display',Georgia,serif;font-size:15.5px;font-weight:700;color:var(--text);margin-bottom:.6rem;letter-spacing:.01em">🎯 Naming Toolkit</div>

      <div style="margin-bottom:.85rem">
        <div style="font-family:sans-serif;font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:#6d4ed1;font-weight:700;margin-bottom:.35rem">✦ Core-friendly name numbers</div>
        <p style="font-family:sans-serif;font-size:12.5px;color:var(--text);line-height:1.55;margin:0">For a Moolank ${moo} (${corePlanet}) child, the ideal name reduces to <strong>${targets.join(', ')}</strong>. Avoid 4 and 8 — they add karmic friction in early life.</p>
      </div>

      <div style="margin-bottom:.85rem">
        <div style="font-family:sans-serif;font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:#6d4ed1;font-weight:700;margin-bottom:.35rem">✦ Auspicious days for naming &amp; ceremonies</div>
        <p style="font-family:sans-serif;font-size:12.5px;color:var(--text);line-height:1.55;margin:0">Use <strong>${days.join(', ')}</strong> of any month for the naming ceremony, annaprashan, school admission or other milestone events — they amplify ${corePlanet} energy.</p>
      </div>

      <div>
        <div style="font-family:sans-serif;font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:#6d4ed1;font-weight:700;margin-bottom:.35rem">✦ ${focus.headline}</div>
        <p style="font-family:sans-serif;font-size:12.5px;color:var(--text);line-height:1.55;margin:0">${focus.body}</p>
      </div>
    </div>
  `;
}

// ── Partner score ──────────────────────────────────────────────────
function partnerScore(aMoo,aBhag,bMoo,bBhag){
  const fA = FRIENDLY[aMoo]||[], fB = FRIENDLY[bMoo]||[];
  let score = 30;
  if(fA.includes(bMoo) && fB.includes(aMoo)) score += 35;
  else if(fA.includes(bMoo) || fB.includes(aMoo)) score += 18;
  if(FRIENDLY[aBhag]?.includes(bBhag)) score += 15;
  if(aMoo === bMoo) score += 8;
  if((CAUTION_NAME_NUMS||[4,8]).includes(aMoo) && (CAUTION_NAME_NUMS||[4,8]).includes(bMoo)) score -= 5;
  return Math.max(15, Math.min(96, score));
}

// ── Result HTML builders (return strings; caller writes to DOM) ────
function miniResultHTML({eyebrow,title,score,tier,pair,narrative,extraHtml,upsellLead,upsell,kind,inline,hideUpsell}){
  const lead = upsellLead || 'Want the full picture?';
  const backBtn = inline ? '' : `<div style="text-align:center"><button class="mini-back" onclick="renderMiniForm('${kind}')">← Check another</button></div>`;
  const upsellBlock = hideUpsell ? '' : `
    <div style="background:rgba(245,196,81,.08);border:1px dashed rgba(245,196,81,.5);border-radius:10px;padding:.8rem 1rem;font-family:sans-serif;font-size:12.5px;color:var(--text);line-height:1.55;margin-bottom:.85rem;">
      <strong style="color:#9d4edd">${lead}</strong> ${upsell}
    </div>
    <a href="report?ref=mini_${kind}" class="mini-cta" onclick="trackEvent('mini_cta_clicked',{kind:'${kind}'})">Unlock Full Chaldean Report — ₹199 →</a>
  `;
  return `
    <div class="mini-eyebrow">${eyebrow}</div>
    <h2 class="mini-title">${title}</h2>
    <div class="mini-result-card">
      <div style="font-family:sans-serif;font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:#9d7fff;font-weight:700">Chaldean Score</div>
      <div class="mini-score">${score}%</div>
      <span class="mini-tag ${tier.cls}">${tier.icon} ${tier.label}</span>
      <p class="mini-pair">${pair}</p>
    </div>
    <div class="mini-narrative">${narrative}</div>
    ${extraHtml || ''}
    ${upsellBlock}
    ${backBtn}
  `;
}

// Tightened upsell-pivot copy: connects free brand-tool result to the
// founder's own ₹199 personal report explicitly.
const UPSELL_BUSINESS = 'This free check is about <strong>your brand</strong>. The ₹199 Chaldean Destiny Report is about <strong>you, the founder</strong> — your Moolank, planetary alignment and 5-year personal-year cycle, so you know which year favours launching, scaling or rebranding. Brands can change. The founder is constant.';
const UPSELL_CHILD    = 'This free check tells you about <strong>the name</strong> you\'re considering. The ₹199 Chaldean Destiny Report is about <strong>you, the parent</strong> — your Moolank, planetary alignment and 5-year personal-year cycle, so you understand the energy you carry into naming and raising your child.';
const UPSELL_PARTNER  = 'This free check shows the pairing. The ₹199 Chaldean Destiny Report includes a dedicated <strong>Compatibility Insight chapter</strong> — planetary interaction map, friction-points and harmony-builders — based on your own complete Chaldean reading.';

function buildPartnerResultHTML(yn,yd,pn,pd, opts){
  const yMoo = getBirthNum(yd), yBhag = getDestinyNum(yd);
  const pMoo = getBirthNum(pd), pBhag = getDestinyNum(pd);
  const score = partnerScore(yMoo,yBhag,pMoo,pBhag);
  const t = tierOf(score);
  const yPlanet = getPlanet(yMoo), pPlanet = getPlanet(pMoo);
  const yArche = ARCHETYPES[yMoo], pArche = ARCHETYPES[pMoo];
  trackEvent('mini_analyzer_result', {kind:'partner', score});

  let narrative;
  if(t.cls==='high'){
    narrative = `<strong>${yPlanet} meets ${pPlanet}</strong> — your Chaldean numbers reinforce each other. The ${yArche.toLowerCase()} in you finds genuine ease with the ${pArche.toLowerCase()} in them. Most disagreements resolve themselves once spoken aloud.`;
  } else if(t.cls==='mid'){
    narrative = `<strong>${yPlanet} meets ${pPlanet}</strong> — workable, with conscious effort. Your rhythms differ, which is why you irritate each other in small ways and complement each other in big ones. Patience and explicit communication amplify the harmony.`;
  } else {
    narrative = `<strong>${yPlanet} meets ${pPlanet}</strong> — different rhythms, which doesn't mean wrong. The bond can work, but it asks for honest naming of needs. Assumptions are where most friction lives in this pairing.`;
  }
  return miniResultHTML({
    eyebrow:'💞 Partner Compatibility',
    title:`${firstWord(yn)} ✦ ${firstWord(pn)}`,
    score, tier:t,
    pair:`${yArche} <span style="opacity:.55">×</span> ${pArche}`,
    narrative,
    upsellLead:'Go deeper:',
    upsell:UPSELL_PARTNER,
    kind:'partner',
    inline: !!(opts&&opts.inline)
  });
}

function buildChildResultHTML(cn,cd, opts){
  const moo = getBirthNum(cd), bhag = getDestinyNum(cd);
  const {raw, reduced} = getNameNum(cn);
  const score = compatPct(reduced, raw, moo, bhag);
  const t = tierChild(score);
  const corePlanet = getPlanet(moo), namePlanet = getPlanet(reduced);
  const arche = ARCHETYPES[moo];
  trackEvent('mini_analyzer_result', {kind:'child', score});

  let narrative;
  if(t.cls==='high'){
    narrative = `<strong>${firstWord(cn)}</strong> vibrates as ${reduced} (${namePlanet}) — and that energy genuinely supports a Moolank ${moo} (${corePlanet}) child. The name strengthens "${arche.toLowerCase()}" qualities rather than fighting them.`;
  } else if(t.cls==='mid'){
    narrative = `<strong>${firstWord(cn)}</strong> vibrates as ${reduced} (${namePlanet}). It's workable for a Moolank ${moo} (${corePlanet}) child — neither amplifying nor suppressing their core.`;
  } else {
    narrative = `<strong>${firstWord(cn)}</strong> vibrates as ${reduced} (${namePlanet}), which sits in tension with a Moolank ${moo} (${corePlanet}) core. The child's natural ${arche.toLowerCase()} energy will work harder than it needs to.`;
  }
  return miniResultHTML({
    eyebrow:'👶 Child Name Alignment',
    title:firstWord(cn),
    score, tier:t,
    pair:`Name ${reduced} (${namePlanet}) <span style="opacity:.55">×</span> Moolank ${moo} (${corePlanet})`,
    narrative,
    extraHtml: buildChildToolkit(moo, bhag, cn),
    upsellLead:'Build your foundation:',
    upsell:UPSELL_CHILD,
    kind:'child',
    inline: !!(opts&&opts.inline),
    hideUpsell: !!(opts&&opts.hideUpsell)
  });
}

function buildBusinessResultHTML(bn,bd, opts){
  const moo = getBirthNum(bd), bhag = getDestinyNum(bd);
  const {raw, reduced} = getNameNum(bn);
  const score = compatPct(reduced, raw, moo, bhag);
  const t = tierBrand(score);
  const founderPlanet = getPlanet(moo), brandPlanet = getPlanet(reduced);
  const compound = (typeof CD!=='undefined' && CD[raw]) ? CD[raw] : null;
  trackEvent('mini_analyzer_result', {kind:'business', score});

  let narrative;
  if(t.cls==='high'){
    narrative = `<strong>${bn}</strong> reduces to ${reduced} (${brandPlanet}) — a vibration that amplifies a founder operating on ${founderPlanet} energy. The brand name does the heavy lifting for you.`;
  } else if(t.cls==='mid'){
    narrative = `<strong>${bn}</strong> reduces to ${reduced} (${brandPlanet}). It's a workable brand vibration for a ${founderPlanet} founder — neither helping nor hurting much.`;
  } else {
    narrative = `<strong>${bn}</strong> reduces to ${reduced} (${brandPlanet}), which works against a ${founderPlanet} founder's energy. The brand will feel like effort rather than flow.`;
  }
  if(compound){
    narrative += ` <em style="color:var(--text2)">Compound ${raw}: ${compound.l}.</em>`;
  }
  return miniResultHTML({
    eyebrow:'🏢 Business Name Vibration',
    title:bn,
    score, tier:t,
    pair:`Brand ${reduced} (${brandPlanet}) <span style="opacity:.55">×</span> Founder Moolank ${moo} (${founderPlanet})`,
    narrative,
    extraHtml: buildBusinessToolkit(moo, bhag, bn),
    upsellLead:'Build your foundation:',
    upsell:UPSELL_BUSINESS,
    kind:'business',
    inline: !!(opts&&opts.inline),
    hideUpsell: !!(opts&&opts.hideUpsell)
  });
}
