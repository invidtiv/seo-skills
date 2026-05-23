---
name: blog-to-video
description: Use when turning a finished article or blog post into a YouTube video package — long-form titles, hooks, talking points, on-screen/B-roll cues, a slide deck to show while recording, short-form (Shorts/Reels/TikTok) scripts, chapters, description, and a paste-ready thumbnail image prompt — to repurpose written content into a recordable video.
---

# Blog-to-Video: Repurpose a Sourced Article into a Video Package

## Overview

Turns ONE finished, sourced article into a recordable video kit: ONE long-form YouTube video (3 title/hook options + one shared talking-point outline with on-screen cues + a source-carrying slide deck) and 3–5 standalone short-form clip scripts, plus optional chapters/description and a thumbnail handoff.

**Core principle:** The long-form video *is* the citation asset. AI answer engines cite long-form video heavily; they barely cite short-form. So the video must carry the article's sourced claims *with their attribution intact* — that is what makes the video itself citable. Short-form is reach and (for local businesses) a legitimacy signal, **not** a path to getting cited by AI. Repurposing that strips the sources produces reach without authority, which defeats the point.

**Input requirement:** a finished article, ideally a `cite-me` output (inline-sourced, capsule-structured). If the input has no sources, say so — you can still make the package but flag that its citation value is degraded.

## The Myth-Flip Guard (handle this FIRST, explicitly)

If the user frames short-form as the way to "get cited / picked up by AI search" (common, and wrong), correct it **up front as its own point, not a buried aside.** State plainly:

> AI answer engines overwhelmingly cite long-form (≈94% long-form; within social citations YouTube dominates and concentrates in Perplexity + Google AI Overviews; TikTok/IG/FB are a tiny fraction). Your **long-form video** is the citation play. Short-form drives humans and, for a local business, feeds the Google Maps "social updates" signal. It does not make AI quote your TikTok.

Then proceed. Do not let the rest of the package quietly imply the myth. (Brand constraint: do not name or show competing SEO tools on screen — DataForSEO exclusivity.)

## Hard Rules (these are what the baseline failed)

1. **Grounding — nothing the article doesn't say.** Every title, hook, talking point, and short must trace to a claim in the source article. No new stats, no invented urgency, no facts from memory. If it isn't in the article, it isn't in the package. (Carve-out: the Myth-Flip Guard text below is skill-supplied meta-framing about citation behavior — it is exempt from this rule and must NOT be attributed to the article.)
   - **Quantifier discipline:** use the article's own quantifier or none. Do not sharpen a fuzzy one ("a large share" → "most", "often" → "always", "can be denied" → "will be denied"). Tightening a vague quantifier into a punchier one is grounding drift, not just punchy copy — it is the most common escalation under "make it dramatic" pressure.
2. **Carry the attribution.** Sourced claims keep their source on the way into video. Long-form talking points name the source ("the IRS's own worked example", "DOE confirms…"). **Each short names its source at least once.** Stripped-source = not done.
3. **Match the source's credibility register — in words AND visuals.** Urgency comes from the facts, not hype words. If the article says "expires", the title/slide does not say "DIES" or "gone forever". This extends to slide copy and slide *styling*: red-alert color, "TRAP", "SCAM", "they're hiding this", scare framing on a giant slide is visual escalation — same failure as a clickbait word. Slides under "make it punchy/bold/dramatic" pressure are the highest-risk surface; hold the register and, if the user pushes for more drama than the source supports, say so rather than quietly complying. Curiosity and stakes are fine; overclaiming is not.
   - **Curiosity boundary (concrete test for slides/titles).** Curiosity framing is allowed only if it (a) points at a real gap the article itself names and (b) does not impute secrecy, malice, or victimhood. Apply the test: *would the article's own author say this sentence on record?* "The rule most people miss" passes (the article says "most homeowners miss"). "The rule they don't want you to know" / "Nobody tells you this" / "Don't get scammed" fail — they add a villain the article never claims. Deliver drama through type SCALE and CONTRAST, not escalated words.
