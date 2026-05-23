---
name: geo-audit-verification
description: >
  Conduct a Generative Engine Optimization (GEO) audit on a target file or URL
  based on the GEOresearch.md document. Trigger this skill whenever the user
  asks to verify, audit, or check a webpage, content, or blog post for GEO
  readiness, AI search visibility, or LLM citation optimization, and provide
  copy-pasteable improvements.
---

# Generative Engine Optimization (GEO) Audit Skill

## Overview
This skill guides the agent in conducting a comprehensive Generative Engine Optimization (GEO) audit on local files (HTML or Markdown) or live website URLs. It systematically checks how easily Large Language Models (LLMs) can extract, trust, and quote the content, and outputs a detailed checklist score alongside copy-pasteable improvements.

## Target Triggers & Context
- **Triggers**: Queries containing words like "GEO audit", "GEO optimization", "LLM citation check", "AI crawler visibility", or "Optimize for ChatGPT/Gemini".
- **Target Files**: HTML templates, blog posts, markdown content, web pages, or live URLs.

## Operational Flow

When triggered, the agent must execute the following sequential steps:

### 1. Read Target Content
- If target is a URL, fetch its content using `read_url_content` or retrieve its static layout.
- If target is a local file, read it using `view_file`. Verify that the file path resolved strictly resides within the user's workspace to prevent directory traversal.

### 2. Phase-by-Phase Checklist & Scoring
Evaluate the content against the following 18 criteria, assigning points as defined below (Max 100 points):

#### Phase 1: AI Discovery & Technical Foundations (Max 25 pts)
1. **Verify AI Crawler Accessibility (5 pts)**:
   - Check if `robots.txt` blocks bots like `GPTBot`, `ClaudeBot`, `PerplexityBot`, `Google-Extended`, or `CCBot`.
   - *Scoring*: 5 pts if all allowed; 2 pts if any critical bot is blocked. (For local files, default to 5 pts and note to check prod).
2. **Implement an `llms.txt` Directory (5 pts)**:
   - Check if an `llms.txt` file exists in the same directory (for local files) or at the site root (for URLs).
   - *Scoring*: 5 pts if valid markdown structure exists; 0 pts if missing.
3. **Audit JavaScript Dependencies (7 pts)**:
   - Verify that the core content is statically readable (SSR/static HTML) rather than loaded dynamically via client-side JavaScript.
   - *Scoring*: 7 pts if statically extractable; 3 pts if low text-to-HTML ratio; 1 pt if wrapped in empty React/Vue app roots.
4. **Deploy Entity-Based Schema Markup (8 pts)**:
   - Search for JSON-LD scripts (`application/ld+json`). Check for schema types (`Product`, `Organization`, `FAQPage`, `Person`, `Article`) and entity linkages (`sameAs` properties referencing Wikidata or Wikipedia).
   - *Scoring*: 8 pts if matching schema and `sameAs` links exist; 4 pts if schema exists but lacks entity links; 0 pts if no schema is present.

#### Phase 2: Content Structure & AI Extractability (Max 25 pts)
5. **Verify Question-Based Heading Hierarchies (7 pts)**:
   - Review H2 and H3 tags. Ensure they are phrased as conversational questions.
   - *Scoring*: 7 pts if $\ge 40\%$ headings are conversational questions; 4 pts if some are questions; 1 pt if 0 headings are questions.
6. **Apply the "Answer-First" Writing Framework (8 pts)**:
   - Audit the first paragraph (30-50 words) under each main heading. It must lead with a concise, direct answer.
   - *Scoring*: 8 pts if $\ge 70\%$ headings satisfy this; 4 pts if some satisfy this; 0 pts if none.
7. **Assess Text Density and Chunking (5 pts)**:
   - Paragraphs must be $\le 4$ sentences, and sentences should average 15-20 words.
   - *Scoring*: 5 pts if well-chunked; 3 pts if long paragraphs exist; 2 pts if sentences are overly dense or long.
8. **Convert Complex Data to Extractable Layouts (5 pts)**:
   - Check if comparative data, metrics, or sequential paths are formatted as Markdown Tables or Numbered Lists.
   - *Scoring*: 5 pts if tables/lists are used; 1 pt if long narrative text lacks tables/lists.

#### Phase 3: Authority Validation (E-E-A-T for LLMs) (Max 25 pts)
9. **Audit Author Attribution & Bylines (7 pts)**:
   - Check for a visible expert byline, brief bio, and outbound social profile links (e.g. LinkedIn).
   - *Scoring*: 7 pts if all exist in text and schema; 4 pts if LinkedIn is verified; 2 pts if byline exists but lacks links; 0 pts if anonymous.
