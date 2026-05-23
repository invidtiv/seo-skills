# Analysis Methodology

Detailed rules the skill uses to turn raw GSC rows into recommendations.

## Period-over-period math

Given Slice A (last 60 days of daily totals):

- `current` window = rows where `date` is in the most recent 30 days.
- `previous` window = rows where `date` is in the 30 days before that.
- For clicks and impressions: sum within each window, compute `(current - previous) / previous * 100` (guard against divide-by-zero).
- For position: weighted by impressions — `sum(position * impressions) / sum(impressions)` per window. Lower is better, so a *negative* delta is an improvement.
- For CTR: recompute as `sum(clicks) / sum(impressions)` per window — do NOT average the per-row CTR field.

Always run the math in `mcp__workspace__bash` with Python over the JSON the connector returned. Do not eyeball it.

## Page classification

Apply rules to the path portion of the URL (after the hostname):

1. **Blog path patterns** (case-insensitive substring match):
   `/blog/`, `/blogs/`, `/post/`, `/posts/`, `/article/`, `/articles/`,
   `/news/`, `/guide/`, `/guides/`, `/learn/`, `/learning/`, `/resources/`,
   `/insights/`, `/tutorial/`, `/tutorials/`, `/how-to/`, `/howto/`,
   `/case-study/`, `/case-studies/`, `/stories/`, `/tips/`

2. **Service / transactional path patterns:**
   `/features/`, `/pricing/`, `/services/`, `/solutions/`, `/products/`,
   `/product/`, `/use-cases/`, `/integrations/`, `/tools/`, `/platform/`,
   `/plans/`, `/buy/`, `/shop/`, `/store/`, `/contact/`, `/demo/`, `/signup/`,
   `/login/`, `/free-trial/`

3. **Slug heuristic:** if no path pattern matched, count hyphens in the final slug. A slug with ≥3 hyphens and ≥4 word-like tokens (e.g. `the-best-way-to-rank-on-google`) is most likely a blog post. A short slug (`/features`, `/pricing`, `/api`) is service-y.

4. **Homepage** (`/` only): treat as service/transactional but flag it — the homepage usually deserves its own dedicated review.

5. **Unsure** → default to service/transactional, note `(classification: unsure)` in the recommendation so the user can correct.

## Opportunity scoring (for the page-2 cohort)

Sort the action plan by an `opportunity_score`:

```
opportunity_score = impressions * (11 - min(position, 11)) / 10 * (1 - ctr)
```

Rationale: more impressions = more upside; closer to position 10 = easier climb; lower CTR = bigger title/meta gain. This is a rough proxy — present the components alongside the score so users can prioritize manually.

Show at most 25 pages in the action plan. If there are more, mention the count and link them to the artifact's "show all" toggle.

## Query opportunity flags (for the insights digest)

For each row in Slice B (top queries), flag:

- **Title/meta opportunity**: `impressions > 200` AND `ctr < 0.02` AND `position <= 10`. The page is ranking but the snippet isn't converting.
- **Ranking opportunity**: `impressions > 100` AND `11 <= position <= 20`. Close-but-not-there queries.
- **Position-1 hold**: `position < 2` AND `ctr > 0.2`. Healthy, just call out as a win.
- **Risky drop**: present in `previous` 30-day window but absent or position-dropped by 5+ positions in `current`. (Requires Slice A logic extended to query level — optional.)

## Branded vs non-branded

Sum clicks/impressions per group from Slice B. Show:
- Branded share of clicks and share of impressions.
- If branded share of clicks > 50% AND non-branded share of impressions > 50%, the site is over-relying on brand searches → flag it as an insight.

## Tailored recommendation language

When generating recommendations, use these templates so the output reads consistently:

**Blog post recommendation (template):**

> **<URL>** — currently averaging position **<n>** for **<query>** with **<impressions>** monthly impressions.
> This is a blog post. Recommended actions:
> 1. Rewrite with greater depth (target 1.5–2× current word count) and add original examples, expert quotes, and 2026 statistics.
> 2. Add an "answer capsule" — a 40–60 word direct answer near the top targeting "<query>".
> 3. Add or extend FAQ schema using these top queries: <list 3 queries from Slice D>.
> 4. Update the publish/last-updated date, add an author byline with credentials, and link to primary sources.
> 5. Add 3–5 internal links FROM higher-authority pages on your site.

**Service / transactional recommendation (template):**

> **<URL>** — currently averaging position **<n>** for **<query>** with **<impressions>** monthly impressions.
> This is a service/transactional page. Recommended actions:
> 1. Audit the on-page content for boilerplate copy — rewrite generic sections so the page is materially different from competitor pages.
> 2. Add concrete proof: 2–3 case studies, customer logos, specific numbers, screenshots of the product/service in action.
> 3. Build internal links from 3–5 blog posts that already rank, using anchor text close to "<query>".
> 4. Add structured data appropriate to the page type (Service, Product, Offer, BreadcrumbList, FAQ).
> 5. Sharpen the above-the-fold value prop and CTA so it speaks directly to "<query>" intent.

Always include the query and metrics so the user understands *why* the recommendation matters.
