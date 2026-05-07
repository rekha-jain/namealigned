#!/usr/bin/env python3
"""
Generate the next batch of programmatic SEO pages:

  /birth-number-N-career           (9)  — Moolank-led career angle
  /life-path-number-N-love-life    (9)  — Bhagyank-led relationships angle

Each ~900-1100 body words, unique per number, with Article +
BreadcrumbList + FAQPage JSON-LD. Same template style as the earlier
generators so the visual is consistent.
"""
import json, os

BASE = 'https://www.namealigned.com'
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Per-number archetype data (planet-keyed; consistent across page types)
ARCH = {
1:{'planet':'Sun','glyph':'☀','tag':'Leadership · Authority · Visibility','color':'Gold · Orange · Red'},
2:{'planet':'Moon','glyph':'☾','tag':'Sensitivity · Partnership · Emotional Wisdom','color':'White · Silver · Cream'},
3:{'planet':'Jupiter','glyph':'♃','tag':'Expression · Optimism · Teaching','color':'Yellow · Cream · Violet'},
4:{'planet':'Rahu','glyph':'◈','tag':'Innovation · Foreign Reach · Systems','color':'Blue · Electric · Grey'},
5:{'planet':'Mercury','glyph':'☿','tag':'Adaptability · Communication · Movement','color':'Green · Light Grey'},
6:{'planet':'Venus','glyph':'♀','tag':'Harmony · Aesthetic · Devotion','color':'Pink · White · Pastel Blue'},
7:{'planet':'Ketu','glyph':'◉','tag':'Wisdom · Inquiry · Solitude','color':'Violet · Purple · Grey'},
8:{'planet':'Saturn','glyph':'♄','tag':'Discipline · Authority · Long Game','color':'Black · Dark Blue · Dark Grey'},
9:{'planet':'Mars','glyph':'♂','tag':'Courage · Service · Decisive Action','color':'Red · Crimson · Deep Orange'},
}

