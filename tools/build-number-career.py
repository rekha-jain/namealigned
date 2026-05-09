#!/usr/bin/env python3
"""
Generate /number/{n}-career cluster (1-9).

Distinct from /number/{n}-personality (which already has a 5-item career
list) — this page goes deeper: ranked top 10 careers, industries to
AVOID, self-employment business types, launch timing windows, and the
numerological signals that say "pivot now". Targets the commercial-
intent search queries: "best careers for number 8", "what business
suits number 5", "career change numerology", etc.

Run:
    python3 tools/build-number-career.py

Output: number/1-career.html ... number/9-career.html
URLs (cleanUrls): /number/1-career ... /number/9-career
"""
import json, os, re, importlib.util

BASE = 'https://www.namealigned.com'
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, 'number')

# Reuse the shared numbers data (planet, glyph, tagline, etc.).
spec = importlib.util.spec_from_file_location(
    'name_number_pages',
    os.path.join(ROOT, 'tools', 'build-name-number-pages.py')
)
nnm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(nnm)
BASE_NUMBERS = nnm.NUMBERS

# Reuse archetype names from the personality builder so this cluster
# stays linked to the same brand vocabulary.
spec2 = importlib.util.spec_from_file_location(
    'number_cluster',
    os.path.join(ROOT, 'tools', 'build-number-cluster.py')
)
ncm = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(ncm)
ARCHETYPE = {n: ncm.PERSONALITY[n]['archetype'] for n in range(1, 10)}

