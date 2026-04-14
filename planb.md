---
title: UX Review — User Journey Complexity Audit
date: 2026-04-14
---

# UX Review: Is Distillary Easy to Use?

An honest assessment of every user journey — what's simple, what's complex, and what needs simplification.

## Journey 1: First book → brain

**What the user says:** "Add books/my-book.epub to my brain"

**What actually happens (11 steps):**

| Step | Who does it | User action needed | Complexity |
|---|---|---|---|
| 1. Extract text | Claude | None | Hidden |
| 2. Ask about chunks | Claude | Answer "yes" or "no" | Simple |
| 3. Extract claims | Claude (parallel agents) | Wait ~2 min | Waiting |
| 4. Dedupe | Claude | Wait ~1 min | Waiting |
| 5. Entities | Claude | Wait ~1 min | Waiting |
| 6. Entity-link | Claude | Wait ~1 min | Waiting |
| 7. Group + pyramid | Claude | Wait ~5 min | Waiting |
| 8. Verify (optional) | Claude | None | Hidden |
| 9. Assemble | Claude | None | Hidden |
| 10. Post-process | Claude | None | Hidden |
| 11. Done | Claude | Open in Obsidian | Simple |

**User effort:** 1 sentence + wait + open Obsidian. No questions asked — chunks always stored.
**Verdict:** Very simple. The pipeline is complex but the user experience is one command.
**Issue (fixed):** Progress updates now shown at every step.

---

## Journey 2: Ask a question

**What the user says:** "Research: what does the brain say about integrity?"

**What actually happens:**

| Step | Who does it | User action needed |
|---|---|---|
| 1. Research agent launches | Claude | None |
| 2. Agent searches, follows links | Claude | Wait ~3-5 min |
| 3. Answer written to file | Claude | Read the file |

**User effort:** 1 sentence + wait + read.
**Verdict:** Simple.
**Issue:** The output file path is long (`brain/personal/research/integrity.md`). User needs to know where to look.
**Fix suggestion:** Print the file path clearly after completion, or open it automatically.

---

## Journey 3: Add a second source + see bridges

**What the user says:** "Add books/second-book.epub to my brain"

**What happens:** Same as Journey 1, PLUS:

| Extra step | Who | User action |
|---|---|---|
| Concept-mapper runs | Claude | Wait ~3 min |
| Bridge-builder runs | Claude | Wait ~3 min |
| Analytics regenerated | Claude | Wait ~2 min |
| Brain index updated | Claude | None |

**User effort:** Same 1 sentence. Bridges appear automatically.
**Verdict:** Simple — the user doesn't need to do anything extra.
**Issue:** The user might not know bridges were created. No notification like "Found 9 bridge concepts between your two sources."
**Fix suggestion:** Report bridge findings after completion.

---

## Journey 4: Add an external brain

**What the user says:** "Add brain at https://someone.github.io/their-brain/"

**What happens:**

| Step | Who | User action |
|---|---|---|
| 1. Fetch agent.json | Claude | None |
| 2. Add to brains.yaml | Claude | None |
| 3. Confirm | Claude | None |

**User effort:** 1 sentence.
**Verdict:** Very simple.
**Issue:** User needs to know the URL. No discovery mechanism ("find brains about philosophy").
**Future idea:** A brain registry where people publish and discover brains.

---

## Journey 5: Clone + map a published brain

**What the user says:** "Clone brain from https://... then map concepts with my brain"

**What happens:**

| Step | Who | User action |
|---|---|---|
| 1. Clone (fetch pages) | Claude | Wait ~2 min |
| 2. Add to brains.yaml | Claude | None |
| 3. Run concept-mapper | Claude | Wait ~3 min |
| 4. Report bridges | Claude | Read results |

**User effort:** 1 sentence (or 2 if separated).
**Verdict:** Moderate — user needs to understand clone-then-map pattern.
**Issue:** Two concepts to understand: "clone" and "map." Could be one command.
**Fix suggestion:** "Compare my brain with https://..." → auto-clones if needed, then maps.

---

## Journey 6: Fact-check a claim

**What the user says:** "Verify the claims in brain/sources/ecc-2024/"

**What happens:**

| Step | Who | User action |
|---|---|---|
| 1. Verify agent reads claims | Claude | None |
| 2. Reads chunk files | Claude | None |
| 3. Compares passages | Claude | None |
| 4. Writes report | Claude | Read report |

**User effort:** 1 sentence + read.
**Verdict:** Simple IF chunks are stored. If not, the agent reports "chunks not available" — user needs to understand why.
**Verdict:** Simple. Chunks always present locally, verify always works.


---

## Journey 7: Create a new brain from scratch (regulatory docs)

**What the user says:** "Create a new brain from books/security-frameworks/"

**What happens:**

| Step | Who | User action |
|---|---|---|
| 1. Scan directory for files | Claude | None |
| 2. Ask about chunks | Claude | Answer yes/no |
| 3. Extract all sources | Claude | Wait ~5-10 min |
| 4. Dedupe + entities | Claude | Wait |
| 5. Entity-link | Claude | Wait |
| 6. Group per source | Claude | Wait ~10 min |
| 7. Pyramid per source | Claude | Wait |
| 8. Analytics + concept-mapper | Claude | Wait |
| 9. Bridge-builder | Claude | Wait |
| 10. Write index | Claude | None |
| 11. Done | Claude | Open in Obsidian |