# ── CAREER content (Birth Number = Moolank, daily work style) ──
CAREER = {
1:{'work_style':'You work best when your judgement is the product. Roles where decisions originate with you — founder, partner, principal, creative director — tend to be where money and recognition compound.',
   'fields':['Founder / CEO / Managing Director','Government & Public Office','Independent professional practice (law, medicine, consulting)','Entertainment & Media as a public figure','Gold, gemstone or luxury trade','Defence-services leadership'],
   'income_pattern':'Income tends to be lumpy in early years and step-functions upward once your name carries reputation. The Sun rewards visibility; expect significant income growth after your work bears your personal signature.',
   'avoid':'Roles where you execute someone else\'s vision quietly tend to feel hollow over time, regardless of pay.',
   'faq':[
     ('What jobs are best for Birth Number 1?','Founder, CEO, government, independent practice, gold/luxury trade — anything where your decisions are the product.'),
     ('Is Birth Number 1 good for business?','Strongly so. The Sun rewards initiative and visibility. Most successful Birth Number 1 careers involve building or leading something whose success bears their personal stamp.'),
     ('What\'s the salary outlook for Birth Number 1?','Lumpy in early years, step-functions upward once reputation compounds. Direct correlation with willingness to be visible.'),
     ('Should Birth Number 1 work in a corporate job?','It can work as a launchpad, but most thrive eventually in roles that grant decision-making authority — even a small business unit run autonomously beats a senior title without authority.'),
   ]},
2:{'work_style':'You work best in roles where reading emotion is the value, not a side-effect. The Moon rewards rooms where empathy compounds — counselling, hospitality, design, partnership-led businesses.',
   'fields':['Counselling & Psychology','Hospitality, Restaurants & Hotels','Music, Art & Poetry','Nursing & Caregiving','Residential Real Estate','HR & People Operations'],
   'income_pattern':'Income tends to grow through retention and depth — the people you serve come back, refer, recommend. Less burst-led than 1 or 9, more compounding.',
   'avoid':'Adversarial, high-friction commercial environments (cold sales, litigation, trading floors) drain Moon energy faster than money compensates.',
   'faq':[
     ('What careers suit Birth Number 2?','Counselling, hospitality, art, music, nursing, residential real estate, HR — fields where reading emotion is the work.'),
     ('Is Birth Number 2 good in business?','Yes, particularly partnership-led businesses where you\'re the relationships side of a duo. Solo cold-sales rarely fits.'),
     ('Why does Birth Number 2 burn out at work?','Emotional permeability — you absorb other people\'s states. Without daily decompression, the same gift that makes you good at the job exhausts you.'),
     ('Which boss-types suit Birth Number 2?','Patient, principle-led leaders. Bullying or chaos-driven environments magnify Moon sensitivity into illness.'),
   ]},
3:{'work_style':'You work best where your voice carries the value — teaching, writing, advising, performing. Jupiter rewards generosity; the more you share, the more comes back.',
   'fields':['Education, Training & Coaching','Law & Justice','Banking, Finance, Asset Management','Religion / Spirituality','Publishing, Media, Broadcasting','Advisory & Consulting'],
   'income_pattern':'Audience-led — slow to start, then exponential as your platform compounds. Steady income arrives after years of public output.',
   'avoid':'Closed-door, never-show-your-face roles deny Jupiter its expansion channel; income and meaning both stagnate.',
   'faq':[
     ('What jobs are best for Birth Number 3?','Education, law, finance, religion, publishing, advisory — anything where your voice or judgement is the product.'),
     ('Is Birth Number 3 lucky for money?','Jupiter is the abundance planet, especially through teaching, publishing, finance and law. Direct cash speculation is less reliable.'),
     ('Why does Birth Number 3 attract opportunities?','Jupiter expands. Whatever you put outward gets amplified — the work and the audience both grow.'),
     ('What if my Birth Number 3 work feels stuck?','Usually a sign you\'ve stopped publishing. Jupiter rewards the creator who keeps showing up; even quiet output, repeated for years, eventually compounds.'),
   ]},
4:{'work_style':'You work best where the conventional playbook doesn\'t exist yet. Rahu rewards the builder of new categories, foreign markets, technologies and methodologies.',
   'fields':['Engineering & Architecture','IT, Software, AI / ML','Research, Analytics, Data','Logistics, Supply Chain, Aviation','Foreign Trade, Cross-border Commerce','Renewables, Climate, Frontier Tech'],
   'income_pattern':'Spiky — windfall years between long stretches of building. Equity and IP compensation tend to outperform pure salary.',
   'avoid':'Highly-formal, hierarchy-heavy, slow-moving institutions tend to feel suffocating; restlessness leads to abrupt exits.',
   'faq':[
     ('What careers suit Birth Number 4?','Engineering, tech, research, logistics, foreign trade, frontier industries — anywhere original thinking is rewarded over conformity.'),
     ('Is Birth Number 4 unlucky for business?','No — the reputation comes from Rahu being misunderstood. Used well, Birth Number 4 thrives in tech and foreign trade.'),
     ('Should Birth Number 4 take equity over salary?','Often yes — Rahu\'s rewards arrive in lumps tied to building something that didn\'t exist before. Equity captures that better than salary.'),
     ('Why does Birth Number 4 quit jobs abruptly?','Rahu intolerates rigidity. The leaves usually look sudden from outside but follow months of internal misalignment.'),
   ]},
5:{'work_style':'You work best at speed — short cycles, multiple projects, high information density. Mercury rewards the trader, the journalist, the founder who pivots before others have noticed.',
   'fields':['Media, Journalism, Broadcasting','Sales, Marketing, Agencies','Travel, Tourism, Hospitality Tech','Stock Trading & Day Trading','Digital Startups, Growth Roles','Ed-tech, Content Creator Economy'],
   'income_pattern':'Velocity-led — high turnover of small wins. Mercury rarely produces single big paydays; income comes from many small, fast loops.',
   'avoid':'Slow, monolithic, multi-year-cycle roles (heavy industry, government bureaucracies) tend to drain interest before maturity.',
   'faq':[
     ('What jobs suit Birth Number 5?','Media, sales, marketing, trading, digital startups, content economy — anywhere speed of communication is value.'),
     ('Is Birth Number 5 good for trading?','Particularly suited — Mercury thrives on short cycles and high-frequency information. Risk-management discipline is the cost.'),
     ('Why does Birth Number 5 hop jobs?','Mercury runs out of Mercury-friendly material before tenure expectations end. Boredom isn\'t a flaw — it\'s a signal that the role no longer rewards the vibration.'),
     ('What\'s the long-term path for Birth Number 5?','A career portfolio rather than a career — multiple parallel income streams that the same speed-of-communication strength serves.'),
   ]},
6:{'work_style':'You work best where care and aesthetic taste are the product, not the wrapper. Venus rewards devoted, beauty-led work; people remember how your work made them feel.',
   'fields':['Fashion, Design, Interiors','Entertainment, Film, Music','Hospitality, Hotels, Restaurants','Cosmetics, Beauty, Wellness','Social Work, NGOs, Counselling','Brand & Creative Direction'],
   'income_pattern':'Compounds through reputation and word-of-mouth. Slow to start, durable once it lands; brand-and-relationship driven, not transactional.',
   'avoid':'Pure number-crunching, cold transactional environments work technically but deplete the Venus signature over time.',
   'faq':[
     ('What jobs are best for Birth Number 6?','Design, fashion, entertainment, hospitality, cosmetics, social work — fields where care and aesthetic taste are central.'),
     ('Is Birth Number 6 good in business?','Particularly in service businesses with a strong brand layer. Repeat customers and referrals do most of the work once trust is established.'),
     ('What kind of boss suits Birth Number 6?','Patient, aesthetic-aware leaders. Brutal commercial environments wear Venus down faster than the salary justifies.'),
     ('Should Birth Number 6 freelance?','Often a strong fit — Venus thrives on personal client relationships. The risk is over-giving without compensating boundaries.'),
   ]},
7:{'work_style':'You work best with depth, solitude and time to think. Ketu rewards research, philosophy and the kind of insight that only emerges after long quiet hours.',
   'fields':['Research, Science, Academia','Spirituality, Healing, Therapy','Writing, Literature, Editing','Astrology, Mysticism, Philosophy','Investment Research, Equity Analysis','Forensic & Investigative Work'],
   'income_pattern':'Step-changes — long quiet years punctuated by recognition that revalues earlier work. Patience rewards more than hustle.',
   'avoid':'Open-floor, performance-led, talk-fast environments tend to short-circuit the depth Ketu requires to function.',
   'faq':[
     ('What careers suit Birth Number 7?','Research, spirituality, writing, academia, equity analysis, investigative work — depth-rewarding fields.'),
     ('Is Birth Number 7 good for business?','Less suited to fast-cycle commercial businesses; better in advisory, research-heavy or knowledge-product businesses.'),
     ('Why does Birth Number 7 prefer working alone?','Ketu regenerates in stillness. Solitude isn\'t avoidance — it\'s how the vibration generates the very insight that makes you valuable.'),
     ('What if my Birth Number 7 work feels invisible?','Often it is, then suddenly isn\'t. Step-change recognition arrives when the work\'s depth becomes culturally relevant — keep the depth.'),
   ]},
8:{'work_style':'You work best at long horizons. Saturn rewards endurance — the project that takes a decade builds the authority that lasts another decade.',
   'fields':['Finance, Banking, Investment','Law & Courts','Mining, Heavy Industry, Infrastructure','Import/Export, Industrial Trade','Real Estate Investment & Development','Senior Operations & Compliance'],
   'income_pattern':'Compounds slowly and durably. The breakthrough usually arrives years after the recognition you deserved would have been timely. Wealth is built, not lucked into.',
   'avoid':'Fast-cycle, fashion-driven roles fight the Saturn signature; the wins feel hollow and the burnout is real.',
   'faq':[
     ('What jobs suit Birth Number 8?','Finance, law, real estate, heavy industry, import-export — anywhere long-horizon discipline is rewarded.'),
     ('Is Birth Number 8 unlucky?','No, but it\'s slow. Saturn rewards endurance; quick-win approaches don\'t fit. Used well, Birth Number 8 builds enduring authority.'),
     ('Why does Birth Number 8 wait so long for recognition?','Saturn delays. The delay is part of the build — when authority finally lands, it\'s real and durable, not borrowed.'),
     ('Should Birth Number 8 take risks early in career?','Calculated risks yes; speculative risks rarely pay. Saturn rewards the move that compounds for fifteen years, not the one that pays this quarter.'),
   ]},
9:{'work_style':'You work best under pressure with a clear cause. Mars rewards the decisive operator — the surgeon, the soldier, the activist, the founder fighting a real fight.',
   'fields':['Military, Defence, Security','Surgery & Emergency Medicine','Sports & Athletics','Politics, Activism, Journalism','Engineering Projects with Field Risk','Crisis-Response Roles'],
   'income_pattern':'Recognition-led — Mars work tends to be either visible (and richly rewarded) or invisible (and undervalued). Choose visibility deliberately.',
   'avoid':'Slow-moving, conflict-averse, consensus-driven environments tend to bore Mars to leaving.',
   'faq':[
     ('What careers suit Birth Number 9?','Defence, surgery, sports, politics, activism, crisis-response — fields requiring decisive movement under pressure.'),
     ('Is Birth Number 9 good in business?','Yes if the business is fight-led — protecting customers, building in a hostile market, taking ground others won\'t. Less suited to consensus-led commercial environments.'),
     ('Why does Birth Number 9 burn out?','Mars runs hot. Crash-and-recovery rhythm is healthy when planned, toxic when ignored.'),
     ('Should Birth Number 9 lead teams?','Yes — but in cause-led contexts, not pure profit-led ones. Mars leadership is at its best when there\'s something to defend or change.'),
   ]},
}

