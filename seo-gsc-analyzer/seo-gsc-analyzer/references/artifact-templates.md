# Artifact Templates

Structural guidance for each of the three artifacts the skill publishes. All three must be self-contained, light-mode HTML, and follow `create_artifact`'s constraints (inline CSS/JS, only the allowed CDN tags for Chart.js / Grid.js / Mermaid).

Use a consistent visual identity across all three artifacts so the user perceives them as one report:
- Background: `#fafafa`
- Card background: `#ffffff` with `box-shadow: 0 1px 3px rgba(0,0,0,0.08)` and `border-radius: 12px`
- Primary color: `#0f172a` (slate)
- Accent: `#2563eb` (blue) for positive, `#dc2626` for negative
- Font: system stack (`-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif`)
- Add `:root { color-scheme: light }` at the top

Each artifact's header should include: the site URL, the date range, and a small "Last updated: <timestamp>" note.

---

## Artifact 1 — Performance Overview

`id: gsc-overview-<sanitized-site>` · file: `overview.html`

Sections (top to bottom):

1. **KPI cards row** — 4 cards: Clicks, Impressions, CTR, Avg Position. Each shows the current 30-day total, the prior 30-day total, and the % change (green for improvement, red for regression — remember position improvement is *negative* delta).

2. **Daily trend chart** (Chart.js line chart) — clicks on the primary axis, impressions on a secondary axis, both 60 days. Mark a vertical line at the boundary between previous and current windows.

3. **Device split** — small horizontal bar chart from Slice E: clicks per device.

4. **Branded vs non-branded share** — donut chart (clicks share) plus a second donut (impressions share). Source: Slice B grouped by `branded_vs_nonbranded`.

5. **Top 10 queries by clicks** — Grid.js table: query, clicks, impressions, CTR, position. Sortable.

Embed the data inline as a `const DATA = { ... }` JSON blob so the artifact is fully self-contained.

---

## Artifact 2 — Insights Digest

`id: gsc-insights-<sanitized-site>` · file: `insights.html`

This artifact is narrative + tables, NOT charts. Sections:

1. **Headline** — one paragraph stating the most important shift: e.g. "Non-branded clicks grew 22% MoM while branded clicks held flat — your content is starting to acquire its own audience."

2. **Wins** — bulleted list of 3–5 wins: queries that jumped into top 10, pages with CTR above expectation, branded growth, etc.

3. **Watch-outs** — 3–5 things to watch: queries that dropped, pages with high impressions but plummeting CTR, device-specific regressions.

4. **Title/meta opportunities** — Grid.js table of queries flagged as title/meta opportunities (high impressions, low CTR, top 10 position). Columns: query, page, impressions, CTR, position.

5. **Quick-win ranking opportunities** — separate Grid.js table of queries flagged as ranking opportunities (high impressions, position 11–20). Columns: query, page, impressions, CTR, position.

6. **Branded-vs-non-branded mix** — one line summarizing the split and whether the site is over-dependent on brand search.

Every flagged item must come from real data — no fabricated queries.

---

## Artifact 3 — Page 2 Action Plan (the headline output)

`id: gsc-page2-actionplan-<sanitized-site>` · file: `page2-actionplan.html`

This is the most important artifact. Sections:

1. **Summary header** — "X pages are stuck on page 2. Together they earned Y impressions in the last 30 days. The top opportunity is …"

2. **Filter chips** — buttons at the top to filter the page list by classification: All / Blog / Service. Implement with simple in-page JS (no frameworks beyond what's allowed).

3. **Page cards** — one card per page, sorted by `opportunity_score` descending. Each card contains:
   - The page URL (clickable, opens in a new tab).
   - A pill showing its classification (`Blog` / `Service` / `Unsure`).
   - Metric row: avg position, clicks, impressions, CTR, opportunity score.
   - **Top queries for this page** (Slice D data) — small table or list, max 5 rows: query · position · impressions · ctr.
   - **Recommended actions** — a numbered list. Use the templates from `analysis-methodology.md`, substituting the real page URL, top query, and metrics. The action list MUST differ in flavor between blog and service classifications (rewrite-for-quality vs improve-content-and-internal-linking).

4. **Footer** — note about how the opportunity score is calculated so the user understands the ordering.

If there are more than 25 pages, show the top 25 by default and add a "Show all <N>" button that reveals the rest.

Embed all data as a `const PAGES = [...]` JSON blob with one object per page, including its query breakdown and recommendations. That way the artifact is fully usable offline and the recommendations don't get regenerated on reload — the data is the source of truth.

---

## Cross-artifact behavior

- All three artifacts should link to each other via simple anchor links at the top: "Overview · Insights · Action Plan" (just open `computer://...` style URLs into the other artifacts? Actually, artifacts can't cross-link reliably — instead, mention the other artifact IDs in the chat summary).
- Each artifact's title tag should be `GSC Analyzer — <Site> — <Section>` for clarity in the sidebar.
- Footer of each artifact: "Generated by the seo-gsc-analyzer skill · data via Windsor.ai · <timestamp>".

---

## Tool list for `mcp_tools`

Pass the actual Windsor `get_data` tool name you called — the prefix will be something like `mcp__594ff54f-…__get_data`. List it once per artifact even though all three share the same tool; this enables the Reload button.
