import fs from 'node:fs';
import path from 'node:path';
import { JSDOM } from 'jsdom';

const ROOT = path.resolve(new URL('..', import.meta.url).pathname);

const planets = {
  1: ['Sun', 'leadership, visibility, and self-direction'],
  2: ['Moon', 'sensitivity, intuition, and emotional rhythm'],
  3: ['Jupiter', 'expression, learning, and social warmth'],
  4: ['Rahu', 'restlessness, originality, and systems thinking'],
  5: ['Mercury', 'adaptability, communication, and quick decisions'],
  6: ['Venus', 'harmony, love, and aesthetic intelligence'],
  7: ['Ketu', 'depth, intuition, and solitary insight'],
  8: ['Saturn', 'discipline, endurance, and long-term authority'],
  9: ['Mars', 'courage, protection, and decisive action'],
};

const blogSnippets = {
  '/blog/chaldean-numerology-guide': ['Chaldean Numerology Guide: Numbers, Names, Meaning', 'Learn Chaldean numerology through name numbers, birth numbers, compound numbers, planetary meanings, and practical examples for real charts.'],
  '/blog/chaldean-vs-pythagorean-numerology': ['Chaldean vs Pythagorean Numerology: Key Differences', 'Compare Chaldean and Pythagorean numerology, including letter values, name readings, cultural use, accuracy claims, and when each system fits.'],
  '/blog/compound-numbers-cheiro': ['Compound Numbers in Cheiro Numerology: 10-52 Guide', 'Understand Cheiro compound numbers from 10 to 52 before reduction, including symbolism, warnings, strengths, and name-number interpretation.'],
  '/blog/how-numerology-works-for-names': ['How Numerology Works for Names in Chaldean Method', 'See how Chaldean numerology converts letters into numbers, reads compound totals, and interprets how a name vibration meets a birth date.'],
  '/blog/how-to-choose-lucky-name': ['How to Choose a Lucky Name Using Numerology', 'A practical guide to choosing a lucky name with Chaldean numerology, including name number, compound vibration, birth number harmony, and fit.'],
  '/blog/is-name-correction-effective': ['Is Name Correction Effective in Numerology?', 'Understand when name correction can help, what it cannot promise, and how Chaldean numerology evaluates spelling, vibration, and alignment.'],
  '/blog/lo-shu-grid-guide': ['Lo Shu Grid Guide: Missing Numbers and Meanings', 'Learn how the Lo Shu grid reads birth-date patterns, missing numbers, repeated numbers, and personality tendencies in a 3x3 numerology chart.'],
  '/blog/lucky-numbers-india': ['Lucky Numbers in India: Chaldean Numerology Guide', 'Find lucky numbers through Moolank, Bhagyank, name number, planetary friendship, and traditional Indian numerology context.'],
  '/blog/moolank-meanings': ['Moolank Meanings: Birth Numbers 1-9 Explained', 'Read all nine Moolank or Birth Number meanings, including ruling planets, strengths, emotional patterns, career tendencies, and compatibility.'],
  '/blog/name-correction-guide': ['Name Correction in Numerology: Practical Guide', 'A practical guide to Chaldean name correction, when spelling changes make sense, how alignment is checked, and what to expect realistically.'],
  '/blog/name-numerology-business': ['Business Name Numerology: Choose an Aligned Brand', 'Use Chaldean numerology to evaluate a business name, founder fit, brand vibration, compound number, and long-term venture alignment.'],
  '/blog/number-4-8-cheiro': ['Number 4 and 8 in Cheiro: Meaning and Caution', 'Explore why Cheiro warned about Numbers 4 and 8, what Rahu and Saturn represent, and how to read this pairing without fatalism.'],
  '/blog/personal-year-1-meaning': ['Personal Year 1 Meaning: New Cycle, New Direction', 'Personal Year 1 begins a fresh nine-year cycle. Learn the career, relationship, timing, and emotional themes of a Year 1 phase.'],
  '/blog/personal-year-2026': ['Personal Year 2026: Calculate Your Year Number', 'Calculate your Personal Year for 2026 and read what the cycle means for decisions, relationships, work, endings, and new beginnings.'],
  '/blog/personal-year-9-meaning': ['Personal Year 9 Meaning: Closure and Release', 'Personal Year 9 closes a nine-year cycle. Learn what to finish, release, forgive, and prepare before the next beginning arrives.'],
  '/blog/personal-year-guide': ['Personal Year Numbers 1-9: Complete Guide', 'Understand Personal Year Numbers 1 to 9, how to calculate yours, and what each year means for timing, choices, relationships, and work.'],
  '/blog/relationship-compatibility-numerology': ['Numerology Compatibility: Birth Number Pair Guide', 'Learn how Chaldean compatibility reads Birth Number pairs, emotional pacing, conflict patterns, friendship, marriage, and relationship repair.'],
  '/blog/should-i-change-my-name': ['Should I Change My Name in Numerology?', 'Use this honest decision guide to decide whether a numerology name change is worthwhile, risky, symbolic, practical, or unnecessary.'],
  '/blog/what-is-name-numerology': ['What Is Name Numerology? Chaldean Meaning Guide', 'Name numerology reads the vibration of your daily-use name. Learn how Chaldean letter values, compound totals, and name alignment work.'],
};

