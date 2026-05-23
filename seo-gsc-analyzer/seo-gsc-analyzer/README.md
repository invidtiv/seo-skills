# seo-gsc-analyzer (Cowork skill)

A drop-in skill for Anthropic Cowork mode that turns a connected **Windsor.ai → Google Search Console** account into a one-command SEO deep dive. It produces three live artifacts:

1. **Performance Overview** — last 30 days vs prior 30 days, clicks / impressions / CTR / avg position, daily trend, device split, branded vs non-branded.
2. **Insights Digest** — wins, watch-outs, title/meta opportunities, quick-win ranking opportunities.
3. **Page 2 Action Plan** — every page averaging position 11–20, classified as **blog post** or **service/transactional**, with tailored recommendations:
   - Blog posts → rewrite for higher quality.
   - Service / transactional pages → unique-content audit + internal linking.

## Requirements

- Cowork mode (or any Claude product that supports user-installed skills).
- A **Windsor.ai** MCP connector connected, with a **Search Console** account authorized for the site you want to analyze.

## Install

Drop the entire `seo-gsc-analyzer/` folder into your skills directory. On Cowork the default location is typically:

```
~/Library/Application Support/Claude/.../skills/
```

(or wherever your existing user skills live — check `mcp__skills__list_skills` to confirm).

Restart Cowork or refresh skills. The skill should appear as `seo-gsc-analyzer` in the available-skills list.

## Use

Just ask:

- "Run the seo-gsc-analyzer skill on my site"
- "Analyze my GSC performance and find page 2 opportunities"
- "Give me an SEO health check"

The skill will auto-discover whichever GSC property is connected via your Windsor.ai connector. If multiple properties are connected, it will ask which one to analyze.

## Portability

The skill never hardcodes a site URL. It always calls `get_connectors` first and uses whatever `searchconsole` account is returned. To share this skill:

1. Send the recipient the `seo-gsc-analyzer/` folder.
2. They drop it into their own skills directory.
3. They install/authorize the Windsor.ai connector for their own GSC site.
4. They run the skill the same way — it picks up *their* site automatically.

## Files

- `SKILL.md` — main skill prompt (Claude reads this when the skill is invoked).
- `references/analysis-methodology.md` — page classification rules, opportunity scoring, recommendation templates.
- `references/artifact-templates.md` — structure and styling guidance for the three HTML artifacts.
- `README.md` — this file.
