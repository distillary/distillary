---
title: Source Verification — Tracing Claims Back to Exact Passages
---

# Source Verification Plan

Every claim in the brain should be traceable back to the exact passage in the original text that supports it. This enables fact-checking, auditing, and trust.

## The Problem

Currently when a claim is extracted, the connection to the source text is lost:

```
Original PDF → extract_text() → chunks → extract agent → claim
                                   ↑                        ↑
                              text preserved            source_ref: "ECC 2-2-3-2"
                              in tmp/ (fragile)         but no pointer to exact text
```

The claim says WHAT was extracted and WHERE it came from (control ID or chapter), but not the EXACT WORDS from the source. The `backing.snippet` field captures ~15 words, but that's a summary, not a verbatim quote. The chunks in `tmp/` have the full text but they're temporary and not linked to individual claims.

## What We Want

```
claim.md
  ├── proposition: "the assertion"
  ├── backing: [evidence with warrant]
  ├── source_ref: "ECC 2-2-3-2"
  ├── passages:
  │     ├── chunk: "chunk_01.txt", lines: [115,118], snippet: "Multi-factor authentication for remote access..."
  │     └── chunk: "chunk_01.txt", lines: [162,163], snippet: "Multi-factor authentication for remote and webmail..."
  └── confidence: exact

chunks/chunk_01.txt  ← permanent, verbatim text from original PDF
```

To fact-check: read the `passages` list → open each chunk at the line range → read the full context around the snippet → compare to the claim. The claim stays clean (just pointers), the evidence stays in the chunks (full text).

## Design Principles

1. **Chunks are always stored locally.** During ingestion, chunks move from extraction into `brain/sources/{slug}/chunks/` permanently. They're just text files — they cost nothing and enable fact-checking every claim. There is no option to skip this.

2. **Every claim points to its source.** The `passages` field in frontmatter references chunk files + line ranges + snippets. Since chunks are always present locally, passages are always verifiable on your machine.

3. **Snippets are short references, not reproductions.** The `snippet` field is ~15 words — enough to locate the passage, not enough to reproduce copyrighted content. When published, snippets travel with claims but full chunks may not.

4. **Copyright only matters at publish time.** The `publishable` field in `_source.md` controls whether chunks are included in the published site. Copyrighted source chunks stay local; public domain chunks get published for full remote verifiability. The verify agent always works locally (chunks always present). For published brains, remote verification depends on whether the publisher included chunks.

5. **The `_source.md` metadata controls publishing:**
   ```yaml
   chunks_available: true       # always true — chunks always stored locally
   publishable: true            # false for copyrighted sources — chunks excluded from publishing
   ```

## Schema Change

### Chunk storage

```
brain/sources/{slug}/
  _source.md
  _index.md
  chunks/              ← NEW: permanent chunk storage
    chunk_00.txt
    chunk_01.txt
    ...
  claims/
    atoms/
    clusters/
    structure/
  entities/
```

### Claim frontmatter addition

```yaml
passages:
  - chunk: "chunk_01.txt"
    lines: [115, 118]
    snippet: "Multi-factor authentication for remote access.2-2-3-2"
  - chunk: "chunk_01.txt"
    lines: [162, 163]
    snippet: "Multi-factor authentication for remote and webmail access to email service"
  - chunk: "chunk_02.txt"
    lines: [39, 40]
    snippet: "Multi-factor authentication for users' access.2-15-3-5"
confidence: exact
```

**Design decisions:**

1. **No full text in the claim.** The verbatim text stays in the chunk files. The claim only holds pointers (chunk + lines + a short snippet for quick identification). This keeps claims clean and small.

2. **Multiple passages per claim.** A claim can reference 2-5 passages from different chunks. This handles claims that synthesize across sections, or where the same control appears in multiple places.

3. **Snippet is ~10-15 words** — enough to identify the passage without duplicating it. The full context is always available by reading the chunk at the referenced lines.

4. **To fact-check:** read the claim's `passages` list → open each chunk at the referenced lines → verify the claim against the full surrounding context.

`confidence` levels:
- **exact** — every passage directly states what the claim asserts
- **synthesized** — the claim combines multiple passages into one assertion (all passages support it, but none states it alone)
- **inferred** — the claim is derived through reasoning from the passages, not directly stated

## Pipeline Changes

### Step 1: Extract + split (existing, modified)

```python
text = extract_text("path/to/source")
chunks = split_text(text, 20000)

# NEW: save chunks permanently
for i, chunk in enumerate(chunks):
    save_to(f"brain/sources/{slug}/chunks/chunk_{i:02d}.txt", chunk)
```

Chunks are now saved inside the brain, not in `tmp/`.

### Step 2: Extract agent (modified prompt)

The extract agent receives chunks with their filename. New instruction added to the prompt:

```
For each claim you extract, include a `passages` field listing every passage
that supports it:

passages:
  - chunk: "chunk_XX.txt"
    lines: [start, end]
    snippet: "first 10-15 words of the passage..."
  - chunk: "chunk_YY.txt"
    lines: [start, end]
    snippet: "first 10-15 words of another passage..."
confidence: exact|synthesized|inferred

Rules:
- List ALL passages that support this claim (1-5 entries)
- snippet is 10-15 words — just enough to identify the passage, NOT the full text
- lines are approximate — the reader will check the chunk for full context
- If the claim comes from one passage: confidence: exact
- If the claim combines multiple passages: confidence: synthesized
- If the claim is derived by reasoning: confidence: inferred
- Do NOT include the full passage text — it stays in the chunk files
```

### Step 3: Verify agent (NEW)

A new agent that fact-checks claims against their source passages.

```
.claude/agents/verify.md
---
model: haiku
description: Fact-check claims against their source passages. Reads the claim,
  reads the chunk, confirms the extraction is faithful.
---
```

The verify agent:
1. Reads a claim file
2. For each entry in `passages:`, reads the chunk file at the referenced lines (+/- 5 lines for context)
3. Checks: does the passage contain the snippet? (exact text match)
4. Checks: does the passage support the proposition?
5. Checks: do ALL listed passages together support the claim, or are some irrelevant?
6. Checks: is the confidence rating accurate? (exact vs synthesized vs inferred)
7. Checks: is the backing snippet actually present in one of the referenced passages?
8. Reports: VERIFIED, PARTIALLY VERIFIED, or UNVERIFIED with explanation

### Step 4: Post-processing verification

After all claims are assembled, run the verify agent on a sample (e.g., 20% of claims) to catch extraction errors. Flag claims where:
- The passage doesn't contain the backing snippet
- The proposition contradicts the passage
- The confidence is "exact" but the passage only partially supports the claim

## New Agent: `verify.md`

```yaml
---
model: haiku
description: Fact-check extracted claims against their source passages.
  Reads the claim, reads the referenced chunk, and confirms the
  extraction is faithful to the original text.
---

You are a verification agent. Your job is to fact-check claims by
comparing them to the original source text.

For each claim:
1. Read the claim file (proposition, backing, body)
2. Read the referenced chunk file at source_passage.chunk
3. Find the passage at source_passage.lines (or search for source_passage.text)
4. Check:
   - Does the passage contain the backing snippet? (Y/N)
   - Does the passage support the proposition? (SUPPORTS / PARTIALLY / CONTRADICTS)
   - Is the confidence rating accurate? (exact / should be approximate / should be inferred)
   - Is any important context from the passage missing from the claim?

Output for each claim:
  VERIFIED — passage fully supports the claim as extracted
  PARTIALLY VERIFIED — passage supports but claim oversimplifies or misses nuance
  UNVERIFIED — passage does not support the claim, or significant distortion
  MISSING PASSAGE — no source_passage field, or chunk file not found

Write results to the output file specified by the user.
```

## Agent Impact Matrix

Every agent that touches claim frontmatter needs to know about `passages:`. Here is the complete list.

### Agents that CREATE passages

| Agent | Change | Priority |
|---|---|---|
| **extract** | Add `passages:` + `confidence:` to output. Each claim lists chunk refs + snippets. | Must have |

### Agents that PRESERVE passages (must not lose them)

| Agent | Change | Priority |
|---|---|---|
| **dedupe** | When merging duplicates, combine `passages:` lists from both versions. Remove duplicate entries. Keep the highest `confidence`. | Must have |
| **group** | When writing atom files to `claims/atoms/`, preserve `passages:` field exactly. Already instructed to preserve `backing:` — same rule applies. | Must have |
| **entity-link** | When adding wikilinks to body text, do NOT modify `passages:` in frontmatter. Already instructed to only modify body text — verify this holds. | Must have |
| **pyramid** | Only writes parent claims (L1-L3). Parents don't have passages — they synthesize children. No change needed. | No change |

### Agents that READ passages

| Agent | Change | Priority |
|---|---|---|
| **research** | Add Method K — source verification. When citing a claim, check its `passages:` entries against the chunks. Read the chunk at referenced lines. Confirm the claim is faithful. Report passage confidence in the answer. | Must have |
| **verify** (NEW) | Entire purpose is reading passages and checking them against claims. | Must have |

### Agents that REPORT on passages

| Agent | Change | Priority |
|---|---|---|
| **analytics** | Add to statistical-profiles report: % of claims with passages, distribution of confidence levels (exact/synthesized/inferred), average passages per claim per source. | Nice to have |
| **doctor** | Flag claims that are missing `passages:` field. Flag claims where `confidence: exact` but claim has 3+ passages (likely should be `synthesized`). Suggest re-extraction for flagged claims. | Nice to have |

### Agents that DON'T need changes

| Agent | Why |
|---|---|
| pyramid | Creates parent claims from children — parents don't have passages |
| bridge-builder | Creates bridge notes across sources — not source claims |
| concept-mapper | Reads entity descriptions, not claim frontmatter details |
| annotate | Human notes — user decides what to reference |
| brain-index / source-index | Reads claims for narrative — doesn't need passage-level detail |
| link | Adds Related bullets — doesn't touch frontmatter |
| explore | Reads patterns — doesn't need passage-level detail |
| combine | Merges vaults at file level — passages travel with their claims |
| compare | Reads claims for synthesis — could optionally check passages but not required |