# Career-specific data, written distinctly per number. Each entry is
# additional content on top of base['career'] (the 5 fields shown on
# the personality page) — top10 has 10 ranked roles with WHY copy,
# avoid lists 3-5 industries, biz_types is for self-employed direction,
# launch_timing is the numerological window, pivot is the signal that
# tells you to switch.
CAREER = {
1:{
  'why':'Sun energy is leadership-shaped — it operates best when the work bears your personal stamp. Number 1 rarely thrives as the seventh person in a team of fifty; it does its best work as the named partner, the founder, the principal, or the public face. The vibration also rewards original thought over received wisdom, which is why Number 1 people often build categories rather than fit into existing ones.',
  'top10':[
    ('Founder / CEO of a category-defining company','Sun rules first-things; the first-mover advantage is built into your numerology'),
    ('Independent professional practice (law, medicine, consulting)','Your judgement is the product; firm-of-one reads as authoritative, not lonely'),
    ('Senior government or political office','Public visibility + decisive authority maps to Sun-ruled vibration'),
    ('Top-of-firm leadership (managing partner, CXO)','You\'re paid for the call you make, not for the work you supervise'),
    ('Independent media / branded creator','The work bears your name and reach is your asset'),
    ('Commodities trading desk lead (gold, oil, energy)','Sun rules gold and energy markets historically'),
    ('Architecture or industrial-design firm principal','Originating the form, not iterating on it'),
    ('Performing arts as a headline act','You\'re the named talent, not part of an ensemble'),
    ('Entrepreneurial education (bootcamps, masterclasses)','Your name becomes the curriculum'),
    ('Strategic advisory to other founders','Sun-ruled people often coach Sun-ruled people best')
  ],
  'avoid':['Pure middle management with no decision authority','Anonymous back-office finance','Sales floors with capped autonomy','Long-cycle research where the credit takes 10 years','Highly bureaucratic government roles below cabinet rank'],
  'biz_types':['Founder-led services firm where your name is the brand','Premium 1-on-1 consultancy','Product company where you remain the public face beyond Series A'],
  'launch_timing':'Sun-ruled best timing: Sundays, dates that reduce to 1 (1st, 10th, 19th, 28th), and the year following your Personal Year 1. Avoid launching anything material on a Saturday in a Personal Year 7.',
  'pivot':'Number 1 should consider a pivot when (a) you\'ve been the third-person at the table for more than two years and (b) your Personal Year shifts to 1 or 5. Both signals together are unusually strong.',
  'pros':'Founders, monarchs, principal partners, signature performing artists and category-defining inventors — Sun-ruled professionals concentrate at the top of structures their work created.',
  'faq':[
    ('What is the best business for Number 1?','One where your name IS the brand. Founder-led professional services, premium consultancies, or product companies where you remain the public face fit Sun-ruled energy best.'),
    ('Should Number 1 quit a salaried job?','Not automatically. The signal is whether your decisions are the deliverable. Salaried roles where you call shots and own outcomes work — salaried roles where you execute someone else\'s vision will quietly drain you.'),
    ('What career suits Number 1 women?','Same answer as men. Sun-ruled energy is leadership-shaped regardless of gender; the cultural framing as masculine is incidental.'),
    ('When should Number 1 launch a business?','In a Personal Year 1, ideally on a Sunday or a date reducing to 1. The first 90 days of any Personal Year 1 carry founding momentum that rarely repeats for nine years.')
  ]
},
2:{
  'why':'Moon energy is relational and emotionally fluent — it does its best work where reading people accurately is the product. Number 2 thrives in fields that reward patience, trust, and the slow arc of relationship-building. The vibration is allergic to high-friction, win-at-all-costs environments where emotional permeability becomes a tax rather than an asset.',
  'top10':[
    ('Therapist / counsellor / clinical psychologist','Reading emotions IS the deliverable; Moon energy is built for it'),
    ('Hospitality founder (boutique hotel, restaurant)','Atmosphere and care become a moat competitors can\'t copy'),
    ('Hospice / palliative care leadership','Holding people at their most vulnerable is what Moon energy does naturally'),
    ('Author or poet','Moon rules the imaginal life; literary work is its native form'),
    ('Music producer / songwriter','Emotional resonance is the product, and you\'re wired to it'),
    ('Residential real estate (homes, not commercial)','Moon rules domestic spaces; commercial leasing is a different planet'),
    ('Family-business steward / succession leader','Patience and relational memory are the assets here'),
    ('UX research lead','Reading users emotionally without their words is Moon-shaped'),
    ('Executive coach for senior leaders','Quiet attunement at the top of organisations'),
    ('Curator (museum, gallery, library)','Caretaker-of-meaning roles fit the vibration')
  ],
  'avoid':['High-volume cold sales','Commercial real estate / leasing','Litigation as a primary practice','Tech-startup growth roles with weekly metrics','Investment banking trading floor'],
  'biz_types':['Boutique therapy or coaching practice','Hospitality (small inn, residential restaurant, retreat)','Independent residential real-estate brokerage'],
  'launch_timing':'Moon-ruled best timing: Mondays, dates reducing to 2 or 7 (2nd, 7th, 11th, 16th, 20th, 25th, 29th), and Personal Year 2. Avoid major launches in Personal Year 9 — that year is for closing chapters, not starting them.',
  'pivot':'Number 2 should consider a pivot when emotional fatigue persists for more than six months despite good rest, or when your Personal Year shifts to 2 — that\'s the diplomacy-and-partnership year that often surfaces a better collaboration than the current one.',
  'pros':'Therapists, hospitality founders, poets, musicians, hospice leaders, and family-business stewards — Moon-ruled professionals concentrate in fields where the deliverable is emotional accuracy.',
  'faq':[
    ('Is Number 2 good for business?','Yes — for the right kind of business. Relationship-led, atmosphere-led, hospitality-led, or care-led businesses do exceptionally well. Volume-and-velocity businesses fight the vibration.'),
    ('What career should Number 2 avoid?','High-volume cold sales, courtroom litigation, and aggressive investment-banking floor roles. The emotional permeability that\'s a creative gift becomes a daily tax in those environments.'),
    ('Is Number 2 too sensitive for leadership?','Permeable, not soft. Moon-ruled leaders pull through patience, rapport and consistency rather than command — which often builds longer-lasting organisations than louder leadership styles.'),
    ('When should Number 2 launch?','In a Personal Year 2, on a Monday, ideally a date reducing to 2 or 7. Co-founder partnerships started in PY 2 tend to outlast those started elsewhere.')
  ]
},
3:{
  'why':'Jupiter energy expands whatever it touches — ideas, audiences, classrooms, conversations. Number 3 thrives in fields that reward verbal articulation and the ability to make complex ideas land warmly. The vibration also rewards generosity with knowledge, which is why teachers, public lecturers, and judges often carry strong Number 3 signatures.',
  'top10':[
    ('Educator (school, university, online cohort-based)','Jupiter literally rules teachers; the vibration is most native here'),
    ('Senior judge or appellate lawyer','Jupiter rules justice; the vibration favours people who weigh rather than fight'),
    ('Religious or spiritual leader','Wisdom-transmission is Jupiter\'s domain'),
    ('Public broadcaster / podcast host','Verbal charisma is your unfair advantage'),
    ('Trade-book author / popular non-fiction','Making hard topics warm is a Number 3 superpower'),
    ('Asset management / wealth advisory','Jupiter rules expansion of resources, including financial'),
    ('Banking (relationship banking, not trading)','Trust + breadth across sectors fits Jupiter'),
    ('Publishing house editor or publisher','Curating what gets amplified'),
    ('Conference organiser / festival director','Convening expansion at scale'),
    ('University fundraiser / development lead','Articulating vision to donors')
  ],
  'avoid':['Solo deep research with zero external audience','Pure operations roles with no narrative work','High-frequency trading','Intelligence services / classified work','Anonymous backend engineering for the long term'],
  'biz_types':['Education / cohort-based course business','Boutique publishing or media','Public-speaking + advisory hybrid practice'],
  'launch_timing':'Jupiter-ruled best timing: Thursdays, dates reducing to 3, 6 or 9 (3rd, 6th, 9th, 12th, 15th, 18th, 21st, 24th, 27th, 30th), and Personal Year 3. Personal Year 3 is your most amplification-friendly year — start the public-facing thing then.',
  'pivot':'Number 3 should consider a pivot when your work has gone fully behind-the-scenes for more than 18 months without your name attached to outcomes, or when your Personal Year shifts to 3 (the natural visibility year).',
  'pros':'Teachers, judges, popular authors, broadcasters, religious leaders, and trusted financial advisors — Jupiter-ruled professionals concentrate in fields where wisdom is transmitted at scale.',
  'faq':[
    ('Is Number 3 good for finance?','Yes for relationship-led wealth advisory, asset management, and senior banking — fields where trust + articulation matter. High-frequency trading and pure quant work fit Mercury (Number 5) better.'),
    ('Should Number 3 do solo work?','Only with an audience attached. Jupiter is amplification — solo work with no public surface tends to feel like underutilisation rather than depth.'),
    ('When should Number 3 launch a course or media business?','In a Personal Year 3, ideally beginning on a Thursday. The 9-month window after a PY 3 starts is unusually warm for content-led launches.'),
    ('Why does Number 3 attract so many opportunities?','Jupiter expands the surface area of whatever you carry. Opportunities multiply because the vibration makes ideas — and the person delivering them — feel bigger than the room.')
  ]
},
4:{
  'why':'Rahu energy is lateral, restless, and pattern-seeing in ways other numbers find disorienting. Number 4 thrives in fields that reward unconventional building — categories that don\'t exist yet, systems that need disruption, or technical work that lateral thinking unlocks. The vibration struggles inside slow, hierarchical, tradition-defending environments.',
  'top10':[
    ('Tech-platform founder / category-creator','Rahu rules new categories; you\'re wired to build them'),
    ('Inventor / patent-holder','Lateral thinking IS the deliverable'),
    ('Aerospace / advanced engineering','Unconventional precision'),
    ('Forensic accountant / fraud investigator','Seeing what\'s hidden in plain sight is Rahu\'s gift'),
    ('Cryptography / cybersecurity research','Outsider thinking is the moat'),
    ('Investigative journalist / documentary maker','Surfacing what others avoid naming'),
    ('Renewable / alternative energy founder','New paradigms in old industries'),
    ('Product designer at a contrarian company','Vision over consensus'),
    ('Independent strategy consultant','Selling lateral angles to executives stuck in linear ones'),
    ('Architect of unconventional structures (biophilic, modular)','Form beyond the templates')
  ],
  'avoid':['Government bureaucracy below senior leadership','Traditional family-run firms with strong succession rules','Long-tenure academic departments resistant to new methods','Religious or institutional leadership in deeply orthodox systems','Pure compliance roles where deviation is penalised'],
  'biz_types':['Tech platform with a contrarian founding insight','Independent investigation / forensic practice','Renewable / alternative-energy venture'],
  'launch_timing':'Rahu-ruled best timing: Sundays and Saturdays (Rahu echoes both Sun and Saturn axes), dates reducing to 4 or 8 (4th, 8th, 13th, 17th, 22nd, 26th, 31st), and Personal Years 4 or 8. Avoid public launches in Personal Year 2 — it dilutes Rahu\'s edge.',
  'pivot':'Number 4 should consider a pivot when restlessness spikes alongside a sense that the current category is closed to new thinking. Personal Year 4 is the structure-building year; Personal Year 5 is the fast-pivot year. Both can be exit signals depending on which way the restlessness points.',
  'pros':'Inventors, contrarian founders, forensic specialists, investigative journalists and architects of unconventional systems — Rahu-ruled professionals concentrate in fields where seeing differently is the unfair advantage.',
  'faq':[
    ('Is Number 4 unlucky for career?','That\'s a misconception. Rahu energy is unconventional and intense — it asks for the right environment, not avoidance. In tech, alternative energy, forensic work and lateral creative fields, Number 4 outperforms.'),
    ('What business suits Number 4?','One built on a contrarian insight. Rahu-ruled businesses do best when they\'re creating a new category rather than competing inside an old one.'),
    ('Should Number 4 work in tradition-bound institutions?','Generally only at senior levels where the institution itself is willing to change. Lower-rank tradition-defending roles consistently feel like compression.'),
    ('When should Number 4 pivot?','In Personal Year 5 (the fast-pivot year) or when restlessness has lasted 9+ months in a closed category. Rahu rewards the bold move when it\'s aimed at a new paradigm, not a sideways step.')
  ]
},
5:{
  'why':'Mercury energy is fast, information-fluent and pivot-comfortable — it thrives where speed of synthesis is the deliverable. Number 5 does its best work in fields that reward quick context-switching and turning information into leverage. The vibration is allergic to slow, single-domain mastery roles where finishing matters more than improvising.',
  'top10':[
    ('Trader (equities, derivatives, FX)','Mercury rules trading floors; speed and information are the product'),
    ('Journalist (news desk, breaking-story specialist)','Information-into-narrative on tight cycles'),
    ('Multi-hyphenate creator (writer + speaker + investor)','Mercury rules portfolio careers'),
    ('Tech-startup founder in fast-moving consumer','Pivots are part of the design, not the failure'),
    ('Marketing / growth lead at a Series A-C company','Speed of test-iterate-scale fits the vibration'),
    ('Stand-up or sketch comedian','Mercury rules verbal speed and timing'),
    ('Sales (consultative, complex products)','Pattern-matching customer needs in real time'),
    ('Travel writer / cross-cultural broker','Movement IS the work'),
    ('Diplomat / international relations','Information-as-leverage between contexts'),
    ('Stock analyst / financial journalist','Synthesising fast on public data')
  ],
  'avoid':['Solo, slow, decade-long research','Heavy-industry operations','Long-arc apprenticeship trades','Slow-moving family business succession','Roles measured in 5-year deliverables'],
  'biz_types':['Trading or active-investment practice','Multi-hyphenate creator brand (newsletter + advisory + product)','Fast-cycle consumer-tech startup'],
  'launch_timing':'Mercury-ruled best timing: Wednesdays, dates reducing to 5 (5th, 14th, 23rd), and Personal Year 5. PY 5 is your pivot year — the launches that feel destined often fail in PY 4 (too rigid) but succeed in PY 5.',
  'pivot':'Number 5 should consider a pivot when boredom is the dominant signal for 6+ months — Mercury reads sustained boredom as a directive. PY 5 is the natural switching year; ignoring it tends to compound restlessness into impulsive moves later.',
  'pros':'Traders, journalists, comedians, multi-hyphenate creators, sales leaders, and tech founders in fast-moving categories — Mercury-ruled professionals concentrate in fields where speed of synthesis is the moat.',
  'faq':[
    ('What business is best for Number 5?','One where pivoting is a feature, not a bug. Trading, fast-cycle tech, multi-hyphenate creator brands, and active-management financial practices fit Mercury energy best.'),
    ('Should Number 5 commit to one career?','One direction, many shapes. Mercury thrives with a stable theme (e.g. "information") expressed through several roles over a decade — versus a single role held for two decades.'),
    ('When should Number 5 launch?','In Personal Year 5, on a Wednesday. PY 5 launches with a pivot built in tend to outlast PY 5 launches positioned as permanent commitments.'),
    ('Is Number 5 good for stable jobs?','Stable in theme, not stable in shape. Long tenure in a single role tends to feel like compression by year four; lateral movement within a domain works much better.')
  ]
},
6:{
  'why':'Venus energy creates atmosphere — beauty, ease, care, aesthetic sensibility — and Number 6 thrives in fields where the environment IS the product. The vibration does best in design, hospitality, education-of-children, fine arts, and relationship-led businesses where warmth becomes the moat.',
  'top10':[
    ('Designer (interior, product, brand)','Venus rules aesthetics; design is its native form'),
    ('Hospitality / boutique hotel founder','The room IS the deliverable'),
    ('Restaurant / café owner','Atmosphere + warmth + taste'),
    ('Wedding / event planner','Beauty + emotional choreography'),
    ('Early-childhood educator','Venus rules nurture; this work is its purest form'),
    ('Family-therapy specialist','Relationship-as-product'),
    ('Fine artist / sculptor / craft specialist','Visual harmony work'),
    ('Cosmetics / beauty industry founder','Direct Venus alignment'),
    ('Florist / botanical-arts entrepreneur','Aesthetic + nature'),
    ('Gallery / curated retail owner','Curation as art')
  ],
  'avoid':['Hard-charging cold sales','Mining, demolition, heavy industry','Litigation','High-frequency trading','Adversarial procurement / negotiation roles'],
  'biz_types':['Design studio (boutique, founder-led)','Hospitality (restaurant, hotel, event company)','Beauty / wellness / lifestyle brand'],
  'launch_timing':'Venus-ruled best timing: Fridays, dates reducing to 6 (6th, 15th, 24th), and Personal Year 6. PY 6 is the relationship-and-home year — launches positioned around community and beauty resonate strongest then.',
  'pivot':'Number 6 should consider a pivot when the current role offers no aesthetic agency — when you can\'t shape the environment, only execute inside it. PY 6 is the natural relationship-and-home year, often surfacing a more values-aligned offer.',
  'pros':'Designers, hoteliers, restaurateurs, fine artists, family therapists, and curators — Venus-ruled professionals concentrate in fields where the made world feels like home.',
  'faq':[
    ('Is Number 6 good for business?','Outstanding for design, hospitality, beauty and lifestyle. The Venus moat — atmosphere — is hard for competitors to copy.'),
    ('Should Number 6 do high-pressure work?','High-stakes, yes; high-friction, no. Venus thrives where pressure is creative; it suffers where pressure is adversarial.'),
    ('What jobs should Number 6 avoid?','Adversarial roles where someone has to lose for you to win — hard sales, litigation, demolition, hostile-takeover finance. The Venus vibration becomes the hostage.'),
    ('When should Number 6 launch a brand?','In Personal Year 6, on a Friday, ideally a date reducing to 6. PY 6 launches that lean into beauty and community tend to compound for years.')
  ]
},
7:{
  'why':'Ketu energy is inward, research-driven, and rewards depth over breadth. Number 7 thrives in fields where going deep into one subject for years IS the work. The vibration is allergic to surface-level commercial hustle, fast-pivot environments, and roles measured in weekly metrics — those fields read as hollow within months.',
  'top10':[
    ('Research scientist / PI of a long-arc lab','Depth-over-breadth is the entire deliverable'),
    ('Theologian / religious scholar','Ketu rules contemplative work'),
    ('Investigative book author / long-form journalist','Multi-year reporting projects'),
    ('Mystic / spiritual teacher','Inner work as the visible work'),
    ('Astrology / numerology / occult-systems specialist','Native territory'),
    ('Cinematographer / contemplative documentary filmmaker','Quiet observation at scale'),
    ('Forensic pathologist / niche medical specialist','Deep single-domain mastery'),
    ('Long-form podcast host (philosophical interviews)','Depth in conversation'),
    ('Library / archive director','Custodianship of accumulated meaning'),
    ('Solo philosopher / essayist','Thought as the work')
  ],
  'avoid':['High-volume retail sales','Fast-cycle consumer marketing','Trading floor / day-trading','Network-effect social-media careers','Roles where weekly output is the deliverable'],
  'biz_types':['Research-led consultancy (one-domain mastery)','Long-form publishing (books, multi-year podcast)','Specialist clinical or contemplative practice'],
  'launch_timing':'Ketu-ruled best timing: Mondays and Sundays, dates reducing to 7 (7th, 16th, 25th), and Personal Year 7. PY 7 is the inward year — quiet, research-led launches in PY 7 outperform loud ones every cycle.',
  'pivot':'Number 7 should consider a pivot when the current role offers no depth — when output is rewarded over insight. PY 7 is the natural inward year, often surfacing the question "what work would I do if no one applauded?"',
  'pros':'Researchers, theologians, mystics, contemplative writers, cinematographers, forensic specialists, and quiet polymath authors — Ketu-ruled professionals concentrate in fields where depth and originality compound over decades.',
  'faq':[
    ('Is Number 7 bad for business?','Bad for fast commercial hustle; excellent for research-led specialist practices. The vibration\'s edge is depth — businesses that monetise depth do unusually well.'),
    ('Should Number 7 work alone?','Often yes. Ketu regenerates in solitude; co-working environments tend to drain the vibration unless solitude is actively protected within them.'),
    ('What jobs should Number 7 avoid?','High-volume sales, fast-cycle marketing, day-trading, and social-media network-effect careers. The vibration\'s gift is depth — surface-level work corrodes it.'),
    ('When should Number 7 launch a research practice?','In Personal Year 7, on a Monday. Quiet, narrow, deep launches in PY 7 reliably outperform broad commercial launches in the same year.')
  ]
},
8:{
  'why':'Saturn energy is structural, patient, and rewards endurance — Number 8 thrives in fields where authority compounds over decades rather than years. The vibration is exceptional in finance, law, real estate, infrastructure, and any field where the value of your judgement increases with time on the job.',
  'top10':[
    ('Senior partner at a law firm','Saturn rules law; long-tenure authority is built in'),
    ('Central / commercial banker','Compounding institutional trust'),
    ('Real-estate developer (long-cycle projects)','Saturn rules earth and structure'),
    ('Heavy industry / infrastructure CEO','Long-arc delivery is your home'),
    ('Judge or appellate court bench','Authority-by-time-served is the qualification'),
    ('Accountant / auditor (Big 4 partner track)','Patience and structural thinking'),
    ('Mining / commodities executive','Saturn-ruled physical assets'),
    ('Family-office or wealth-preservation specialist','Multi-decade thinking'),
    ('Government cabinet / civil service senior leader','Slow-built public authority'),
    ('Insurance / actuarial leadership','Discipline and long-arc probability')
  ],
  'avoid':['Fast-fashion / weekly-trend retail','Day-trading','Stand-up comedy as a primary career','Influencer / social-media-led careers','Roles measured in 90-day OKRs'],
  'biz_types':['Long-cycle real-estate or infrastructure venture','Family-office or wealth-preservation practice','Specialist law / compliance / regulatory firm'],
  'launch_timing':'Saturn-ruled best timing: Saturdays, dates reducing to 8 (8th, 17th, 26th), and Personal Year 8. PY 8 is the authority-and-money year — material moves made in PY 8 with patience tend to anchor for decades.',
  'pivot':'Number 8 should consider a pivot when the current path offers no compounding — when years of effort don\'t accumulate into authority or assets. PY 8 is the natural recompounding year; PY 4 is the restructuring year.',
  'pros':'Long-game founders, senior partners, central bankers, judges, real-estate developers, and infrastructure leaders — Saturn-ruled professionals concentrate in fields where authority compounds invisibly until it becomes unmistakable.',
  'faq':[
    ('Is Number 8 good for business?','Excellent — particularly long-cycle businesses (real estate, finance, infrastructure, law). Less suited to fast-moving consumer or trend-driven markets.'),
    ('Why does Number 8 feel slow?','Saturn\'s curriculum is patience. The pace isn\'t a flaw — it\'s the engine. Used well, the eventual authority is rare and lasting.'),
    ('Should Number 8 take risky bets?','Calculated, structural ones — yes. Speculative, fast-flip ones — no. Saturn rewards patience priced into the bet.'),
    ('When should Number 8 launch?','In Personal Year 8, on a Saturday, ideally a date reducing to 8. PY 8 launches anchored in long-cycle thinking compound for years past their starting points.')
  ]
},
9:{
  'why':'Mars energy is decisive, courageous, and protective — Number 9 thrives in fields that reward moving first under pressure. The vibration does its best work in defense, surgery, sports, activism, and any field where someone has to act before the situation is fully understood.',
  'top10':[
    ('Surgeon / emergency physician','Mars rules cutting-and-decisive medicine'),
    ('Military / defence leadership','Native Mars territory'),
    ('Professional athlete / coach','Physical decisiveness as the job'),
    ('Politician (campaign-led, decisive)','Mars rules political will'),
    ('Activist / NGO founder','Cause-led courage'),
    ('Trauma therapist / first responder','Holding ground under pressure'),
    ('Firefighter / search-and-rescue leader','Physical courage as the deliverable'),
    ('Trial lawyer (criminal defence, prosecution)','Combat-shaped advocacy'),
    ('Sports-medicine specialist','Physical performance optimisation'),
    ('Sales-leadership in high-stakes B2B','Decisive close-the-deal energy')
  ],
  'avoid':['Slow consensus-building academic roles','Long-tenure family-business succession','Hospitality at scale','Mediation / dispute-resolution as primary practice','Curatorial / archival work'],
  'biz_types':['Specialist surgical or emergency medical practice','Defence / security consulting','Cause-led activist organisation or campaign'],
  'launch_timing':'Mars-ruled best timing: Tuesdays, dates reducing to 9 (9th, 18th, 27th), and Personal Year 9. PY 9 is the closing-and-launching-the-next-cycle year — the launches that survive PY 9 tend to be the right ones.',
  'pivot':'Number 9 should consider a pivot when the current role doesn\'t require courage — when you\'re using maintenance energy where action energy is wired in. PY 9 is the natural cycle-closing year, often surfacing the next courage-shaped move.',
  'pros':'Surgeons, soldiers, athletes, activists, trial lawyers, first responders and decisive political leaders — Mars-ruled professionals concentrate in fields where moving first under pressure is the entire deliverable.',
  'faq':[
    ('Is Number 9 too aggressive for business?','Energetic, not aggressive. Mars is courage and protection; channeled correctly it builds decisive organisations. Channeled poorly it burns the team out.'),
    ('What business suits Number 9?','Specialist surgical / emergency medical practice, defence consulting, cause-led activist organisations, and elite sports performance — fields where decisive action is the product.'),
    ('Should Number 9 work in slow industries?','Generally only at senior levels where you can drive pace. Lower ranks in slow industries tend to feel like compression by year three.'),
    ('When should Number 9 launch?','In Personal Year 9, on a Tuesday. PY 9 launches that emerge from genuine cycle-closing energy outlast PY 9 launches that are reactive starts.')
  ]
}
}


