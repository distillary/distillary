---
title: How It Works
---

# How Distillary works

## The insight

Every source (book, video, article, regulatory framework) has an argument structure: a central thesis supported by a hierarchy of claims backed by evidence. Distillary makes that structure explicit, navigable, and verifiable.

## The pipeline (11 steps)

```
Source text (book, PDF, video transcript, article)
  ↓ split into ~20KB chunks
  ↓ save chunks permanently to brain/sources/{slug}/chunks/
  ↓ parallel haiku agents → atomic claims with backing + passages
  ↓ haiku agent → deduplicate (merge passages lists)
  ↓ haiku agent → extract entities (people, concepts, frameworks)
  ↓ haiku agent → add [[wikilinks]] to claim bodies (preserve passages in frontmatter)
  ↓ opus agents → group claims into argumentative clusters (layer 1)
  ↓ opus agent → build clusters into structure claims (layer 2) + root thesis (layer 3)
  ↓ haiku agents → find tensions, patterns, evidence between claims
  ↓ haiku agent → verify sample of claims against source chunks (optional)
  ↓ Python → assemble vault, fix links, build entity hubs, doctor
  ↓ opus agent → map concepts to other sources in the brain
  ↓ haiku agent → build bridge entities for same-concept pairs
Brain vault
```

Chunks are always saved locally — no question asked. They cost nothing and enable fact-checking every claim. Copyright only matters at publish time: sources marked `publishable: false` in `_source.md` have their chunks excluded from the public site.

## The pyramid

```
Layer 3: Root thesis (1 note)
  "The Lean Startup engineers sustainable businesses
   through validated learning"
    ↓
Layer 2: Structure (~2-3 notes)
  "Pivots and growth engines drive course correction"
  "Innovation accounting replaces vanity metrics"
    ↓
Layer 1: Clusters (~5-8 notes)
  "Small batches accelerate the feedback loop"
  "Customer validation precedes scaling"
    ↓
Layer 0: Atoms (~50-300 notes)
  "Zappos tested demand by posting shoe photos" [backed by experiential/case_study]
  "Cohort analysis reveals true retention" [backed by empirical/methodology, strength: strong]
```

Each layer summarizes the layer below. Drill down for detail + evidence. Drill up for context.

## The note format (v4.0)

```yaml
---
tags:
  - type/claim/atom
  - priority/core
  - certainty/argued
  - stance/endorsed
  - domain/methodology
  - role/argument
  - source/ries-lean-startup
  - backing/empirical
  - strength/strong
kind: claim
layer: 0
proposition: "validated learning → measures progress → better than vanity metrics"
source_ref: "Chapter 7: Measure"
published: 2011
extracted_by: claude-haiku-4.5
prompt_version: v4.0
backing:
  - category: empirical
    subtype: case_study
    ref: "IMVU pivot story"
    snippet: "We had been spending our time improving a product that nobody wanted"
    strength: strong
    warrant: "The IMVU case demonstrates that traditional metrics masked the fundamental product-market fit failure"
passages:
  - chunk: "chunk_04.txt"
    lines: [42, 48]
    snippet: "We had been spending our time improving a product that nobody wanted"
confidence: exact
---

Validated learning is empirically demonstrated progress through experiments
that test specific hypotheses about the business.

Parent: [[Innovation accounting replaces vanity metrics]]
```

### What each field does

| Field | Purpose |
|---|---|
| `proposition` | The claim in canonical form (subject → relationship → object) |
| `source_ref` | Where in the source (chapter, section, control ID) |
| `backing` | The evidence: what type, how strong, why it supports the claim |
| `passages` | Pointers to exact source text in chunk files (for fact-checking) |
| `confidence` | How directly the source text states the claim (exact / synthesized / inferred) |

### The 9 backing categories

Every piece of evidence fits one of 9 universal categories:

| Category | What it means | Examples |
|---|---|---|
| **textual** | Direct citation from authoritative text | Quranic verse, statute, primary source |
| **transmitted** | Report through chain of people | Hadith, witness testimony, reported data |
| **consensus** | Collective expert agreement | Scholarly ijma, scientific consensus, legal precedent |
| **analogical** | Extension from known to unknown | Qiyas, legal analogy, comparative study |
| **empirical** | Direct observation/measurement | Experiment, RCT, statistic |
| **rational** | Logical deduction/induction | Proof, syllogism, cost-benefit analysis |
| **experiential** | First-hand lived experience | Case study, anecdote |
| **authority** | Recognized expert statement | Scholar opinion, expert testimony |
| **silence** | Absence of evidence IS evidence | No text → ijtihad permitted |

These work across any domain — Islamic jurisprudence, cybersecurity, academic research, business, philosophy, law.

## Tag dimensions

| Tag | Question it answers |
|---|---|
| `priority/` | How central is this to the argument? |
| `certainty/` | How solid is the evidence? |
| `stance/` | Does the author endorse, criticize, or neutrally present this? |
| `domain/` | What field is this about? |
| `role/` | Is this a fact, argument, definition, requirement, rebuttal, or methodology? |
| `source/` | Which source does this come from? |
| `backing/` | What type of evidence backs this? (textual, transmitted, etc.) |
| `strength/` | How strong is the evidence? (definitive, strong, moderate, weak) |

## Cross-source bridges

When two sources discuss the same concept under different names, a bridge entity unifies them:

```
Lean Startup: "Vanity Metrics"  ←→  Mom Test: "Compliments"
                     ↓
          Bridge: "False Signals"
          (aliases both names, backlinks from both sources)
```

The bridge page shows both perspectives and every claim from both sources. One read = complete cross-source answer.

## Source verification

Claims can be traced back to exact source text:

```
Claim: "MFA for remote access"
  → passages: chunk_01.txt, lines 117-118
  → open chunk_01.txt → read line 117
  → "Multi-factor authentication for remote access.2-2-3-2"
  → VERIFIED — exact match
```

Chunks are always stored locally, so this always works on your machine. For published brains, verification depends on whether the publisher included chunks (copyrighted sources typically don't).

## Agent navigation

Entity pages are question-answering hubs. Their backlinks ARE the answer to "what does this brain know about X?"

```
Question: "How do I validate demand?"
  → find entity: "Customer Validation"
  → read its Referenced-by section
  → Lean Startup: test with MVP before building
  → Mom Test: look for commitment, not compliments
  → Zero to One: find a secret others have missed
  = 1 entity page, multi-source answer with citations
```

## Deep research

For complex questions, the research agent iterates through multiple passes:

1. Scope the question → break into sub-questions
2. Search claims → check backing quality
3. Follow backlinks → entity → claims → entity → claims (3+ hops)
4. Walk the pyramid → root to atom for context
5. Cross-reference sources → check bridges for agreement/conflict
6. Advanced methods → warrant mining, analogical transfer, rebuttal reconstruction
7. Source verification → read chunks to confirm claims (Method K)
8. Report with evidence, confidence rating, and gaps

See [Deep research agent](deep-research.md) for the full methodology.