# ── LOVE LIFE content (Life Path / Bhagyank, destiny in relationships) ──
LOVE = {
1:{'partner_arc':'Your destiny in love is shaped by an early lesson about leadership inside relationships. Sun energy struggles when both partners want to lead in the same domain — the work of marriage is finding distinct domains where each person leads naturally.',
   'gives':'Visibility, ambition, decisive forward motion. You bring scale to a partnership.',
   'asks':'Reception. Sun energy can override quieter partners without realising; the growth is learning to listen for what isn\'t being said.',
   'best':'Life Path 1, 2, 4, 9. The 1+2 dynamic (Sun-Moon) is one of the strongest classical pairings — leadership softened by sensitivity.',
   'faq':[
     ('Who is Life Path 1 most compatible with in love?','Life Paths 1, 2, 4 and 9. The 1+2 (Sun-Moon) pairing is traditionally one of the strongest because the Moon\'s sensitivity balances the Sun\'s decisiveness.'),
     ('Is Life Path 1 good for marriage?','Yes, when domains are clear. Sun energy struggles when both partners want to lead the same area; once each person has their own territory, the marriage strengthens.'),
     ('Why does Life Path 1 attract dependent partners?','Visibility attracts both leaders and followers. Healthy Life Path 1 marriages avoid the rescue dynamic by deliberately partnering with self-led people.'),
     ('Can Life Path 1 marry Life Path 8?','It can work but takes effort — Sun and Saturn run on different timescales. Mutual respect for each other\'s pace is the work.'),
   ]},
2:{'partner_arc':'Your destiny in love is built around the slow ripening of trust. Moon energy rarely connects fast — depth comes after a partner has shown up consistently across small, ordinary tests over time.',
   'gives':'Emotional fluency, devotion, the rare gift of being deeply heard.',
   'asks':'Patience from your partner with how long it takes you to feel safe enough to need them visibly.',
   'best':'Life Path 1, 2, 7. The 2+7 pairing (Moon-Ketu) is a classical depth match — both partners value inner life over performance.',
   'faq':[
     ('Who is Life Path 2 most compatible with in love?','Life Paths 1, 2 and 7. The 2+7 pairing is particularly strong because both partners are introspective and prefer depth to volume.'),
     ('Is Life Path 2 too sensitive for marriage?','No — sensitivity is the gift. The growth work is learning to ask for what you need rather than expecting partners to read it from your moods.'),
     ('Why does Life Path 2 stay too long in unhealthy relationships?','Moon energy bonds deeply and grieves slowly. The growth is learning that loyalty to the past isn\'t the same as commitment to the present.'),
     ('Can Life Path 2 marry Life Path 8?','Often yes — Moon\'s warmth softens Saturn\'s structure. The key is mutual respect for each other\'s emotional rhythm.'),
   ]},
3:{'partner_arc':'Your destiny in love is shaped by the words you exchange. Jupiter expands what gets spoken — kind partnerships flourish, conflict-heavy partnerships also expand fast. Choose your conversational diet carefully.',
   'gives':'Optimism, humour, the ability to make a difficult topic feel survivable.',
   'asks':'Slowing down sometimes — Jupiter speaks faster than feelings settle. Pauses build the depth that words alone don\'t.',
   'best':'Life Path 3, 6, 9. The 3+6 (Jupiter-Venus) pairing combines abundance and harmony — a classical happy-marriage signature.',
   'faq':[
     ('Who is Life Path 3 most compatible with in love?','Life Paths 3, 6 and 9 — the Jupiter-Venus-Mars triangle. Jupiter and Venus together is one of the strongest classical signatures for a warm marriage.'),
     ('Is Life Path 3 good for long marriages?','Yes — Jupiter\'s warmth ages well. The risk is over-giving in early years and resenting it later; balance comes from earlier honesty.'),
     ('Why does Life Path 3 sound the most fine when least fine?','Jupiter expands the chosen presentation, including the cheerful one. The growth is letting partners see what\'s underneath the warmth.'),
     ('Can Life Path 3 marry Life Path 8?','It works when the Saturn partner appreciates Jupiter\'s warmth as a gift, not a frivolity. Saturn-Jupiter is one of the most studied tense pairings in classical numerology.'),
   ]},
4:{'partner_arc':'Your destiny in love is unconventional by design. Rahu rarely chooses the partner the family expected; long-term marriages often involve cross-cultural, cross-religion or cross-geography elements.',
   'gives':'A perspective most partners haven\'t encountered before, and a willingness to build the relationship from first principles.',
   'asks':'Stability rituals to compensate for the natural restlessness — anniversaries, recurring dates, small unchanging routines.',
   'best':'Life Path 1, 2, 4, 8. The 4+8 pairing (Rahu-Saturn) shares an outsider quality and rewards patient long-game commitment.',
   'faq':[
     ('Who is Life Path 4 most compatible with in love?','Life Paths 1, 2, 4 and 8. The 4+8 pairing is particularly resilient because both numbers value endurance over novelty.'),
     ('Why do Life Path 4 marriages look unconventional?','Rahu does. Cross-cultural, late-blooming or non-traditional structures are more common than average.'),
     ('Is Life Path 4 emotionally distant?','Read that way sometimes; usually it\'s actually thinking-pace difference. Verbal partners feel emotional distance where there\'s really intellectual processing.'),
     ('Can Life Path 4 marry Life Path 6?','Yes — Venus softens Rahu\'s edges. The key is Venus partner appreciating that Rahu\'s loyalty looks different from theirs.'),
   ]},
5:{'partner_arc':'Your destiny in love is built around partners who keep up. Mercury\'s pace bores easily; relationships that thrive include constant new conversation, fresh adventure and intellectual oxygen.',
   'gives':'Energy, humour, intellectual companionship, never-quite-the-same-twice presence.',
   'asks':'Anchoring rituals — Mercury moves fast, partners need predictable returns to home base.',
   'best':'Life Path 1, 5, 9. The 5+1 pairing (Mercury-Sun) combines speed and authority into a high-leverage marriage.',
   'faq':[
     ('Who is Life Path 5 most compatible with in love?','Life Paths 1, 5 and 9 — fast, fire-and-air combinations. 3 and 6 also work supportively.'),
     ('Why does Life Path 5 fear commitment?','Mercury intolerates feeling stuck. Long-term commitment works when growth, novelty and freedom are explicitly built in, not just hoped for.'),
     ('Is Life Path 5 unfaithful?','Not by design — but boredom + Mercury + unspoken expectations is a risky combination. Strong Life Path 5 marriages are honest about novelty needs early.'),
     ('Can Life Path 5 marry Life Path 4?','Possible but takes work — different speeds. Mercury runs faster than Rahu, and Rahu requires more solitary processing time.'),
   ]},
6:{'partner_arc':'Your destiny is built around partnership; few Life Path 6 lives feel complete in deep solitude. Venus rewards devotion, beauty and the patient construction of a shared aesthetic life.',
   'gives':'Devotion, aesthetic care, emotional fluency, the rare gift of making partners feel truly seen.',
   'asks':'Reciprocity. Venus over-gives by default; the growth is asking partners to bring proportionate care, not just receive it.',
   'best':'Life Path 3, 6, 9. The 6+9 (Venus-Mars) pairing is a passionate-and-protective signature; 3+6 is the abundance-and-harmony classic.',
   'faq':[
     ('Who is Life Path 6 most compatible with in love?','Life Paths 3, 6 and 9. The Venus-Jupiter-Mars triangle. 1, 4 and 5 also work supportively.'),
     ('Is Life Path 6 the marriage number?','Often called that. Venus rules partnership; few Life Path 6 lives feel complete without devoted long-term love.'),
     ('Why does Life Path 6 over-give in relationships?','Venus over-gives by default. The growth is asking for reciprocity early; partners often won\'t bring it unless asked.'),
     ('Can Life Path 6 marry Life Path 8?','It can; Venus softens Saturn. The key is Saturn partner explicitly valuing Venus\'s aesthetic and emotional offerings.'),
   ]},
7:{'partner_arc':'Your destiny in love is depth-led. Ketu rarely chooses social-performance partners; the long-term match is someone who values quiet over noise and finds your inwardness magnetic, not strange.',
   'gives':'Depth of conversation, emotional honesty, the rare gift of being truly listened to.',
   'asks':'A partner who doesn\'t need constant external validation — Ketu\'s alone-time isn\'t rejection.',
   'best':'Life Path 2, 7. The 2+7 pairing is a classical depth match — both partners value inner life over performance.',
   'faq':[
     ('Who is Life Path 7 most compatible with in love?','Life Paths 2 and 7 are the strongest matches. 1, 4 and 6 also work supportively.'),
     ('Is Life Path 7 hard to marry?','Not hard — selective. Ketu values depth over volume; once a real match is found, commitment runs unusually deep.'),
     ('Why does Life Path 7 need alone time even in marriage?','Ketu regenerates in stillness. Strong Life Path 7 marriages explicitly preserve solo space — not as rejection, as fuel.'),
     ('Can Life Path 7 marry Life Path 9?','Possible but high-friction — Mars\'s heat and Ketu\'s coolness need conscious negotiation. Works when both partners deeply respect each other\'s rhythm.'),
   ]},
8:{'partner_arc':'Your destiny in love is built across decades, not seasons. Saturn rewards the partnership that grows roots through hard years — the long-term marriages of Life Path 8 people often look unremarkable in year five and remarkable by year fifteen.',
   'gives':'Reliability, accountability, a partner who shows up year after year regardless of fashion.',
   'asks':'A partner who doesn\'t mistake slow trust for absent affection — Saturn loves quietly and durably, not loudly.',
   'best':'Life Path 2, 4, 6, 8. The 8+2 pairing balances Saturn\'s structure with Moon\'s warmth.',
   'faq':[
     ('Who is Life Path 8 most compatible with in love?','Life Paths 2, 4, 6 and 8. The 8+2 pairing is particularly classic — Saturn\'s authority softened by Moon\'s emotional fluency.'),
     ('Is Life Path 8 lucky in marriage?','Slow but durable. Marriages survive into the long run more often than Life Path 8 marriages of the early years suggest.'),
     ('Why does Life Path 8 look composed but feel heavy in love?','Saturn carries weight by default. Strong marriages explicitly create space for the heaviness to be seen, not just managed.'),
     ('Can Life Path 8 marry Life Path 5?','It takes work — different speeds, different priorities. Mercury\'s velocity vs Saturn\'s endurance. Possible with explicit pace-negotiation.'),
   ]},
9:{'partner_arc':'Your destiny in love is intense and protective. Mars chooses partners worth defending; the long-term marriage is rarely lukewarm — either deeply loyal or short-lived.',
   'gives':'Loyalty as a force, courage in difficult moments, a partner who fights for the relationship explicitly.',
   'asks':'A partner who doesn\'t take the heat personally — Mars runs hot, the heat isn\'t aimed at you, it\'s the engine.',
   'best':'Life Path 1, 3, 5, 9. The 9+3 (Mars-Jupiter) pairing combines courage with optimism into a classically vibrant marriage.',
   'faq':[
     ('Who is Life Path 9 most compatible with in love?','Life Paths 1, 3, 5 and 9. Fire-and-air pairings. 6 and 7 also work supportively.'),
     ('Is Life Path 9 too intense for marriage?','Not for partners who appreciate the intensity. Lukewarm partners burn out fast; matched-intensity partners thrive.'),
     ('Why does Life Path 9 fight in relationships?','Mars\'s default mode is fight — used well it\'s defending the relationship; misused, it\'s the relationship itself.'),
     ('Can Life Path 9 marry Life Path 2?','Possible but high-contrast — Mars heat vs Moon coolness. Works when Mars partner consciously protects Moon partner\'s sensitivity.'),
   ]},
}