HEAD = '''<!DOCTYPE html>
<html lang="en">
<head>
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-C1JMQTNHDE"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', 'G-C1JMQTNHDE');
</script>

<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<link rel="icon" type="image/svg+xml" href="/assets/namealigned-favicon.svg"/>
<title>{title}</title>
<meta name="description" content="{desc}"/>
<meta name="keywords" content="best careers for number {n}, number {n} career, number {n} business, number {n} {planet_lower} career, career numerology number {n}, number {n} job suggestions"/>
<meta name="author" content="NameAligned.com"/>
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1"/>
<link rel="canonical" href="{canon}"/>
<link rel="alternate" hreflang="en-IN" href="{canon}"/>
<meta property="og:title" content="{og_title}"/>
<meta property="og:description" content="{og_desc}"/>
<meta property="og:type" content="article"/>
<meta property="og:url" content="{canon}"/>
<meta property="og:site_name" content="NameAligned.com"/>
<meta property="og:locale" content="en_IN"/>
<meta property="og:image" content="{base}/assets/og/moolank-{n}.png"/>
<meta name="twitter:card" content="summary_large_image"/>
<meta name="twitter:title" content="{og_title}"/>
<meta name="twitter:description" content="{og_desc}"/>
<meta name="twitter:image" content="{base}/assets/og/moolank-{n}.png"/>

<script type="application/ld+json">
{article_json}
</script>
<script type="application/ld+json">
{breadcrumb_json}
</script>
<script type="application/ld+json">
{faq_json}
</script>

<link rel="stylesheet" href="/assets/style.css"/>
<link rel="stylesheet" href="/assets/theme-cosmic-light.css"/>
<style>
.nc-hero{{padding:3rem 0 1.5rem;text-align:center;background:linear-gradient(160deg,#1a1340 0%,#2a1a5c 100%);color:#f0ece0;}}
.nc-hero .badge{{display:inline-block;font-family:sans-serif;font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:#f0b429;background:rgba(240,180,41,.12);padding:5px 14px;border-radius:20px;border:1px solid rgba(240,180,41,.35);margin-bottom:1rem;}}
.nc-hero h1{{font-family:'Playfair Display',Georgia,serif;font-size:clamp(28px,4.2vw,42px);line-height:1.2;margin:0 auto .5rem;max-width:780px;color:#f0ece0!important;}}
.nc-hero h2{{color:#f0ece0!important;}}
.nc-hero .glyph{{font-size:42px;color:#f0b429;line-height:1;margin-bottom:.5rem;}}
.nc-hero .tag{{font-family:sans-serif;font-size:14px;color:rgba(240,236,224,.78);letter-spacing:.06em;}}
.nc-tldr{{max-width:780px;margin:1.25rem auto 0;padding:1.1rem 1.4rem;background:rgba(0,0,0,.28);border:1px solid rgba(240,180,41,.42);border-radius:12px;font-family:sans-serif;font-size:14px;line-height:1.65;color:#f0ece0;backdrop-filter:blur(6px);}}
.nc-tldr strong{{color:#f0b429;}}
.nc-body{{max-width:780px;margin:0 auto;padding:2rem 1.25rem;}}
.nc-body h2{{font-family:'Playfair Display',Georgia,serif;font-size:23px;color:var(--text);margin:1.85rem 0 .55rem;line-height:1.25;}}
.nc-body h3{{font-family:'Playfair Display',Georgia,serif;font-size:17px;color:var(--text);margin:1.4rem 0 .45rem;}}
.nc-body p{{font-family:sans-serif;font-size:14.5px;line-height:1.75;color:var(--text);margin-bottom:.85rem;}}
.nc-body ul{{font-family:sans-serif;font-size:14px;line-height:1.85;color:var(--text);padding-left:1.25rem;margin-bottom:1rem;}}
.nc-body li{{margin-bottom:.35rem;}}
.nc-top10{{list-style:none;padding:0;margin:.75rem 0 1.25rem;counter-reset:rank;}}
.nc-top10 li{{position:relative;padding:.65rem .85rem .65rem 2.5rem;background:var(--card);border:1px solid var(--gold-b);border-radius:10px;margin-bottom:.45rem;font-family:sans-serif;font-size:14px;line-height:1.6;counter-increment:rank;}}
.nc-top10 li::before{{content:counter(rank);position:absolute;left:.7rem;top:.65rem;width:22px;height:22px;background:linear-gradient(135deg,#f0b429,#f5d060);color:#0a0820;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:11.5px;font-family:Georgia,serif;}}
.nc-top10 .role{{font-weight:700;color:var(--text);display:block;margin-bottom:2px;}}
.nc-top10 .why{{color:var(--text2);font-size:13px;}}
.nc-cta-band{{background:var(--gold-l);border:1.5px solid var(--gold-b);border-radius:14px;padding:1.4rem;margin:1.75rem 0;text-align:center;}}
.nc-cta-band h3{{margin:0 0 .35rem;font-family:Georgia,serif;font-size:18px;color:var(--text);}}
.nc-cta-band p{{margin:0 0 .85rem;font-size:13.5px;color:var(--text2);font-family:sans-serif;}}
.nc-cta-band .btn-pair{{display:flex;gap:.6rem;justify-content:center;flex-wrap:wrap;}}
.nc-cta-band a{{display:inline-block;font-family:sans-serif;font-size:13.5px;font-weight:600;padding:9px 18px;border-radius:8px;text-decoration:none;}}
.nc-cta-band a.primary{{background:var(--gold);color:#0a0820;}}
.nc-cta-band a.primary:hover{{background:#f5c247;}}
.nc-cta-band a.outline{{background:transparent;color:var(--text);border:1.5px solid var(--gold-b);}}
.nc-faq{{margin:1.75rem 0;}}
.nc-faq details{{background:var(--card);border:1px solid var(--gold-b);border-radius:10px;padding:.8rem 1.1rem;margin-bottom:.55rem;}}
.nc-faq summary{{font-family:Georgia,serif;font-size:14.5px;font-weight:700;color:var(--text);cursor:pointer;line-height:1.4;}}
.nc-faq details[open] summary{{margin-bottom:.45rem;}}
.nc-faq details p{{font-family:sans-serif;font-size:13.5px;line-height:1.7;color:var(--text2);margin:0;}}
.nc-related{{margin:1.75rem 0;}}
.nc-related-grid{{display:grid;grid-template-columns:repeat(2,1fr);gap:.75rem;}}
@media(max-width:640px){{.nc-related-grid{{grid-template-columns:1fr;}}}}
.nc-rel-card{{display:flex;flex-direction:column;background:var(--card);border:1px solid var(--gold-b);border-radius:10px;padding:.85rem 1rem;text-decoration:none;color:var(--text);transition:transform .15s ease,box-shadow .15s ease;}}
.nc-rel-card:hover{{transform:translateY(-2px);box-shadow:0 6px 20px rgba(201,162,39,.12);}}
.nc-rel-card .eb{{font-family:sans-serif;font-size:9.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--gold-d);font-weight:700;margin-bottom:.2rem;}}
.nc-rel-card .ti{{font-family:Georgia,serif;font-size:14px;font-weight:700;line-height:1.3;}}
nav.crumb{{font-family:sans-serif;font-size:12px;color:var(--text3);padding:1rem 1.25rem 0;max-width:780px;margin:0 auto;}}
nav.crumb a{{color:var(--text3);text-decoration:none;}}
</style>
</head>
<body>'''