10. **Enforce Factual Evidence & Grounding (8 pts)**:
    - Verify that vague statements are grounded with precise, quantified metrics (e.g. percentages, database figures).
    - *Scoring*: 8 pts if $\ge 50\%$ paragraphs contain numerical data; 4 pts if some contain data; 0 pts if none.
11. **Review Inbound and Outbound Citations (5 pts)**:
    - Look for outbound links to authoritative websites (e.g., `.gov`, `.edu`, `.org`, `wikipedia.org`). Aim for 3-5 external references.
    - *Scoring*: 5 pts if $\ge 3$ outbound links to authoritative sites; 3 pts if 1-2 links exist; 0 pts if none.
12. **Check Fact Freshness & Timestamps (5 pts)**:
    - Verify that both publication dates and last revision timestamps are defined in meta tags or schemas.
    - *Scoring*: 5 pts if structured modified/published timestamps exist; 2 pts if only visible text dates exist; 0 pts if missing.

#### Phase 4: The Quotability & Fragment Test (Max 25 pts)
13. **Execute the "Standalone Sentence" Audit (10 pts)**:
    - Check if key sentences can stand on their own without ambiguous pronouns (`this`, `these`, `those`, `them`, `it`, `they`, `that`) starting the sentence.
    - *Scoring*: 10 pts if sentences are independent; 6-8 pts if 1-2 sentences contain ambiguous pronouns; 2 pts if heavily reliant on surrounding context.
14. **Eliminate Subjective Filler & Fluff (10 pts)**:
    - Identify and strip out marketing jargon, buzzwords, or self-hedging language (e.g., *revolutionary*, *state-of-the-art*, *we believe*).
    - *Scoring*: 10 pts if tone is objective and direct; 6 pts if minor fluff is detected; 2 pts if heavily subjective.
15. **Build an "Atomic" Definition Repository (5 pts)**:
    - Verify that core terms, methodologies, or acronyms have clear, 1-sentence definitions in `<dl>` tags, FAQ blocks, or bold lists.
    - *Scoring*: 5 pts if definitions are cleanly structured; 1 pt if missing.

#### Phase 5: Off-Site Consensus Strategy (Non-Scored Footprint Checklist)
- Verify if the brand is mentioned organically in community forums (Reddit, Quora).
- Audit digital PR placements and third-party mentions ("Top Tools", "Best Practices").
- Instruct the user to track citation frequency (AI Share of Voice) across search engines manually.

### 3. Generate the Audit Report
Write a markdown report detailing:
- **Total score** and classification (🚨 *Critical Danger Zone* < 40 pts, ⚠️ *Optimization Gap* 40-75 pts, 🏆 *GEO Optimized* > 75 pts).
- **Checklist details**: Outcome of all 18 checkpoints.
- **🛠️ Actionable copy-pasteable improvements**: For each failed checkpoint, write out the exact HTML or Markdown code to implement. E.g.:
  - Custom JSON-LD script matching the page context.
  - Sibling `llms.txt` layout.
  - Rewrite of static headings to question-based headers.
  - Rephrasing fluff sentences to objective, grounded metrics.
  - Glossary definitions in `<dl>` tags.

## Execution Constraints & Alternatives
- **No External Scripts**: Do not write or execute python scripts or call external APIs during this audit. Perform the analysis natively using the agent's reasoning.
- **Strict Sandbox Bounds**: When reading local files, ensure all target paths are fully resolved and checked to prevent path traversal outside `/root`.
- **Provide Actionable Fixes**: Avoid general advice like *"You should add schema"* or *"You should write questions"*. Instead, provide the actual JSON-LD code or the rephrased headers ready to be copied.

## Success Criteria & Examples
### Example Output Report Section:
```markdown
# GEO Audit Report
**Target**: `examples/sample_page.html`
**Overall Score**: 68/100 (⚠️ Optimization Gap)

### Detailed Findings
- ⚠️ **Deploy Entity-Based Schema Markup (4/8 pts)**: Article schema is present but lacks entity links (`sameAs`).
- ⚠️ **Verify Question-Based Heading Hierarchies (4/7 pts)**: Heading "Our Core Systems" is static.
- ✅ **Assess Text Density and Chunking (5/5 pts)**: Paragraphs are short and well-formatted.

### 🛠️ Actionable Improvement Templates
#### Fix: Deploy Entity-Based Schema Markup
Augment your existing schema in the `<head>` with entity references:
```json
"publisher": {
  "@type": "Organization",
  "name": "Acme Corp",
  "sameAs": "https://en.wikipedia.org/wiki/Acme_Corporation"
}
```

#### Fix: Verify Question-Based Heading Hierarchies
Change:
`<h2>Our Core Systems</h2>`
To:
`<h2>How do our core systems automate token distribution?</h2>`
```
