---
title: Architecture
---

# Architecture

## Three layers

```
.claude/          The brain — agents and skills that do the thinking
distillary/          The hands — Python utilities agents call
brain/            The output — Obsidian vault with all knowledge
```

### .claude/ (14 agents, 8 skills)

Agents are individual workers with specific models:
- **Haiku** (10 agents): extraction, deduplication, linking, entity work, doctor
- **Opus** (4 agents): grouping, pyramid building, concept mapping, comparison

Skills are orchestration workflows that chain agents:
- `distillary-add-source`: full pipeline from file to brain
- `distillary-retrieval`: self-contained skill for querying published brains
- `distillary-publish`: Quartz build + agent.json generation

### distillary/ (8 Python files)

```
extraction/loader.py  — extract_text(), split_text()
notes.py              — Note dataclass, parse/serialize, wikilink helpers
vault_ops.py          — fix_vault(), reinforce_links(), validate(),
                        build_entity_hubs(), fix_ghost_links()
doctor.py             — doctor() — fix + discover + _suggestions.md
cross_vault.py        — combine_vaults(), _build_bridges()
agent_index.py        — generate agent.json for publishing
sharing.py            — init_vault() — README + .gitignore
publish.py            — Quartz preview + deploy
```

### brain/ (the vault)

```
brain/
  sources/{slug}/         Per-source content
    _source.md            Metadata (title, author, type, year, URL)
    claims/atoms/         Layer 0: individual propositions
    claims/structure/     Layer 1: argument parents
    claims/clusters/      Layer 2: chapter groups
    claims/root           Layer 3: thesis
    entities/             People, concepts, companies
  shared/                 Cross-source
    concepts/             Bridge entities (source/cross-vault tag)
    analytics/            Comparison, mapping, graphs, stats
  personal/               Your voice
    annotations/          Reactions to claims
    notes/                Freeform thinking
    questions/            Things to explore
```

## Design decisions

- **Agents are the pipeline, Python is the plumbing.** Agents do extraction, grouping, comparison. Python does file I/O, link fixing, validation.
- **Haiku for bulk, opus for reasoning.** 16 parallel haiku agents = minutes not hours. Opus only where deep reasoning matters.
- **Post-processing catches agent mistakes.** `fix_ghost_links`, `_wire_parent_links`, `_split_frontmatter` handle format inconsistencies mechanically.
- **One vault, not many.** Everything in `brain/`. Sources accumulate. Bridges grow. Your annotations are part of the graph.
- **Static publishing.** Quartz generates a website. `agent.json` makes it agent-queryable. No server needed.
- **Backlinks are the search engine.** Entity pages + backlinks = "what does this brain know about X?" No keyword search needed.