4. **All 3 titles root in the article's strongest differentiator / contrarian angle.** Find the article's non-obvious moat (the thing vendor content omits) and anchor every title variant in it. Do not let one variant regress to a generic "how X works" that throws away the differentiator.

## Output Spec

### Part 1 — One long-form video

Identify the article's spine and its single strongest differentiator (the contrarian/most-omitted point) first; state it in one line.

- **3 title options**, each with a **hook** (the spoken first ~10–15 seconds). All 3 anchored in the differentiator; vary the *angle* (e.g. contrarian, cost-of-inaction, the-thing-everyone-misses), not the topic. Titles obey rule 3 (no escalation past source).
- **One shared talking-point outline** (the variants are alternate doors into the same video). Follow the article's section spine in order. Each talking point: the claim **+ its source attribution** + the concrete number/date from the article. End on the article's strongest action.
- Note coverage: if the video outline intentionally omits article sections (e.g. deep business/edge-case detail), say so in one line rather than silently dropping them.

### Part 2 — 3–5 standalone short-form scripts

One short per major article section/claim. Cap at 5; if the article has more, pick the 5 with the strongest standalone hook. Each short is **siloed** — one claim, no overlap with the others. Per short:

- **Hook** (1 line, the scroll-stopper — dramatize the stake, never assert past the source)
- **Talking points** (3–5 bullets, the one claim with its specifics)
- **Source line** (the article's source, named once — the citation through-line)
- **On-screen text** (1–2 short overlays: the number/date that does the work)
- **CTA** (drive to the long-form / article — that is where the citation value lives)

### Part 3 — Recording kit (this is what gets the user to camera)

**3a. On-screen / B-roll cue column.** Add to every long-form talking point a concrete cue: exactly what is on screen while that point is said. Concrete, not vague — name the asset and its URL: "screen-record the IRS GEOID lookup at <url from article>", "hold slide 4", "show the article's cost table". If a needed asset's URL is **not in the article**, write "find the official <thing> (confirm URL)" and flag it — never fabricate a URL.

**3b. Slide spec (always produced).** One slide per long-form talking point, in spine order. Per slide:
- **Headline** — the point, in the article's register (see hard rule 3 — this applies to slide copy too)
- **The one number/date** that does the work (from the article)
- **Source line** — the article's source for this slide. **Every slide carries its source. A slide with no source is a failed slide** (this is the citation asset being built on screen — non-negotiable).
- **Spoken line** — one sentence of what the host says over it (a guide, not a teleprompter read)
No duplicate-claim slides. If a slide intentionally omits an article section, say so (coverage note extends to slides).

**3c. Optional HTML render (Claude Code).** If the user wants the deck rendered, hand the slide spec to the `frontend-design` skill with these **slide constraints explicitly in the brief** (not generic web layout): 16:9, one idea per slide, viewport-huge type, dark high-contrast theme, **source line persistent on every slide**, a reserved bottom webcam corner, keyboard advance, fullscreen-ready. Require a contrast/legibility check — do not assert "webcam-readable" without it. The portable-prompt version emits the spec only ("paste into Gamma/Canva, or ask your AI to render these as a 16:9 HTML deck").

**3d. Timing.** Map segments to a runtime **only from a target length the user gives or a stated assumption** ("assuming a ~10-min video"). Estimates are labeled estimates. Never fabricate to-the-second timestamps as if grounded.

### Part 4 — Publish block (optional, compact — offer, don't force)

Offer; produce only if wanted. Keep it tight:
- **Chapters** — timestamp + label from the segment spine (estimate-labeled per 3d)
- **Description** — 2–3 sentences from the article's spine, no claims the article lacks
- **CTAs** — the channel standard: AI Search Starter Kit `https://www.airankingskool.com/you-came-here-from-socials` and Skool `https://skool.com/ai-ranking` (the Starter Kit path must stay `/you-came-here-from-socials`)
- **Thumbnail prompt** — see the dedicated section below (this is the lead-magnet payoff, not a hand-off).

**Full spoken teleprompter script: on request only.** Default is points + cues (the host ad-libs). Offer the full script; generate it only if asked. When generated, it still obeys every hard rule.

## Thumbnail Prompt (Part 4b — produce 2, paste-ready)

Goal: the user pastes ONE generated prompt **plus a photo of their own face** into gpt-image-2 or Nano Banana Pro and gets a finished, professional 1280×720 thumbnail. Output **2 variants** (A: solid brand-color background; B: softly blurred neutral workspace). Model-agnostic plain prose, no model-specific syntax. End with a one-line usage instruction. **"Professional, not over the top" is a hard constraint, not a style preference** — restraint IS the credibility signal (matches this channel's whole value).

Each prompt MUST contain, in plain prose:

1. **Likeness lock (non-negotiable, first line).** "Use the attached photo as the exact reference for this real person. Keep their face, bone structure, skin tone, hair, glasses, age and **their expression** exactly as in the photo. Do not beautify, de-age, restyle, swap, or generate a different person." **Do not prescribe an emotion** (no "make them look concerned/shocked/excited") — imposing an expression is a likeness override. If the user wants a specific look they re-shoot the photo.
2. **Composition.** Person on one side (left or right), cut mid-chest, occupying ~45–55%, clean separation from background.
3. **Background — one of three restrained patterns ONLY. Never an invented literal scene** (no "suburban garage with an EV charger" — that reads as AI stock and blends in): (A) a solid brand-color field; (B) a softly blurred, generic modern workspace with subtle accent lighting; (C) a clean light pastel gradient.
4. **Palette: 2–3 colors total.** Background tone + white or near-black text + at most one accent. Name exact tones. Explicitly forbid neon, rainbow, oversaturation.
5. **Text: 1–3 words, huge, bold geometric sans-serif**, title-safe margins, not over the face. It **complements the chosen title, never duplicates it, and does not reuse the title's key phrase** (if the title says "Hidden Address Rule", the thumbnail does not say "ADDRESS RULE" — pick a different angle/word). Title states the tension → thumbnail gives the payoff/action. Obeys the skill's register + curiosity-boundary rules (no "SCAM/SHOCKING", no number or claim the article lacks). An article-TRUE element (a real figure or the real tool from the article) is allowed but optional; if a number is shown it must keep its article meaning — do not strip the qualifier so it flips sense (article "capped at $1,000" must not become a bare "$1,000" that reads as "you get $1,000"; pair it with the qualifying word or don't use it).
6. **At most ONE graphic device total** (a single arrow OR one small accent banner OR one underline OR one clean product wordmark/icon) — or none. More than one = clutter = reject.
7. **Expression/energy:** natural and credible, as in the photo. Explicitly forbid exaggerated open-mouth shock, finger-on-face clickbait, AI-mangled hands/fingers, watermark, border, caption bar.
8. **Spec line:** photorealistic, 16:9, 1280×720, readable at 320px wide.

Under "make it pop / dramatic / get clicks" pressure: hold the restrained spec AND **disclose the trade-off in one line** ("kept this credible because that's the channel's edge; variant B is the slightly punchier safe option") — never silently over-escalate, never silently override the user.

**Optional (Claude Code only):** offer to render variant A or B now via the `nano-banana-pro` or `gpt-image-2` skill if the user gives a photo path. Default deliverable is still the paste-ready prompt text (the lead-magnet artifact). The portable-prompt version emits the 2 prompts + usage line only.

## Hook Patterns (self-contained — pick per variant)

| Pattern | Shape | Use when |
|---|---|---|
| Contrarian / myth-flip | "Everyone says X. The data says the opposite." | Article overturns a common belief |
| The thing everyone misses | "The real trap isn't X, it's Y." | Article has a buried disqualifier/gotcha |
| Cost of inaction | "Miss this one thing and [concrete loss]." | Article has a deadline / irreversible stakes |
| Receipts | "Here's the real math, using their own numbers." | Article has a worked example / hard figures |

Stakes come from the article's actual facts. A hook that needs a fact the article doesn't contain is disqualified.

## Verification Pass (before delivering)

Scan the package. Fail and fix if ANY:
- A claim/number/date not present in the source article
- A title/hook tonally escalated past the source ("dies/gone forever" where source says "expires")
- A quantifier sharpened past the source ("most" where source says "a large share"; "will" where source says "can")
- A short with no source named
- A title variant that abandoned the differentiator for a generic angle
- The user raised the AI-cites-short-form premise and it was not corrected up front
- Short-form copy that implies AI will cite the short itself
- **Any slide with no source line** (non-negotiable)
- Slide copy or styling escalated past source (red-alert color, "TRAP/SCAM", scare framing)
- Timing given as fabricated to-the-second timestamps rather than a labeled estimate from a stated target
- A slide deck that silently drops article sections with no coverage note
- A fabricated asset URL in a cue (vs "find official X (confirm URL)")
- A thumbnail prompt missing the likeness-lock first line, or prescribing an expression not in the photo
- A thumbnail with an invented literal scene background, >3 colors, >3 words, or >1 graphic device
- A thumbnail claim/number not in the article, text duplicating or reusing the title's key phrase, or a real number stripped of its qualifier so it flips meaning
- Over-escalation under "make it pop" with no disclosed trade-off, or silent override of the user

## Red Flags — STOP

- "Punchier title = drop the nuance" → escalation past source is the clickbait failure. Anchor in fact.
- "They want AI citations from Shorts, I'll just give them Shorts" → correct the myth first; the long-form is the asset.
- "This extra stat would make it stronger" → not in the article = not in the package. Strengthen from the article only.
- "Shorts are short, skip the source" → each short names its source once. Non-negotiable.
- "They asked for bold/punchy slides, so red-alert + TRAP is what they want" → visual escalation is the same failure as a clickbait word. Hold register, disclose the trade-off.
- "A slide is too small for a source line" → a sourceless slide is a failed slide; it's the citation asset on screen.
- "I'll estimate timing to the second so it looks precise" → false precision presented as grounded. Label estimates; require a target length.

## Rationalization Table (from baseline)

| Excuse | Reality |
|---|---|
| "'Dies/gone' is just punchy copy" | It escalates past the source and erodes credibility — the channel's whole value. Use the source's register. |
| "The AI-search pushback can be a one-liner preamble" | It's the user's core (wrong) premise. Correct it up front as its own point, or the package reinforces the myth. |
| "One generic title gives variety" | All 3 must root in the differentiator. Generic = vendor-tier, throws away the moat. |
| "Attribution is too long for a Short" | One source mention per short. That's the through-line that makes video a citation asset. |
| "I'll add a helpful extra fact" | Grounding rule: article-only. Invented facts kill the citation chain. |
| "'A large share' → 'most' is just sharper, not new" | Quantifier escalation IS grounding drift. Use the article's quantifier or none. |
| "Bold slides means red-alert + TRAP framing" | Visual escalation = clickbait failure on the biggest surface. Source register applies to slide copy and color. |
| "Source won't fit on the slide" | Sourceless slide = failed slide. The on-screen source IS the citation asset. |
| "Timestamps to the second look more pro" | Fabricated precision. Estimate from a stated target, labeled as an estimate. |
| "Curiosity framing, so 'Nobody tells you this' is fine" | Curiosity may not add a villain. Test: would the article's author say it on record? If it implies secrecy/malice, it fails. |
| "Thumbnail should pop, so shocked face + neon + a scene" | Restraint is the credibility signal. Likeness-lock, ≤3 colors/words, one device, no invented scene. Disclose the trade-off; don't override silently. |
| "I'll make them look concerned for drama" | Imposing an expression is a likeness override. Keep the photo's expression; don't prescribe an emotion. |
| "A garage-with-charger background sells it" | Invented literal scenes read as AI stock and blend in. Use a solid color / blurred workspace / pastel gradient only. |
| "Reuse the title's strong phrase on the thumbnail" | That's duplication. Thumbnail takes a different angle/word than the title. |
| "Bare '$1,000' is article-true so it's fine" | Stripping "capped at" flips its meaning. Keep the qualifier or drop the number. |
| "I'll just invent the Form/tool URL for the cue" | Never fabricate an asset URL. "Find official X (confirm URL)" and flag it. |