function walk(dir) {
  return fs.readdirSync(dir, { withFileTypes: true }).flatMap((entry) => {
    if (entry.name === 'node_modules' || entry.name.startsWith('.')) return [];
    const full = path.join(dir, entry.name);
    return entry.isDirectory() ? walk(full) : [full];
  });
}

function routeFor(file) {
  let rel = path.relative(ROOT, file).replace(/\\/g, '/').replace(/\.html$/, '');
  if (rel === 'index') return '/';
  return '/' + rel.replace(/\/index$/, '');
}

function snippetFor(route) {
  let m;
  if (route === '/') return ['Free Chaldean Numerology Calculator | NameAligned', 'Calculate your name number, Birth Number, Life Path, compatibility, and name alignment with free Chaldean numerology tools.'];
  if (route === '/number') return ['Chaldean Numbers 1-9: Personality, Career, Love', 'Explore every Chaldean numerology number from 1 to 9, including personality, career, name number, life path, love, stress, and remedies.'];
  if (route === '/blog') return ['Numerology Blog: Chaldean Guides and Meanings', 'Read Chaldean numerology guides on names, Moolank, compatibility, personal years, lucky numbers, name correction, and business names.'];
  if (route === '/sitemap-pages') return ['NameAligned Site Map: Tools, Guides, Numbers', 'Browse every NameAligned tool, guide, number meaning, compatibility page, emotional pattern, career page, and Chaldean numerology resource.'];
  if (route === '/ai-disclosure') return ['AI Disclosure: How NameAligned Uses AI', 'See where NameAligned uses AI support, where calculations stay rule-based, and how Aura, reports, sources, and editorial review are handled.'];
  if (route === '/love-compatibility-numerology') return ['Relationship Compatibility Calculator | Chaldean', 'Compare any two people with a free Chaldean compatibility reading for communication style, emotional pace, stress response, and repair patterns.'];
  if (route === '/analyzer') return ['Free Chaldean Numerology Calculator by Name and DOB', 'Use the free Chaldean calculator to read your name number, Birth Number, Life Path, alignment score, lucky attributes, and core patterns.'];
  if (route === '/ask-aura') return ['Ask Aura: Numerology Chat for Love and Career', 'Ask Aura about love, career, timing, names, and emotional patterns using your Chaldean numerology context as a reflective guide.'];
  if (route === '/report') return ['Full Chaldean Numerology Report PDF | NameAligned', 'Get a personalised Chaldean numerology PDF with name alignment, 5-year forecast, career themes, compatibility, remedies, and timing.'];
  if (route === '/name-alignment') return ['Name Alignment Meaning in Chaldean Numerology', 'Name alignment shows how well your name vibration supports your birth numbers, identity, confidence, work rhythm, and relationships.'];
  if (route === '/name-numerology-calculator') return ['Free Name Numerology Calculator: Is Your Name Lucky?', 'Check your name number instantly with a free Chaldean numerology calculator. Get your name score, Birth Number, Life Path Number, archetype and lucky days.'];
  if (route === '/name-correction-numerology') return ['Name Correction Numerology: Free Spelling Check', 'Check whether your spelling supports your Chaldean birth numbers and explore realistic name correction guidance without overpromising.'];
  if (route === '/business-name-numerology') return ['Business Name Numerology Calculator | Chaldean', 'Check whether a business or brand name aligns with founder numbers, venture timing, compound vibration, and long-term identity.'];

  if (blogSnippets[route]) return blogSnippets[route];

  if ((m = route.match(/^\/number\/([1-9])-personality$/))) {
    const [planet, traits] = planets[m[1]];
    return [`Number ${m[1]} Personality: ${planet} Traits and Patterns`, `Number ${m[1]} personality in Chaldean numerology: ${traits}, with love style, career rhythm, emotional shadows, and related meanings.`];
  }
  if ((m = route.match(/^\/number\/([1-9])-career$/))) {
    const [planet] = planets[m[1]];
    return [`Best Careers for Number ${m[1]}: ${planet} Work Style`, `Best careers for Number ${m[1]} in Chaldean numerology, with work strengths, pressure patterns, industries to avoid, and practical role matches.`];
  }
  if ((m = route.match(/^\/name-number-([1-9])-meaning$/))) {
    const [planet, traits] = planets[m[1]];
    return [`Name Number ${m[1]} Meaning: ${planet} Vibration`, `Name Number ${m[1]} in Chaldean numerology carries ${planet} energy: ${traits}, with career, love, shadow, and alignment insights.`];
  }
  if ((m = route.match(/^\/life-path-number-([1-9])-meaning$/))) {
    const [planet, traits] = planets[m[1]];
    return [`Life Path Number ${m[1]} Meaning: ${planet} Destiny`, `Life Path Number ${m[1]} carries ${planet} energy: ${traits}, with Chaldean destiny themes, work patterns, love, and growth lessons.`];
  }
  if ((m = route.match(/^\/number-([1-9])-in-love$/))) {
    const [planet] = planets[m[1]];
    return [`Number ${m[1]} in Love: ${planet} Relationship Style`, `Number ${m[1]} in love shows a ${planet}-led relationship style: emotional needs, attraction patterns, conflict habits, repair cues, and best matches.`];
  }
  if ((m = route.match(/^\/why-number-([1-9])-overthinks$/))) {
    const [planet] = planets[m[1]];
    return [`Why Number ${m[1]} Overthinks: ${planet} Stress Pattern`, `Why Number ${m[1]} overthinks in Chaldean numerology, including ${planet} stress loops, emotional triggers, communication needs, and calming practices.`];
  }
  if ((m = route.match(/^\/number-([1-9])-spiritual-meaning$/))) {
    const [planet] = planets[m[1]];
    return [`Number ${m[1]} Spiritual Meaning: ${planet} Lesson`, `Number ${m[1]} spiritual meaning in Chaldean numerology: the ${planet} soul lesson, shadow, growth practice, relationships, and inner work.`];
  }
  if ((m = route.match(/^\/lucky-attributes-number-([1-9])$/))) {
    const [planet] = planets[m[1]];
    return [`Lucky Attributes for Number ${m[1]}: ${planet} Guide`, `Lucky days, colours, gemstones, directions, dates, metals, and practical Chaldean remedies for Number ${m[1]} under ${planet} energy.`];
  }
  if ((m = route.match(/^\/number-([1-9])-and-([1-9])-compatibility$/))) {
    const [pa] = planets[m[1]], [pb] = planets[m[2]];
    return [`Number ${m[1]} and ${m[2]} Compatibility: ${pa} and ${pb}`, `Number ${m[1]} and ${m[2]} compatibility in Chaldean numerology: marriage, friendship, communication, conflict rhythm, strengths, and repair patterns.`];
  }
  return null;
}

