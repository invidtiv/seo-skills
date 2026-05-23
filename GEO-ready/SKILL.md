---
name: geo-ready-verification
description: >
  Check and verify all the Generative Engine Optimization (GEO) audit items
  defined in research.md for local documents or live websites.
---

# GEO-Ready Verification Skill

This skill automates and guides the process of conducting a **Generative Engine Optimization (GEO) audit** on local content library files or live production URLs. GEO audits evaluate how easily Large Language Models (LLMs) like Gemini, ChatGPT, Claude, and Perplexity can **extract, trust, and quote** your content directly within AI-generated answers.

---

## Directory Structure

This skill follows the standard structure for agent skills:
- **`SKILL.md`**: Main documentation and metadata.
- **`research.md`**: Reference checklist describing the 18 audit points across 5 phases.
- **`scripts/`**: Contains [geo_audit.py](file:///root/SEO-SKILLS/GEO-ready/scripts/geo_audit.py), the Python-based audit engine.
- **`resources/`**: Contains [.env.example](file:///root/SEO-SKILLS/GEO-ready/resources/.env.example) configuration variables.
- **`examples/`**: Contains local demo pages like [sample_page.html](file:///root/SEO-SKILLS/GEO-ready/examples/sample_page.html) to test features.

---

## When to Use This Skill

- Use this skill before publishing new blog posts, knowledge base articles, or product pages.
- Use this skill to evaluate your existing content library layout, schema markup, and authority footprint.
- Use this skill to identify structural blockages that prevent AI crawlers and scrapers from indexing your content.

---

## How It Works

The skill relies on the custom audit script `scripts/geo_audit.py`. It parses and evaluates content against the 18 checklist items defined in [research.md](file:///root/SEO-SKILLS/GEO-ready/research.md).

### Capabilities
1. **Multi-Source Auditing**: Can audit live websites via HTTP URLs or local files (HTML or Markdown).
2. **AI Crawler & Technical Checks**: Evaluates `robots.txt` access rules, root `/llms.txt` existence, SSR (Server-Side Rendering) readability ratio, and JSON-LD schema objects (`Product`, `Organization`, `FAQPage`, etc.).
3. **Structure & Extractability Verification**: Verifies question-based heading hierarchies (H2/H3), assesses text densities, and verifies tabular/list representations of complex comparative data.
4. **Authority validation**: Checks author attribution bylines, outbound citations to authority websites, LinkedIn footprints, and content timestamp metadata.
5. **Quotability & Fluff Testing**: Runs pronoun audits for standalone sentence structures, filters out marketing jargon/buzzwords, and validates term definitions.
6. **Off-Site Consensus Footprint**: Runs automatic queries via Google Search API to count Reddit/Quora brand mentions and digital PR placements.
7. **Brand Name Inference**: If a brand name is not supplied, the tool automatically infers it from page titles, schema properties, domain netlocs, or via a qualitative LLM query.

---

## Configuration

To enable advanced qualitative analysis and automated web footprint searches, create a `.env` file based on `resources/.env.example`:

```bash
# Copy template env
cp /root/SEO-SKILLS/GEO-ready/resources/.env.example /root/SEO-SKILLS/GEO-ready/.env
```

Set the keys in `/root/SEO-SKILLS/GEO-ready/.env`:
- **`GEMINI_API_KEY`**: Enables qualitative analysis (e.g. evaluating the "Answer-First" framework and checking "Standalone Sentence" grammar).
- **`GOOGLE_SEARCH_API_KEY` & `GOOGLE_SEARCH_CX`**: Enables automated search query validation of off-site brand footprint mentions.
- **`BRAND_NAME`**: Optional override. If not set, it is automatically inferred from target pages.

---

## How to Run the Audit

Run the audit script by passing a live URL or a local file path:

### 1. Auditing a Live URL
```bash
python3 /root/SEO-SKILLS/GEO-ready/scripts/geo_audit.py https://example.com/blog/sample-article --report /root/SEO-SKILLS/GEO-ready/my_report.md
```

### 2. Auditing a Local Example File
```bash
python3 /root/SEO-SKILLS/GEO-ready/scripts/geo_audit.py /root/SEO-SKILLS/GEO-ready/examples/sample_page.html --report /root/SEO-SKILLS/GEO-ready/examples/sample_page_report.md
```

### 3. Auditing a Local Markdown File
```bash
python3 /root/SEO-SKILLS/GEO-ready/scripts/geo_audit.py /root/SEO-SKILLS/GEO-ready/research.md --report /root/SEO-SKILLS/GEO-ready/markdown_audit.md
```

---

## Output Report

The script generates a markdown audit report containing:
- **GEO-Ready Score (0 to 100)**.
- **Scoring Status**:
  - 🚨 **Critical Danger Zone** (< 40 pts): Blocked crawlers, heavy JS client-side dependencies, no schema, dense walls of narrative text.
  - ⚠️ **Optimization Gap** (40 - 75 pts): Crawlable, structured, but lacks grounding metrics, author profiles, citations, or conversational heading structures.
  - 🏆 **GEO Optimized** (> 75 pts): Answer-first layouts, rich JSON-LD markup, clear definitions/tables, and verified off-site citations.
- **Detailed checklist results** for all 18 GEO checkpoints.
- **Advanced Gemini Insights** (if API key provided): Spotlights specific instances of subjective marketing fluff and provides direct improvements.
- **Footprint Analysis**: Displays brand mentions count on Reddit, Quora, and PR sites.