# ── Page renderers ───────────────────────────────────────────

CSS_BLOCK = '''<style>
.nn-hero{padding:3.5rem 0 1.75rem;text-align:center;background:linear-gradient(160deg,#1a1340 0%,#2a1a5c 100%);color:#f0ece0;}
.nn-hero .badge{display:inline-block;font-family:sans-serif;font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:#f0b429;background:rgba(240,180,41,.12);padding:5px 14px;border-radius:20px;border:1px solid rgba(240,180,41,.35);margin-bottom:1rem;}
.nn-hero h1{font-family:'Playfair Display',Georgia,serif;font-size:clamp(28px,4.2vw,44px);line-height:1.2;margin:0 auto .5rem;max-width:780px;}
.nn-hero .glyph{font-size:48px;color:#f0b429;line-height:1;margin-bottom:.75rem;}
.nn-hero .tag{font-family:sans-serif;font-size:14px;color:rgba(240,236,224,.78);letter-spacing:.06em;}
.nn-body{max-width:780px;margin:0 auto;padding:2rem 1.25rem;}
.nn-body h2{font-family:'Playfair Display',Georgia,serif;font-size:24px;color:var(--text);margin:2rem 0 .65rem;line-height:1.25;}
.nn-body h3{font-family:'Playfair Display',Georgia,serif;font-size:18px;color:var(--text);margin:1.5rem 0 .5rem;}
.nn-body p{font-family:sans-serif;font-size:14.5px;line-height:1.75;color:var(--text);margin-bottom:1rem;}
.nn-body ul{font-family:sans-serif;font-size:14px;line-height:1.85;color:var(--text);padding-left:1.25rem;margin-bottom:1.25rem;}
.nn-body li{margin-bottom:.35rem;}
.nn-cta-band{background:var(--gold-l);border:1.5px solid var(--gold-b);border-radius:14px;padding:1.5rem;margin:2rem 0;text-align:center;}
.nn-cta-band h3{margin:0 0 .35rem;font-family:Georgia,serif;font-size:19px;color:var(--text);}
.nn-cta-band p{margin:0 0 1rem;font-size:13.5px;color:var(--text2);font-family:sans-serif;}
.nn-cta-band .btn-pair{display:flex;gap:.6rem;justify-content:center;flex-wrap:wrap;}
.nn-cta-band a{display:inline-block;font-family:sans-serif;font-size:13.5px;font-weight:600;padding:9px 18px;border-radius:8px;text-decoration:none;}
.nn-cta-band a.primary{background:var(--gold);color:#0a0820;}
.nn-cta-band a.outline{background:transparent;color:var(--text);border:1.5px solid var(--gold-b);}
.nn-faq{margin:2rem 0;}
.nn-faq details{background:var(--card);border:1px solid var(--gold-b);border-radius:10px;padding:.85rem 1.1rem;margin-bottom:.6rem;}
.nn-faq summary{font-family:Georgia,serif;font-size:15px;font-weight:700;color:var(--text);cursor:pointer;line-height:1.4;}
.nn-faq details[open] summary{margin-bottom:.5rem;}
.nn-faq details p{font-family:sans-serif;font-size:13.5px;line-height:1.7;color:var(--text2);margin:0;}
.nn-related-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:.75rem;}
@media(max-width:640px){.nn-related-grid{grid-template-columns:1fr;}}
.nn-rel-card{display:flex;flex-direction:column;background:var(--card);border:1px solid var(--gold-b);border-radius:10px;padding:.9rem 1rem;text-decoration:none;color:var(--text);}
.nn-rel-card .eb{font-family:sans-serif;font-size:9.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--gold-d);font-weight:700;margin-bottom:.25rem;}
.nn-rel-card .ti{font-family:Georgia,serif;font-size:14.5px;font-weight:700;line-height:1.3;}
nav.crumb{font-family:sans-serif;font-size:12px;color:var(--text3);padding:1rem 1.25rem 0;max-width:780px;margin:0 auto;}
nav.crumb a{color:var(--text3);text-decoration:none;}
</style>'''

