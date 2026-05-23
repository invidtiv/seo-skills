---
name: seo-gsc-analyzer
description: Analyze a site's Google Search Console performance via the Windsor.ai connector and produce three live artifacts — a 30-day performance overview, an insights digest, and a page-2 opportunity action plan that classifies each stuck page as blog vs service/transactional and gives tailored rewrite or internal-link recommendations. Use whenever the user asks for an "SEO performance analysis", "GSC report", "page 2 opportunities", "SEO health check", or "what should I fix on my site" — as long as a Windsor.ai connector with a `searchconsole` account is connected. Works portably against whichever GSC site the connector is authorized for.
---

# SEO GSC Analyzer

This skill turns the Windsor.ai Google Search Console connector into a one-command SEO deep dive. It produces three live artifacts:

1. **Performance Overview (last 30 days vs prior 30 days)** — clicks, impressions, CTR, average position, trend chart, branded vs non-branded split, device split.
2. **Insights Digest** — interesting movers, surprising winners/losers, query-level wins, queries with high impressions but weak CTR, branded vs non-branded shifts.
3. **Page 2 Action Plan** — every page averaging position 11–20, classified as `blog` vs `service/transactional`, with tailored recommendations:
   - **Blog posts** → rewrite for higher quality (depth, freshness, examples, schema, original data).
   - **Service / transactional pages** → improve uniqueness of the on-page content and internal linking from related blog posts.

Artifacts are created with `mcp__cowork__create_artifact` so the user can re-open them later and they will refresh from the connector.

---

## When to use this skill

Trigger on:
- "Analyze my SEO performance", "audit my GSC", "run my monthly SEO report"
- "What pages are on page 2", "find page-2 opportunities", "where can I get quick SEO wins"
- "Give me an SEO health check"
- Any time the user mentions the Windsor.ai connector and Search Console

Do NOT trigger when:
- The user wants a Lighthouse / technical audit (use `seo-audit-report` or `dataforseo-technical-audit` instead)
- The user wants AI-search visibility (use `dataforseo-ai-visibility`)
- The user has not connected a Windsor.ai `searchconsole` account

---

## Required tools

This skill calls these MCP tools — they are part of the Windsor.ai connector. The exact server prefix (`mcp__<id>__`) varies per user, but the underscore-suffix names are stable:

- `get_connectors` — discover connected Windsor connectors
- `get_fields` — confirm the searchconsole fields available
- `get_data` — pull rows
- `mcp__cowork__create_artifact` — publish the three artifacts

If the prefix differs, find the right one by searching for `searchconsole` in the available tools.

---

## Workflow

### Step 1 — Discover the connected GSC account (portable)

Call `get_connectors` (no arguments). Look for a connector with id `searchconsole`. It returns an `accounts` list — each account's `id` is the GSC property URL (e.g. `https://www.example.com/` or `sc-domain:example.com`).

Decision rules:
- **No `searchconsole` connector** → tell the user they need to connect Google Search Console in Windsor.ai, and offer to call `get_connector_authorization_url` with connector id `searchconsole`. Stop.
- **One account** → use it directly. Tell the user which site you're analyzing.
- **Multiple accounts** → ask the user which property to analyze (use `AskUserQuestion` with each account id as an option).

Store the chosen account id as `SITE_ID` for the rest of the workflow. Never hardcode a URL — always use the discovered value.

### Step 2 — Pull the three data slices

Always pass `accounts: [SITE_ID]` and `connector: "searchconsole"`. Use `date_preset` rather than absolute dates so the skill stays portable.

**Slice A — daily totals (last 60 days, for trend + period-over-period comparison)**

```
fields: ["date", "clicks", "impressions", "ctr", "position"]
date_preset: "last_60d"
```

Split the rows in code into two windows: most recent 30 days = "current", prior 30 days = "previous". Compute totals and deltas.

**Slice B — top queries (last 30 days)**

```
fields: ["query", "clicks", "impressions", "ctr", "position", "branded_vs_nonbranded"]
date_preset: "last_30d"
```

Use this for the Insights artifact: top performers, high-impression / low-CTR queries (title/meta opportunities), branded vs non-branded split.

**Slice C — page-level data, position 11–20 only (the page-2 cohort)**

```
fields: ["page", "clicks", "impressions", "ctr", "position"]
date_preset: "last_30d"
filters: [["position", "gte", 11], "and", ["position", "lte", 20.99]]
```

This is the heart of the action plan. Sort by `impressions` descending — these are the pages with the most upside.

**Slice D (optional but recommended) — queries per page-2 page**

For each page in Slice C with `impressions > 50`, pull its top queries:

```
fields: ["query", "clicks", "impressions", "ctr", "position"]
date_preset: "last_30d"
filters: [["page", "eq", <page-url>]]
```

This lets you tell the user *which* query each stuck page is closest to winning.

**Slice E — device split (last 30 days)**

```
fields: ["device", "clicks", "impressions", "ctr", "position"]
date_preset: "last_30d"
```

### Step 3 — Classify each page-2 page

For every page in Slice C, classify by URL pattern. Use the path after the hostname:

