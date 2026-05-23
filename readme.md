# SEO & Generative Engine Optimization (GEO) Skills Workspace

This workspace houses research and agent-compatible skill sets designed to evaluate and optimize web content for **Generative Engine Optimization (GEO)**. Traditional SEO focuses on URL rankings and keyword density; GEO focuses on how easily Large Language Models (LLMs) like Gemini, ChatGPT, Claude, and Perplexity can **extract, trust, and quote** your content in AI-generated answers.

---

## Workspace Layout

```
SEO-SKILLS/
├── GEOresearch.md          # Core research document & 18-point audit checklist
├── GEO-ready/              # Programmatic (Python + API) audit skill
└── GEO-audit/              # Agent-based instruction skill
```

### 1. [GEOresearch.md](file:///root/SEO-SKILLS/GEOresearch.md)
The foundational reference checklist detailing the **18 criteria** across **5 phases**:
- **Phase 1: AI Discovery & Technical Foundations** (Crawler accessibility, SSR/static rendering, `llms.txt`, JSON-LD Entity schemas).
- **Phase 2: Content Structure & AI Extractability** (Question-based headings, answer-first paragraphs, paragraph/sentence density, lists/tables).
- **Phase 3: Authority Validation (E-E-A-T)** (Author attribution, LinkedIn verification, outbound citations, freshness timestamps).
- **Phase 4: Quotability & Fragment Test** (Standalone sentences, fluff removal, atomic glossaries).
- **Phase 5: Off-Site Consensus Strategy** (Reddit/Quora footprints, PR listings, AI Share of Voice).

---

## Audit Skills Compared

We provide two distinct methods to run audits depending on whether you want a programmatically calculated score or an agent-guided review.

| Feature | Programmatic: [GEO-ready](file:///root/SEO-SKILLS/GEO-ready/SKILL.md) | Agent-Instructional: [GEO-audit](file:///root/SEO-SKILLS/GEO-audit/SKILL.md) |
| --- | --- | --- |
| **Primary File** | [geo_audit.py](file:///root/SEO-SKILLS/GEO-ready/scripts/geo_audit.py) | [SKILL.md](file:///root/SEO-SKILLS/GEO-audit/SKILL.md) |
| **Execution** | Programmatic Python execution | Agent-driven manual checklist analysis |
| **APIs Used** | Gemini Developer API & Google Search API | None (uses native agent analytical reasoning) |
| **Credentials** | Requires `.env` configuration file | None required |
| **Key Output** | Numeric score (0-100) & JSON-LD validation | Score, checklist logs, and copy-pasteable HTML fixes |

---

## How to Run Audits

### Method A: Programmatic Audit (GEO-ready)
Best for automated pipeline checks or querying search footprints.

1. **Configure Environment**:
   ```bash
   cp /root/SEO-SKILLS/GEO-ready/resources/.env.example /root/SEO-SKILLS/GEO-ready/.env
   # Add your GEMINI_API_KEY and GOOGLE_SEARCH credentials to .env
   ```
2. **Execute Script**:
   ```bash
   python3 /root/SEO-SKILLS/GEO-ready/scripts/geo_audit.py <path-or-url> --report <output-report-path>
   ```

### Method B: Instruction-based Audit (GEO-audit)
Best for manual or inline edits. Ask the AI agent (Antigravity) to audit a file using the `geo-audit-verification` skill:
* *Example prompt:* `"Audit /path/to/page.html using the GEO-audit skill guidelines."*
The agent will read the file, score it against the checklist, and generate the copy-pasteable templates for any gaps found.