NAV = '''<nav class="nav">
  <div class="container nav-inner">
    <a href="/" class="nav-logo" aria-label="NameAligned.com" style="font-family:'Playfair Display',Georgia,serif;text-decoration:none;display:inline-flex;flex-direction:column;align-items:stretch;gap:0;line-height:1;">
      <span style="font-size:26px;font-weight:700;color:#0a0820;letter-spacing:-.01em;line-height:1;white-space:nowrap;">Name<span style="color:#6d4ed1;">Aligned</span><span style="color:#6d4ed1;font-weight:600;">.com</span></span>
      <span style="font-family:'Inter','Helvetica Neue',Arial,sans-serif;font-size:9.5px;font-weight:600;color:#8a7ba8;text-transform:uppercase;margin-top:5px;display:flex;justify-content:space-between;width:100%;"><span>C</span><span>H</span><span>A</span><span>L</span><span>D</span><span>E</span><span>A</span><span>N</span><span>&nbsp;</span><span>N</span><span>U</span><span>M</span><span>E</span><span>R</span><span>O</span><span>L</span><span>O</span><span>G</span><span>Y</span></span>
    </a>
    <ul class="nav-links">
      <li><a href="/analyzer">Free Analysis</a></li>
      <li><a href="/blog">Blog</a></li>
      <li><a href="/about">About</a></li>
      <li><a href="/analyzer" class="nav-cta">Try Free →</a></li>
    </ul>
  </div>
</nav>'''