NAV = '''
<nav class="nav">
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
</nav>
'''

FOOTER = '''
<footer class="footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <div class="footer-brand"><span class="logo-moon">☽</span> NameAligned.com</div>
        <p class="footer-tagline">Free Chaldean numerology analysis for everyone. Based on Cheiro\'s Book of Numbers, the oldest and most accurate system.</p>
        <div style="margin-top:1.5rem;display:flex;gap:10px">
          <a href="/analyzer" style="font-size:12px;font-family:sans-serif;color:var(--gold);border:1px solid rgba(240,180,41,.35);border-radius:20px;padding:5px 14px;text-decoration:none;transition:all .2s" onmouseover="this.style.background='rgba(240,180,41,.12)'" onmouseout="this.style.background='transparent'">Try free →</a>
          <a href="/report" style="font-size:12px;font-family:sans-serif;color:rgba(157,127,255,.8);border:1px solid rgba(157,127,255,.3);border-radius:20px;padding:5px 14px;text-decoration:none;transition:all .2s" onmouseover="this.style.background='rgba(157,127,255,.10)'" onmouseout="this.style.background='transparent'">Full report · ₹499 / $5</a>
        </div>
      </div>
      <div>
        <div class="footer-col-title">Free Tools</div>
        <ul class="footer-links">
          <li><a href="/name-numerology-calculator">Name Numerology Calculator</a></li>
          <li><a href="/name-correction-numerology">Name Correction Check</a></li>
          <li><a href="/business-name-numerology">Business Name Check</a></li>
          <li><a href="/love-compatibility-numerology">Love Compatibility</a></li>
          <li><a href="/report">Full Destiny Report · ₹499 / $5</a></li>
          <li><a href="/ask-aura">✦ Ask Aura · Conversational</a></li>
        </ul>
      </div>
      <div>
        <div class="footer-col-title">Guides</div>
        <ul class="footer-links">
          <li><a href="/blog/chaldean-numerology-guide">Chaldean Guide</a></li>
          <li><a href="/blog/moolank-meanings">Birth Number Meanings</a></li>
          <li><a href="/blog/personal-year-guide">Personal Year Guide</a></li>
          <li><a href="/blog/name-correction-guide">Name Correction Guide</a></li>
          <li><a href="/blog/compound-numbers-cheiro">Compound Numbers</a></li>
          <li><a href="/blog/lo-shu-grid-guide">Lo Shu Grid</a></li>
        </ul>
      </div>
      <div>
        <div class="footer-col-title">More</div>
        <ul class="footer-links">
          <li><a href="/blog">All Articles</a></li>
          <li><a href="/about">About</a></li>
          <li><a href="/sitemap-pages">Site Map</a></li>
          <li><a href="/privacy">Privacy</a></li>
          <li><a href="/terms">Terms</a></li>
          <li><a href="/refund">Refund</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© 2026 NameAligned.com · For entertainment &amp; self-reflection purposes</span>
      <span>Made with <span style="color:#e8526b;">❤</span> in India · 🔒 Secured by <strong style="color:#9d7fff;">Razorpay</strong></span>
    </div>
  </div>
</footer>
</body>
</html>
'''