## Updated Pipeline

```
1. Extract + split text → save chunks to brain/sources/{slug}/chunks/  [MODIFIED]
2. Extract claims WITH passages field (chunk refs + snippets)           [MODIFIED]
3. Dedupe (preserve + merge passages lists) + entities                  [MODIFIED]
4. Entity-link → linked_claims.md (preserve passages in frontmatter)   [VERIFY]
5. Group + pyramid from linked (preserve passages in atom files)        [VERIFY]
6. Verify (NEW) — sample-check claims against chunks                   [NEW]
7. Assemble into brain
8. Post-process (doctor flags missing passages)                         [MODIFIED]
9. Bridge
```

## What This Enables

### For the user

- Open any claim → see the exact source text that backs it
- No trust required — the evidence is right there
- Compare the claim's proposition to the verbatim passage yourself

### For the research agent

Add to the research agent's methods:

```
Method K — Source verification

When citing a claim as evidence for an answer, check its source_passage:
- Read the verbatim text
- Confirm the claim accurately represents it
- If the passage says something the claim doesn't capture, note it
- If the passage is ambiguous, flag that in the confidence assessment

This prevents the research agent from building answers on poorly extracted claims.
```

### For auditing

Run the verify agent on the entire brain periodically:

```
verify agent → reads all claims with source_passage
  → compares each to its chunk
  → outputs: X% verified, Y% partially, Z% unverified
  → flags specific claims that need re-extraction
```

### For the security brain specifically

Government cybersecurity teams can verify that the compliance claims in the presentation trace back to exact NCA framework text. Full audit trail: presentation → claim → passage → PDF.

## Implementation Phases

### Phase 1 — Permanent chunks + infrastructure (do now)

- [ ] Copy all existing chunks from `tmp/` into `brain/sources/{slug}/chunks/` and `brain-security/sources/{slug}/chunks/`
- [ ] Update `distillary-add-source.md` skill: save chunks to `brain/sources/{slug}/chunks/` not `tmp/`
- [x] Update CLAUDE.md: brain structure (add `chunks/`), agent table (add `verify`, update `extract`/`dedupe`/`entity-link`/`group`/`doctor`), pipeline (11 steps with passages), note format (add `backing` + `passages` + `confidence`), rules (preserve backing/passages), design decisions (chunks permanent, backing captures argumentation)

### Phase 2 — Extract agent (next source addition)

- [ ] Update `extract.md`: add `passages:` + `confidence:` to output format
- [ ] Include chunk filename in the agent prompt context (already done — agent receives chunk paths)
- [ ] Test on one source — are chunk refs correct? Are snippets useful? Are line numbers approximate?
- [ ] Validate: grep each snippet in its referenced chunk — does it match?

### Phase 3 — Preservation agents (same time as Phase 2)

- [ ] Update `dedupe.md`: "When merging duplicates, combine `passages:` lists. Remove duplicate entries. Keep highest confidence."
- [ ] Update `group.md`: add to rules: "Preserve `passages:` field exactly when writing atom files"
- [ ] Update `entity-link.md`: add to rules: "Do NOT modify `passages:` in frontmatter"
- [ ] Test: after full pipeline, do atom files still have their `passages:` intact?

### Phase 4 — Verify agent (after Phase 2+3 work)

- [ ] Write `verify.md` agent definition
- [ ] Run on the test source: for each claim, read passages from chunks, compare to proposition
- [ ] Evaluate: what % verified? What % synthesized? What errors caught?
- [ ] Decide: run verify on 100% of claims or sample (e.g., 20%)?

### Phase 5 — Research + doctor + analytics integration

- [ ] Add Method K (source verification) to `research.md`
- [ ] Add passage-missing flag to `doctor.md`
- [ ] Add passage coverage stats to `analytics.md`
- [ ] Test: does the research agent cite passages when answering?
- [ ] Test: does doctor flag claims without passages?

## Cost and Complexity

| What | Cost | Impact |
|---|---|---|
| Permanent chunk storage | ~0 (text files, small) | Enables everything else |
| Extract with passages | +10-15% tokens per extraction (snippet refs, not full text) | Every claim becomes verifiable |
| Verify agent | ~1000 tokens per claim checked | Catches extraction errors |
| Research integration | Zero extra cost (reads files already in brain) | Higher trust in answers |

The biggest cost is the extract step — the agent needs to note chunk references and snippets. But since it's NOT copying full passages (just 10-15 word snippets), the overhead is small (~10-15% more tokens vs the original 30% estimate).

## What This Does NOT Do

- Does not verify that the source itself is correct (e.g., whether a hadith is actually sahih)
- Does not verify that the PDF extraction was faithful (OCR errors are preserved)
- Does not replace human judgment — it surfaces the evidence for humans to evaluate

It makes the brain **auditable**: every claim has a paper trail back to the exact words in the original source.