FOOTER = '''<footer class="footer">
  <div class="container">
    <div class="footer-grid">
      <div><div class="footer-brand">☽ NameAligned.com</div><p class="footer-tagline">Free Chaldean numerology for everyone.</p></div>
      <div><div class="footer-col-title">Free Tools</div><ul class="footer-links"><li><a href="/name-numerology-calculator">Name Calculator</a></li><li><a href="/name-correction-numerology">Name Correction</a></li><li><a href="/business-name-numerology">Business Name</a></li><li><a href="/baby-name-numerology">Baby Name</a></li><li><a href="/love-compatibility-numerology">Love Compatibility</a></li><li><a href="/report">Full Report INR 199/-</a></li></ul></div>
      <div><div class="footer-col-title">Guides</div><ul class="footer-links"><li><a href="/blog/chaldean-numerology-guide">Chaldean Guide</a></li><li><a href="/blog/moolank-meanings">Birth Number Meanings</a></li><li><a href="/blog/personal-year-guide">Personal Year</a></li><li><a href="/blog/name-correction-guide">Name Correction</a></li><li><a href="/blog/compound-numbers-cheiro">Compound Numbers</a></li><li><a href="/blog/lo-shu-grid-guide">Lo Shu Grid</a></li></ul></div>
      <div><div class="footer-col-title">More</div><ul class="footer-links"><li><a href="/blog">All Articles</a></li><li><a href="/about">About</a></li><li><a href="/sitemap-pages">Site Map</a></li><li><a href="/privacy">Privacy</a></li><li><a href="/terms">Terms</a></li><li><a href="/refund">Refund</a></li></ul></div>
    </div>
    <div class="footer-bottom"><span>© 2026 NameAligned.com</span><span>Made with <span style="color:#e8526b;">❤</span> in India</span></div>
  </div>
</footer>'''


