---
title: How It Works
---

# How Distillary works

## The insight

Every source (book, video, article) has an argument structure: a central thesis supported by a hierarchy of claims. Distillary makes that structure explicit and navigable.

## The pipeline

```
Source text
  ↓ split into ~20KB chunks
  ↓ 16 parallel haiku agents → atomic claims (one assertion each)
  ↓ haiku agents → deduplicate
  ↓ haiku agent → extract entities (people, concepts, companies)
  ↓ opus agents → group claims into argumentative clusters (layer 1)
  ↓ opus agent → build clusters into chapter groups (layer 2)
  ↓ opus agent → build single root thesis (layer 3)
  ↓ haiku agents → find tensions, patterns, evidence between claims
  ↓ haiku agent → add [[wikilinks]] to entity references
  ↓ Python → assemble vault, fix links, build entity hubs
  ↓ Python → doctor (fix orphans, discover ghosts, write suggestions)
  ↓ opus agent → map concepts to other sources in the brain
  ↓ haiku agent → build bridge entities for same-concept pairs
Brain vault
```

## The pyramid

```
Layer 3: Root thesis (1 note)
  "The Lean Startup engineers sustainable businesses through validated learning"
    ↓
Layer 2: Clusters (~8 notes)
  "Pivots and growth engines drive course correction"
  "Small batches accelerate the feedback loop"
  "Innovation accounting replaces vanity metrics"
    ↓
Layer 1: Structure (~50 notes)
  "A pivot is a structured strategic hypothesis"
  "Customer segment pivots redefine the audience"
    ↓
Layer 0: Atoms (~300 notes)
  "Zappos tested demand by posting shoe photos before buying inventory"
  "IMVU's IM interop assumption was wrong — users wanted to meet strangers"
```

Each layer is a summary of the layer below. Drill down for detail. Drill up for context.

## The note format

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
kind: claim
layer: 0
proposition: "validated learning → measures progress → better than vanity metrics"
source_ref: "Chapter 7: Measure"
---

Validated learning is empirically demonstrated progress through experiments
that test specific hypotheses about the business. Unlike traditional metrics
that measure output, validated learning measures whether customers actually
want what you're building.

## Related

Parent: [[Innovation accounting replaces vanity metrics]]
- 📊 Supported by: [[Cohort analysis reveals true effectiveness]]
- ⚡ Tension with: [[Speed of shipping matters more than what you learn]]
```

## Tag dimensions

| Tag | Question it answers |
|---|---|
| `priority/` | How central is this to the argument? |
| `certainty/` | How solid is the evidence? |
| `stance/` | Does the author endorse, criticize, or neutrally present this? |
| `domain/` | What field is this about? |
| `role/` | Is this a fact, argument, prediction, definition, example, or methodology? |
| `source/` | Which source does this come from? |

## Cross-source bridges

When two sources discuss the same concept under different names, a bridge entity unifies them:

```
Lean Startup: "Vanity Metrics"  ←→  Mom Test: "Compliments"
                     ↓
           Bridge: "False Signals"
           (aliases both names, backlinks from both sources)
```

The bridge page shows both perspectives and every claim from both sources that discusses the concept. One fetch = complete cross-source answer.

## Agent navigation

Entity pages are question-answering hubs. Their backlinks are the answer to "what does this brain know about X?"

```
Question: "How do I validate demand?"
  → agent.json (see bridges)
  → "Real Signals" bridge page
  → Lean Startup: actionable metrics with causation
  → Mom Test: commitment that costs time/money/reputation
  → 36 + 26 backlinks for specific evidence
  = 2 fetches, multi-source answer
```
