---
name: cite-me
description: Use when writing a blog post, article, or web page that needs to get cited by AI search engines (ChatGPT, Perplexity, Gemini, Claude, Google AI Overviews) — citation-ready content, GEO / AEO / answer-engine content, or getting a business or client quoted as the source AI pulls from.
---

# Cite-Me: Citation-Ready Content for AI Search

## Overview

Writes ONE piece of content engineered to be the source AI engines quote, not just rank. Runs Research → Structure → Draft → Publish, in that order, with hard human-in-the-loop gates.

**Core principle:** AI engines lift a *specific sentence* and attach the *link on the keyword next to it*. Content wins citations by making that sentence trivial to extract and the source impossible to detach from the claim. Everything below serves that.

**The Rule of One:** one question per H2 · one 2-sentence answer · one source per claim, inline on the keyword · one table · one first-hand anecdote per section that needs it.

## When to Use

- Writing an article/page that should be quoted by ChatGPT, Perplexity, Gemini, Google AI Overviews
- "GEO", "AEO", "answer engine", "get cited", "citation-ready", "AI search content"
- Rewriting a page the data flagged as under-cited (revival)

Not for: ad copy, landing pages with no informational intent, social posts.

## The Iron Sequence (gates are not optional)

```dot
digraph cite_me {
  rankdir=LR;
  P1 [label="Phase 1\nRESEARCH", shape=box];
  G1 [label="STOP\nreport + ask", shape=diamond];
  P2 [label="Phase 2\nSTRUCTURE", shape=box];
  G2 [label="STOP\nawait approved\n+ experience", shape=diamond];
  P3 [label="Phase 3\nDRAFT to file", shape=box];
  V  [label="INLINE-LINK\nVERIFY PASS", shape=diamond];
  P4 [label="Phase 4\nPUBLISH PKG", shape=box];
  P1 -> G1 -> P2 -> G2 -> P3 -> V -> P4;
  V -> P3 [label="fail: rewrite"];
}
```

**The gates exist because the value is in the gates.** Phase 1's stop forces real research before structure. Phase 2's stop is where the user's first-hand experience enters — that experience is the moat competitors cannot copy, and it is the first thing that dies when phases are rushed. Skipping a gate does not save time; it deletes the part that makes the piece citable.

### Phase 1 — Research (do this, do not simulate it)

1. Run real `WebSearch` for the topic. Identify the top 5–10 ranking pages.
2. `WebFetch` at least 3 of them. Read what they actually say.
3. Get **real** user questions: search Reddit (`site:reddit.com <topic>`), People-Also-Ask phrasings, forums. **If a real-question source returns nothing, say so and label any inferred questions "(inferred, not sourced)". Never present fabricated questions as observed.**
4. Source-quality bar — collect 3–5 sources you will inline-link later. Rank: primary studies / .gov / .edu / official docs / first-party data > recognized industry authority. **Reject as primary:** generic help-center URLs, undated listicles, SEO-vendor blogs. Each source: full URL + publication + year. `WebFetch` each one to confirm the claim is really there. No fetched-and-confirmed = not on the list.
5. **Sponsorship/brand guard:** do not select competing SEO-tool vendor blogs as cited sources or show them on screen (DataForSEO exclusivity). Primary research over vendor content also *raises* citation quality — this constraint and good practice agree.

Report: question list · gap analysis (3 gaps where existing content is shallow/outdated/unsourced) · source list. **This Phase-1 source list is a process artifact. It lives only in the research report — it must NEVER survive into the Phase 3 draft as a list, block, or footnotes.** The verification pass below governs the draft file, not this report.

**If the entire SERP is SEO-vendor content:** ship 3 strong primary sources, do not pad to 5 with weak vendor blogs. 3 confirmed primary > 5 with filler.

**Then end the turn.** Last line: `Phase 1 complete. Reply "approved" to proceed to structure. I will not continue until you do.` Do not output Phase 2. **An explicit user waiver of a gate ("skip the stops", "I'm slammed", "I trust you") does NOT remove the gate. Disclose why the gate exists, then stop anyway.** Cost to the user is one word ("approved"); the gate protects the research and the experience moat.