def render_page(canon, title, desc, og_desc, h1, hero_glyph, hero_tag, breadcrumb_label, body_html, faq_data, kw):
    article = {"@context":"https://schema.org","@type":"Article","headline":title,"description":desc,"url":canon,"datePublished":"2026-03-01","dateModified":"2026-05-06","author":{"@type":"Organization","name":"NameAligned.com","url":BASE+"/"},"publisher":{"@type":"Organization","name":"NameAligned.com","url":BASE+"/","logo":{"@type":"ImageObject","url":BASE+"/assets/namealigned-logo-full.svg"}},"inLanguage":"en-IN","mainEntityOfPage":{"@type":"WebPage","@id":canon}}
    breadcrumb = {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":BASE+"/"},{"@type":"ListItem","position":2,"name":"Numerology Guides","item":BASE+"/sitemap-pages"},{"@type":"ListItem","position":3,"name":breadcrumb_label,"item":canon}]}
    faq = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faq_data]}

    head = f'''<!DOCTYPE html>
<html lang="en">
<head>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-C1JMQTNHDE"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-C1JMQTNHDE');</script>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<link rel="icon" type="image/svg+xml" href="/assets/namealigned-favicon.svg"/>
<title>{title}</title>
<meta name="description" content="{desc}"/>
<meta name="keywords" content="{kw}"/>
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1"/>
<link rel="canonical" href="{canon}"/>
<link rel="alternate" hreflang="en-IN" href="{canon}"/>
<meta property="og:title" content="{title}"/>
<meta property="og:description" content="{og_desc}"/>
<meta property="og:type" content="article"/>
<meta property="og:url" content="{canon}"/>
<meta property="og:site_name" content="NameAligned.com"/>
<meta property="og:locale" content="en_IN"/>
<meta name="twitter:card" content="summary_large_image"/>
<meta name="twitter:title" content="{title}"/>
<meta name="twitter:description" content="{og_desc}"/>
<script type="application/ld+json">{json.dumps(article, ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(breadcrumb, ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(faq, ensure_ascii=False)}</script>
<link rel="stylesheet" href="assets/style.css"/>
<link rel="stylesheet" href="assets/theme-cosmic-light.css"/>
{CSS_BLOCK}
</head>
<body>
{NAV}
<nav class="crumb" aria-label="Breadcrumb"><a href="/">Home</a> <span style="margin:0 8px;">›</span> <a href="/sitemap-pages">Numerology Guides</a> <span style="margin:0 8px;">›</span> <span style="color:var(--text2);">{breadcrumb_label}</span></nav>
<header class="nn-hero"><div class="container"><div class="badge">Chaldean Numerology</div><div class="glyph">{hero_glyph}</div><h1>{h1}</h1><div class="tag">{hero_tag}</div></div></header>
<main class="nn-body">
{body_html}
</main>
{FOOTER}
</body>
</html>'''
    return head


def build_career(n):
    a = ARCH[n]; c = CAREER[n]
    title = f'Birth Number {n} Career · Best Jobs, Salary Outlook & Work Style ({a["planet"]})'
    desc = f'Birth Number {n} carries {a["planet"]} energy — {a["tag"].lower()}. The careers that work best, the work style that compounds, the salary pattern to expect, and the environments to avoid.'
    og_desc = f'Best careers and work style for Birth Number {n} ({a["planet"]}).'
    canon = f'{BASE}/birth-number-{n}-career'
    breadcrumb = f'Birth Number {n} Career'
    h1 = f'Birth Number {n} Career · Work Style Under {a["planet"]}'

    fields_html = '\n'.join(f'    <li>{x}</li>' for x in c['fields'])
    faq_html = '\n'.join(f'    <details><summary>{q}</summary><p>{ans}</p></details>' for q,ans in c['faq'])
    related = [m for m in [1,2,3,4,5,6,7,8,9] if m != n][:6]
    related_html = '\n'.join(f'    <a href="/birth-number-{m}-career" class="nn-rel-card"><span class="eb">Birth Number {m}</span><span class="ti">{ARCH[m]["planet"]} · Career</span></a>' for m in related)

    body = f'''
  <p>Your <strong>Birth Number</strong> (also known as Moolank in Indian Chaldean numerology) is the single digit your day of birth reduces to. It governs your daily expression — including how you naturally work. For Birth Number {n}, the ruling planet is <strong>{a["planet"]}</strong>, and the work-life signature carries themes of <em>{a["tag"].lower()}</em>.</p>

  <h2>Birth Number {n} work style</h2>
  <p>{c["work_style"]}</p>

  <h2>Best careers for Birth Number {n}</h2>
  <ul>
{fields_html}
  </ul>
  <p>This isn\'t a checklist — many Birth Number {n} people thrive outside these fields. The list captures the natural slope; working against it isn\'t a problem, but takes more conscious adjustment.</p>

  <h2>Salary &amp; income pattern</h2>
  <p>{c["income_pattern"]}</p>

  <h2>Roles to approach with awareness</h2>
  <p>{c["avoid"]}</p>

  <div class="nn-cta-band">
    <h3>What\'s your Birth Number?</h3>
    <p>Free Chaldean analysis — Birth Number, Life Path Number, Name Number and alignment score in 15 seconds.</p>
    <div class="btn-pair">
      <a class="primary" href="/analyzer">Run free analysis →</a>
      <a class="outline" href="/name-numerology-calculator">Name calculator</a>
    </div>
  </div>

  <h2>Frequently asked questions</h2>
  <div class="nn-faq">
{faq_html}
  </div>

  <div class="nn-cta-band">
    <h3>Read more about Birth Number {n}</h3>
    <p>The full Chaldean profile — personality, relationships, lucky attributes and the 5-year forecast — sits in the personalised destiny report.</p>
    <div class="btn-pair">
      <a class="primary" href="/report">Full Destiny Report · INR 199/-</a>
      <a class="outline" href="/life-path-number-{n}-meaning">Life Path Number {n}</a>
    </div>
  </div>

  <h2>Career angles for Birth Numbers 1-9</h2>
  <div class="nn-related-grid">
{related_html}
  </div>
'''
    kw = f'birth number {n} career, birth number {n} jobs, moolank {n} career, life path {n} career, birth number {n} business, {a["planet"].lower()} career'
    return canon, render_page(canon, title, desc, og_desc, h1, a["glyph"], c["work_style"][:120]+"…", breadcrumb, body, c["faq"], kw)