def render(n):
    base = BASE_NUMBERS[n]
    c = CAREER[n]
    planet = base['planet']
    glyph = base['glyph']
    archetype = ARCHETYPE[n]

    title = f'Best Careers for Number {n} — Top 10 Profession Matches'
    og_title = f'Number {n} Careers: 10 fields where {planet} energy compounds'
    desc = f'Best careers for Number {n} in Chaldean numerology — top 10 ranked roles, industries to avoid, business types for self-employment, lucky launch timing and when to pivot careers under {planet} energy.'
    og_desc = f'Top 10 careers for Number {n} ({planet}) — plus what to avoid, the best self-employment shapes and ideal launch windows.'
    canon = f'{BASE}/number/{n}-career'

    article = {
        '@context':'https://schema.org','@type':'Article','headline':title,
        'description':desc,'url':canon,'datePublished':'2026-05-08','dateModified':'2026-05-08',
        'author':{'@type':'Organization','name':'NameAligned.com','url':BASE+'/'},
        'publisher':{'@type':'Organization','name':'NameAligned.com','url':BASE+'/','logo':{'@type':'ImageObject','url':BASE+'/assets/namealigned-logo-full.svg'}},
        'inLanguage':'en-IN','mainEntityOfPage':{'@type':'WebPage','@id':canon},
        'about':[
            {'@type':'DefinedTerm','name':f'Number {n}','inDefinedTermSet':'Chaldean Numerology'},
            {'@type':'DefinedTerm','name':planet,'inDefinedTermSet':'Ruling Planets'},
            {'@type':'DefinedTerm','name':'Career Numerology','inDefinedTermSet':'Numerology Concepts'}
        ]
    }
    breadcrumb = {'@context':'https://schema.org','@type':'BreadcrumbList','itemListElement':[
        {'@type':'ListItem','position':1,'name':'Home','item':BASE+'/'},
        {'@type':'ListItem','position':2,'name':'Numbers','item':BASE+'/sitemap-pages'},
        {'@type':'ListItem','position':3,'name':f'Number {n} Career','item':canon}
    ]}
    faq = {'@context':'https://schema.org','@type':'FAQPage','mainEntity':[
        {'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for q,a in c['faq']
    ]}

    head = HEAD.format(
        n=n, title=title, og_title=og_title, desc=desc, og_desc=og_desc, canon=canon, base=BASE,
        planet_lower=planet.lower(),
        article_json=json.dumps(article, ensure_ascii=False),
        breadcrumb_json=json.dumps(breadcrumb, ensure_ascii=False),
        faq_json=json.dumps(faq, ensure_ascii=False),
    )

    top10_html = '\n'.join(
        f'    <li><span class="role">{role}</span><span class="why">{why}</span></li>'
        for role, why in c['top10']
    )
    avoid_html = '\n'.join(f'    <li>{x}</li>' for x in c['avoid'])
    biz_html = '\n'.join(f'    <li>{x}</li>' for x in c['biz_types'])
    faq_html = '\n'.join(f'    <details><summary>{q}</summary><p>{a}</p></details>' for q, a in c['faq'])

    related = [m for m in [1,2,3,4,5,6,7,8,9] if m != n][:6]
    related_html = '\n'.join(
        f'    <a href="/number/{m}-career" class="nc-rel-card"><span class="eb">Number {m} · {BASE_NUMBERS[m]["planet"]}</span><span class="ti">Best careers — {ARCHETYPE[m]}</span></a>'
        for m in related
    )

    tldr = f'Number {n} in Chaldean numerology is {planet}-ruled — career fields where {planet}\'s rhythm compounds tend to outperform fields that fight it. The top 10 roles below are ranked by how natively the work fits {planet} energy, plus a list of industries to avoid, the best shapes for self-employment, and the numerological windows that say "launch now" or "pivot now".'

    body = f'''
{NAV}

<nav class="crumb" aria-label="Breadcrumb">
  <a href="/">Home</a> <span style="margin:0 8px;">›</span>
  <a href="/sitemap-pages">Numbers</a> <span style="margin:0 8px;">›</span>
  <span style="color:var(--text2);">Number {n} Career</span>
</nav>

<header class="nc-hero">
  <div class="container">
    <div class="badge">Career Numerology · Number {n}</div>
    <div class="glyph">{glyph}</div>
    <h1>Best Careers for Number {n} — {archetype}</h1>
    <div class="tag">{base["tagline"]}</div>
  </div>
  <div class="nc-tldr"><strong>In short.</strong> {tldr}</div>
</header>

<main class="nc-body">

  <h2>Why Number {n} fits these careers</h2>
  <p>{c["why"]}</p>

  <h2>Top 10 careers for Number {n}, ranked</h2>
  <ol class="nc-top10">
{top10_html}
  </ol>

  <h2>Industries Number {n} should avoid</h2>
  <p>The vibration\'s strengths become liabilities in environments shaped against them. Number {n} people consistently report compression, drain or stalled growth in:</p>
  <ul>
{avoid_html}
  </ul>
  <p>This isn\'t a hard prohibition — many people make these careers work — but the energy budget required is high enough that most never reach the authority they would have in a better-aligned field.</p>

  <h2>Best business types if Number {n} goes self-employed</h2>
  <ul>
{biz_html}
  </ul>

  <h2>Lucky launch timing for Number {n}</h2>
  <p>{c["launch_timing"]}</p>

  <div class="nc-cta-band">
    <h3>Find your exact numbers in 15 seconds</h3>
    <p>Free Chaldean calculator — Birth Number, Life Path Number and Name Number, side by side. The combination, not any single digit, drives career fit.</p>
    <div class="btn-pair">
      <a class="primary" href="/name-numerology-calculator">Calculate my numbers →</a>
      <a class="outline" href="/analyzer">Full free analysis</a>
    </div>
  </div>

  <h2>Famous Number {n} professionals</h2>
  <p>{c["pros"]}</p>

  <h2>When to pivot careers under Number {n}</h2>
  <p>{c["pivot"]}</p>

  <h2>Frequently asked questions</h2>
  <div class="nc-faq">
{faq_html}
  </div>

  <div class="nc-cta-band">
    <h3>Want the full picture for your career?</h3>
    <p>The Full Destiny Report covers your specific Number {n} placement (Birth, Life Path or Name), the planetary windows for the next 5 years, the industries your chart actively pulls toward, and the months most favourable for a career launch or pivot.</p>
    <div class="btn-pair">
      <a class="primary" href="/report">Full Destiny Report · ₹499 / $5 USD</a>
      <a class="outline" href="/number/{n}-personality">Number {n} personality</a>
    </div>
  </div>

  <h2>Related: Number {n} on every chart</h2>
  <ul>
    <li><a href="/number/{n}-personality">Number {n} personality</a> — the archetype across the whole chart</li>
    <li><a href="/name-number-{n}-meaning">Name Number {n} meaning</a> — what the name does</li>
    <li><a href="/life-path-number-{n}-meaning">Life Path Number {n} meaning</a> — the soul curriculum</li>
  </ul>

  <h2>Other number careers</h2>
  <div class="nc-related">
    <div class="nc-related-grid">
{related_html}
    </div>
  </div>

</main>

{FOOTER}
'''
    return head + body


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    for n in range(1, 10):
        out = os.path.join(OUT_DIR, f'{n}-career.html')
        html = render(n)
        with open(out, 'w') as f:
            f.write(html)
        words = len(re.findall(r'\b\w+\b', html))
        print(f'wrote number/{n}-career.html (~{words} words including markup)')


if __name__ == '__main__':
    main()