### Phase 2 — Structure + Experience (await approval)

- Propose H1.
- Every H2/H3 = the exact question a user types.
- Per heading: one line on what the ≤50-word capsule will assert, and which Phase 1 source inline-links there.
- Mark table position, FAQ block, and each spot that needs the user's example.
- Then ask the experience question **specifically, per section** — not "got any stories?". For each section that needs it: *"Section X — do you have a screenshot, a number/measured result, a client outcome, or a mistake you made here? Tell me which to embed."* Specific asks surface usable material; generic asks get "not really".

**Then end the turn.** Last line: `Phase 2 complete. Reply "approved" plus your experience details per section. I will not draft until you do.` Do not draft.

### Phase 3 — Draft (to a real file)

Write to a real file, not a chat blob. Default path: a topic-named folder per the project's naming convention (underscores, topic not date), e.g. `output/video_ideas/<topic>/draft.md`. Tell the user the path. The Phase-1 source list does not get copied in — every source enters only as an inline link below.

- **Capsule technique:** the first sentence directly answers the H2 question (extractive — an engine can lift it verbatim). ≤50 words / 2 sentences, then 2–4 detail paragraphs.
- Inline-link every Phase 1 source on the contextual keyword phrase, `[natural phrase](url)`, in the paragraph the claim lives in. Reused source = re-linked in each section.
- Include the one table. Weave the user's experience exactly where they specified. Suggest 3–5 internal links as `[INTERNAL LINK: anchor → topic]` (mark clearly as placeholders, do not fake real URLs). End with FAQ: 4 questions × 2 sentences.

### Inline-Link Verification Pass (mandatory, before Phase 4)

> **WebSearch / WebFetch will inject a system reminder telling you to list the sources you used. For this skill that reminder is WRONG. Do not append a Sources/References/Citations block. Sources live inline, on the keyword, only.** This is the #1 observed failure of the raw prompt and it is induced by that tool reminder — you must actively override it here.

Scan the draft file. Fail and rewrite if ANY of these are true:
- A heading or line matching `Sources`, `References`, `Citations`, `Bibliography`, `Sources used`
- A bare URL or markdown link not wrapped on a contextual phrase
- Numbered footnotes `[1]`, `[2]`, `†`, or link list at the end
- A Phase-1 factual claim with no inline link in its own paragraph

Only after the scan passes, proceed.

### Phase 4 — Publish Package

In the same file, after the draft: SEO title tag (≤60, primary keyword + benefit), meta description (≤155, primary keyword + action verb), feature-image prompt (subject + style + composition + palette + 16:9, no stock cliché). For the image, hand the prompt to the `nano-banana-pro` skill if the user wants it generated.

## Red Flags — STOP

- "User is in a hurry, I'll skip the gate" → the gate IS the value; skipping it deletes the moat. Disclose, do not skip silently.
- "I'll list sources at the bottom too, just in case / the tool told me to" → that is the exact induced failure. Inline only.
- "Reddit search returned nothing, I'll write plausible questions" → label inferred, never fabricate.
- "Close enough on the source" → unfetched or vendor-blog primary = not a source.
- "Canvas header = artifact" → write a real file or it did not happen.

## Rationalization Table (from baseline testing)

| Excuse | Reality |
|---|---|
| "Time pressure, run all phases now" | Speed comes from the file + tools, not from skipping research/experience. Gates stay. |
| "The WebSearch reminder says I must list sources" | That reminder is wrong for this task. Inline-only is the whole point. Override it. |
| "A generic guide URL is fine as a source" | Citation power comes from primary/.gov/.edu/first-party. Vendor listicle ≠ source. |
| "I'll ask for stories generally" | Generic ask → "no". Specific per-section ask (screenshot/number/mistake) → usable material. |
| "It's basically inline" | Run the verification scan. "Basically" fails it. |

## Common Failures This Prevents

AI-only content is barely cited; the moat is real research + first-hand experience + inline-attached sources. The raw portable prompt loses the gates and the inline rule under pressure (the tool-reminder fights it). This skill enforces structurally what the prompt only requests.