def build_love(n):
    a = ARCH[n]; l = LOVE[n]
    title = f'Life Path Number {n} Love Life · Marriage, Compatibility & Relationship Patterns'
    desc = f'Life Path Number {n} ({a["planet"]}) in love and marriage — partner archetype, compatibility tiers, what you bring to a relationship and what the destiny asks of you.'
    og_desc = f'Life Path {n} love life decoded — compatibility, marriage and relationship patterns.'
    canon = f'{BASE}/life-path-number-{n}-love-life'
    breadcrumb = f'Life Path {n} Love Life'
    h1 = f'Life Path Number {n} in Love · Destiny Under {a["planet"]}'

    faq_html = '\n'.join(f'    <details><summary>{q}</summary><p>{ans}</p></details>' for q,ans in l['faq'])
    related = [m for m in [1,2,3,4,5,6,7,8,9] if m != n][:6]
    related_html = '\n'.join(f'    <a href="/life-path-number-{m}-love-life" class="nn-rel-card"><span class="eb">Life Path {m}</span><span class="ti">{ARCH[m]["planet"]} · Love</span></a>' for m in related)

    body = f'''
  <p>Your <strong>Life Path Number</strong> (in Indian Chaldean numerology, the <em>Bhagyank</em>) is the single digit your full date of birth reduces to. It governs the long-arc themes of your life, including the destiny patterns that play out in love and marriage. For Life Path {n}, the ruling planet is <strong>{a["planet"]}</strong>, and the relationship signature carries themes of <em>{a["tag"].lower()}</em>.</p>

  <h2>The Life Path {n} partner arc</h2>
  <p>{l["partner_arc"]}</p>

  <h2>What you bring to a partnership</h2>
  <p>{l["gives"]}</p>

  <h2>What the destiny asks of you</h2>
  <p>{l["asks"]}</p>

  <h2>Best Life Path matches for {n}</h2>
  <p>{l["best"]}</p>

  <p>Compatibility in Chaldean numerology comes from how the ruling planets of two numbers interact. It isn\'t deterministic — every match works with the right effort — but the strongest matches require less conscious adjustment, and the more challenging ones offer more rapid growth.</p>

  <div class="nn-cta-band">
    <h3>Check Chaldean love compatibility</h3>
    <p>Two birth dates, an instant Chaldean compatibility read — friendly, supportive, neutral or growth-oriented dynamics.</p>
    <div class="btn-pair">
      <a class="primary" href="/love-compatibility-numerology">Run compatibility check →</a>
      <a class="outline" href="/blog/relationship-compatibility-numerology">Read the relationship guide</a>
    </div>
  </div>

  <h2>Frequently asked questions</h2>
  <div class="nn-faq">
{faq_html}
  </div>

  <div class="nn-cta-band">
    <h3>Want the complete Life Path {n} picture?</h3>
    <p>The personalised destiny report covers your destiny themes, name optimisation, 5-year forecast and full compatibility analysis.</p>
    <div class="btn-pair">
      <a class="primary" href="/report">Full Destiny Report · INR 199/-</a>
      <a class="outline" href="/life-path-number-{n}-meaning">Life Path {n} meaning</a>
    </div>
  </div>

  <h2>Love-life angles for Life Paths 1-9</h2>
  <div class="nn-related-grid">
{related_html}
  </div>
'''
    kw = f'life path number {n} love, life path {n} marriage, bhagyank {n} love, destiny number {n} compatibility, life path {n} relationships, {a["planet"].lower()} love life'
    return canon, render_page(canon, title, desc, og_desc, h1, a["glyph"], l["partner_arc"][:140]+"…", breadcrumb, body, l["faq"], kw)


def main():
    for n in range(1, 10):
        canon, html = build_career(n)
        path = os.path.join(OUT, f'birth-number-{n}-career.html')
        open(path, 'w').write(html)

        canon, html = build_love(n)
        path = os.path.join(OUT, f'life-path-number-{n}-love-life.html')
        open(path, 'w').write(html)
    print('wrote 18 pages: 9 birth-number-N-career + 9 life-path-number-N-love-life')


if __name__ == '__main__':
    main()