function setContent(doc, selector, value) {
  const el = doc.querySelector(selector);
  if (el) el.setAttribute('content', value);
}

function resetMeta(doc, selector, attrs) {
  const el = doc.querySelector(selector);
  if (!el) return;
  for (const attr of [...el.attributes]) el.removeAttribute(attr.name);
  for (const [name, value] of Object.entries(attrs)) el.setAttribute(name, value);
}

let changed = 0;
let optimized = 0;

for (const file of walk(ROOT).filter((f) => f.endsWith('.html'))) {
  const route = routeFor(file);
  if (route.startsWith('/share') || /preview|staging-report|wordmark|google31|share-card/.test(route)) continue;

  const html = fs.readFileSync(file, 'utf8');
  const dom = new JSDOM(html);
  const doc = dom.window.document;
  const robots = doc.querySelector('meta[name="robots"]')?.getAttribute('content') || '';
  if (/noindex/i.test(robots)) continue;

  const snippet = snippetFor(route);
  if (!snippet) continue;
  const [title, desc] = snippet;

  const titleEl = doc.querySelector('title');
  if (titleEl) titleEl.textContent = title;
  resetMeta(doc, 'meta[name="description"]', { name: 'description', content: desc });
  resetMeta(doc, 'meta[property="og:title"]', { property: 'og:title', content: title });
  resetMeta(doc, 'meta[property="og:description"]', { property: 'og:description', content: desc });
  resetMeta(doc, 'meta[name="twitter:title"]', { name: 'twitter:title', content: title });
  resetMeta(doc, 'meta[name="twitter:description"]', { name: 'twitter:description', content: desc });

  const out = dom.serialize();
  if (out !== html) {
    fs.writeFileSync(file, out);
    changed++;
    optimized++;
  }
}

console.log(JSON.stringify({ changed, optimized }, null, 2));