**User effort:** 1 sentence + 1 answer + long wait.
**Verdict:** Simple input, but the wait is 20-30 minutes for a multi-source brain. No progress.
**Issue:** Long wait with no visibility. User doesn't know if it's stuck or working.
**Fix suggestion:** Real-time progress updates. "Processing source 3/12: CSCC (86 claims extracted)."

---

## Journey 8: Generate a presentation from research

**What the user says:** "Make a presentation about our NCA compliance"

**What happens:** This is currently NOT a single command. The user went through:

1. Run deep research
2. Read the output
3. Ask for a presentation
4. Review
5. Ask for team version
6. Review
7. Ask for domain details
8. Ask for sync
9. Ask for interactivity

**9 back-and-forth exchanges** to get from question to final deliverable.

**User effort:** High — multiple iterations, manual review, corrections.
**Verdict:** Complex. This is the hardest journey.
**Issue:** No single command produces a polished output. The user has to guide the process.
**Future idea:** A `distillary-present` skill that takes a research output and generates a presentation with one command. Or a `distillary-report` skill for audit-ready documents.

---

## Complexity Scorecard

| Journey | Steps for user | Wait time | Complexity | Rating |
|---|---|---|---|---|
| Add first book | 1 (command only) | 10-15 min | Very low | Excellent |
| Ask a question | 1 (command) | 3-5 min | Low | Good |
| Add second source + bridges | 1 (command) | 15-20 min | Low | Good |
| Add external brain | 1 (command) | 10 sec | Very low | Excellent |
| Clone + map published brain | 1-2 (commands) | 5 min | Moderate | OK |
| Fact-check claims | 1 (command) | 2-3 min | Low | Good |
| Create new brain from docs | 2 (command + chunks) | 20-30 min | Low (but long wait) | OK |
| Generate presentation | 5-9 (iterations) | 30+ min | High | Needs work |

## Top Pain Points

### 1. No progress visibility during pipeline

The user types one command and waits 10-30 minutes with no feedback. They don't know if it's working, stuck, or almost done.

**Current:** "Add this book" → silence for 15 minutes → "Done!"
**Should be:** "Add this book" → "Extracting (chunk 3/8)..." → "Deduping (78 claims)..." → "Grouping into 7 clusters..." → "Done! 78 claims, 7 clusters, 14 entities."

### 2. Presentations require too many iterations

Going from "I need a compliance presentation" to a finished HTML with interactive filters took 9 exchanges. There's no skill that does this in one shot.

**Suggestion:** A `distillary-present` skill:
```
"Present: NCA compliance posture for government client"
→ reads research output
→ generates HTML presentation
→ one command
```

### 3. Output file locations are unpredictable

Research goes to `brain/personal/research/`. Presentations end up wherever the user asks. The user has to remember paths or ask where things are.

**Suggestion:** Always print the output path. Consider a `distillary-outputs` command that lists recent outputs.

### 4. ~~The chunks choice question~~ ELIMINATED

Chunks are now always stored locally — no question needed. Copyright is handled at publish time only. One fewer question in the most common workflow.

### 5. No undo for failed extractions

If an extraction produces garbage (bad OCR, wrong language), there's no "undo" or "re-extract this source." The user has to manually delete files and re-run.

**Suggestion:** A `distillary-redo` skill: "Redo extraction for brain/sources/shafii-resala/" → deletes old claims, re-runs extract agents.

### 6. brains.yaml is manual

Adding a local brain requires the user to know the path or say the command. There's no "scan for brains in my projects" feature.

**Suggestion:** Auto-discover brains in common locations (sibling directories, home folder) and suggest adding them.

## What's Already Good

- **One command to add a source** — the pipeline complexity is hidden
- **One command to ask a question** — deep research happens automatically
- **Bridges appear automatically** — no manual concept mapping needed
- **Evidence grading is automatic** — backing/strength/warrant extracted without user effort
- **Published brains via URL** — one command to connect
- **Interactive presentations** — click tasks to mark done, progress persists

## Simplification Priorities

| Priority | What to do | Impact | Effort | Status |
|---|---|---|---|---|
| 1 | Progress updates during pipeline | High — removes anxiety | Medium | **DONE** — add-source skill now has step-by-step messages + completion summary |
| 2 | `distillary-present` skill | High — eliminates iteration | Medium | Future |
| 3 | Print output paths after every operation | Medium — reduces confusion | Low | **DONE** — research skill prints path + confidence + stats after completion |
| 4 | ~~Smart chunks defaults~~ | ~~Low~~ | ~~Low~~ | **ELIMINATED** — chunks always stored locally, no question asked. Copyright only at publish time. |
| 5 | `distillary-redo` skill | Medium — recovery from bad extraction | Low | **DONE** — "redo extraction" cleans old claims, re-runs pipeline from chunks |
| 6 | Brain auto-discovery | Low — convenience | Low | Future |
