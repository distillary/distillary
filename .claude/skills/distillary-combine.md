---
name: distillary-combine
description: Combine multiple book vaults into one with cross-references and concept bridges. Triggers on "combine vaults", "compare books", "cross-vault", "merge vaults", "field-level".
---

# Distillary Combine — Multi-vault synthesis

Combine two or more book vaults into a unified knowledge base with concept bridges, comparison analytics, and cross-book navigation.

## Full workflow

### Step 1: Combine vaults

```python
from distillary.cross_vault import combine_vaults
combine_vaults(["vault-book-a/", "vault-book-b/"], "vault-combined/")
```

Or launch a `combine` agent to handle it.

### Step 2: Generate concept mapping (opus agent)

Launch a `concept-mapper` agent:

```
Agent(subagent_type="concept-mapper", model="opus",
  prompt="Read entities in vault-combined/entities/. Find same-concept pairs across books.
  Write mapping to vault-combined/analytics/entity-mapping.md")
```

This produces a table of same-concept-different-name pairs and complementary concepts.

### Step 3: Build bridge entities

Launch a `bridge-builder` agent with the mapping results:

```
Agent(subagent_type="bridge-builder", model="haiku",
  prompt="Read vault-combined/analytics/entity-mapping.md.
  Create bridge entity notes in vault-combined/ using the concept pairs.")
```

Or run directly:

```python
from distillary.cross_vault import _build_bridges
from pathlib import Path

pairs = [
    {"ls": "Validated Learning", "mt": "Conversation quality",
     "merged": "Validated Learning",
     "description": "Whether customer interaction produced genuine knowledge."},
    # ... more pairs from the mapping
]
_build_bridges(Path("vault-combined/"), pairs)
```

### Step 4: Generate comparison essay (opus agent)

```
Agent(subagent_type="compare", model="opus",
  prompt="Read root notes from both books in vault-combined/.
  Write comparison to vault-combined/analytics/comparison.md")
```

### Step 5: Post-process

```python
from distillary.vault_ops import reinforce_links, build_entity_hubs, validate
from distillary.doctor import doctor

reinforce_links("vault-combined/")
build_entity_hubs("vault-combined/")
doctor("vault-combined/")
validate("vault-combined/")
```

### Step 6: Generate analytics

Launch an `analytics` agent to generate all cross-source reports:

```
Agent(subagent_type="analytics", model="haiku",
  prompt="Read all claims and entities in brain/sources/.
  Generate statistical-profiles.md, entity-overlap.md, set-operations.md,
  and graph-analytics.md in brain/shared/analytics/.")
```

This produces 4 reports: statistical profiles comparing authorial style, entity overlap and hub identification, claim-level set operations, and graph centrality analysis.

## What the combined vault contains

```
vault-combined/
  _index.md                  — links to both roots + analytics
  analytics/
    comparison.md            — opus synthesis essay
    entity-mapping.md        — concept mapping table
    graph-analytics.md       — hub ideas + bridge nodes
    statistical-profiles.md  — tag distributions compared
  claims/                    — all claims from both books
  entities/
    concepts/                — includes bridge notes (source/cross-vault)
    people/, companies/      — merged from both books
  *.base                     — cross-book Bases
```

## Key concepts

- **Bridge notes** have `source/cross-vault` tag, aliases from both books, Referenced-by from both
- **Original entities** get a "Cross-book concept: See [[Bridge]]" link
- **The `source/` tag** on every claim identifies which book it came from
- **Graph view** colored by `source/` shows which book each node belongs to
