# Google Search Console — Indexing Submission Plan

All canonical URLs on namealigned.com, grouped by submission priority.

## Step 0 — submit the sitemap (one-time, covers everything)

In **GSC → Sitemaps → Add a new sitemap**, paste:

```
sitemap.xml
```

(GSC prepends your verified domain automatically.) Full URL is `https://www.namealigned.com/sitemap.xml`.

## Step 1 — request individual indexing

GSC's "Request Indexing" quota is roughly 10 URLs/day, so the plan is split across 3 days.

| File | Day | Pages | Why these |
|---|---|---|---|
| [`tier-a-day1.txt`](./tier-a-day1.txt) | Day 1 | 10 | Money pages + top SEO landings |
| [`tier-b-day2.txt`](./tier-b-day2.txt) | Day 2 | 10 | High-traffic blog posts |
| [`tier-c-day3.txt`](./tier-c-day3.txt) | Day 3 | 10 | Long-tail blog posts + about |
| [`skip-let-google-find.txt`](./skip-let-google-find.txt) | — | 3 | Legal pages (low-priority, sitemap is enough) |
| [`all-urls.txt`](./all-urls.txt) | reference | 33 | Master list, plain text dump |

For each URL: GSC → URL Inspection → paste URL → "Request indexing".

## Step 2 — other Google tools to run

1. **Rich Results Test** — https://search.google.com/test/rich-results
   Paste homepage and /name-numerology-calculator → confirm FAQ rich-result eligibility.
2. **PageSpeed Insights** — https://pagespeed.web.dev/
   Paste homepage. Core Web Vitals affect rankings.
3. **GSC → Performance → Pages** — track which of the 33 URLs start gaining clicks/impressions over the next 2–4 weeks.

## Step 3 — confirm crawl is healthy

GSC → Settings → Crawl stats → confirm Googlebot has visited in the last 24h.