- **Blog** if any of these substrings appear in the path: `/blog/`, `/blogs/`, `/post/`, `/posts/`, `/article/`, `/articles/`, `/news/`, `/guide/`, `/guides/`, `/learn/`, `/resources/`, `/insights/`, `/tutorial/`, `/how-to/`, `/case-study/`, `/case-studies/`. Also classify as blog if the slug ends in a long descriptive phrase (≥4 hyphenated words) and isn't under `/features/`, `/pricing/`, `/services/`, `/solutions/`, `/products/`.
- **Service / transactional** otherwise — especially `/features/`, `/pricing/`, `/services/`, `/solutions/`, `/products/`, `/use-cases/`, `/integrations/`, `/tools/`, or the root/homepage.
- **Unsure** — treat as service/transactional but note the uncertainty in the recommendation.

If the user has told you their site's URL conventions in prior messages or in CLAUDE.md, prefer those over the defaults.

### Step 4 — Build recommendations per page

**For a blog post on page 2:**
- Rewrite the post for higher quality: more depth, original examples, expert quotes, current statistics (note the publish year), screenshots, and a clear answer capsule near the top.
- Add or expand FAQ schema using questions extracted from the page's top queries (Slice D).
- Improve E-E-A-T: byline, author bio, last-updated date, sources.
- Tighten the title tag and meta description to match the dominant query intent.
- Refresh internal links pointing TO this post from related higher-authority pages.

**For a service / transactional page on page 2:**
- Audit content uniqueness: rewrite generic boilerplate, add proof (case studies, screenshots, customer logos, numbers), differentiate from competitors.
- Strengthen internal linking: link FROM at least 3–5 relevant blog posts using exact-match or near-match anchor text targeting the page's primary query.
- Add structured data appropriate to the page type (Product, Service, Offer, BreadcrumbList).
- Improve scannability and clarity of value prop above the fold; clarify the CTA.
- Build out a dedicated FAQ section answering the top queries from Slice D.

Surface, for each recommendation, the specific query it targets and the impressions/CTR/position context so the user can prioritize.

### Step 5 — Publish three artifacts

Create three separate artifacts so each is independently re-openable. Each artifact must be self-contained HTML, light-mode, and may load Chart.js / Grid.js from the allowed CDNs (see the create_artifact tool description for exact tags).

Write each artifact's HTML to a temporary file first, then call `mcp__cowork__create_artifact`:

- `id: "gsc-overview-<sanitized-site>"`, file: `overview.html`
- `id: "gsc-insights-<sanitized-site>"`, file: `insights.html`
- `id: "gsc-page2-actionplan-<sanitized-site>"`, file: `page2-actionplan.html`

Pass `mcp_tools` listing the Windsor `get_data` tool you used so each artifact can refresh.

Artifact structure guidance is in `references/artifact-templates.md`. Page classification rules and recommendation language live in `references/analysis-methodology.md`.

### Step 6 — Summarize in chat

Finish with a short chat reply:

> Pulled 30-day GSC data for `<SITE_ID>` via Windsor. Three artifacts ready below.
> - **Headline:** Clicks `<curr>` vs `<prev>` (`<+/- %>`). Avg position `<curr>` vs `<prev>`.
> - **Biggest page-2 opportunity:** `<URL>` at position `<n>` for `<query>` (`<impressions>` monthly impressions). Recommended action: `<one-line>`.
>
> [View overview](computer://...) · [View insights](computer://...) · [View page 2 action plan](computer://...)

Do NOT dump full tables into chat — that's what the artifacts are for.

---

## Portability notes

This skill is intentionally site-agnostic. To run it for a different GSC property:

1. The recipient must have a Windsor.ai connector with a `searchconsole` account connected to their target site.
2. They run the skill the same way — Step 1 will auto-discover their site.
3. No code changes required.

If the recipient's connector is connected but no `searchconsole` account is present, point them at `get_connector_authorization_url(connector="searchconsole")` to authorize Google Search Console inside Windsor.

---

## Edge cases & guardrails

- **Tiny sites (fewer than 50 total impressions in 30 days):** say the data is too thin for meaningful page-2 analysis; show the overview only.
- **Pages with `clicks=0` and `impressions<20`:** drop from the action plan — too noisy.
- **Position field is fractional:** treat anything in `[10.5, 20.99]` as page 2 to catch borderline pages.
- **Domain-property sites (`sc-domain:example.com`):** pages will still come back with full URLs; classification rules above still apply.
- **The connector returns `branded_vs_nonbranded` as `"branded"` / `"nonbranded"`** — group by this for the branded mix chart.
- **Never invent recommendations.** Every recommendation should reference a real query, page, or metric that came back from the connector. If you have no Slice D data for a page, say "no query-level breakdown available — review top organic queries in GSC directly".
- **Use code for math.** Don't eyeball averages or growth percentages — compute them with the bash tool over the JSON the connector returned.

---

## What to share at the end

In chat, link to all three artifacts via `computer://` paths (Cowork auto-renders these). Keep the chat summary short — the artifacts hold the detail.
