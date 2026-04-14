---
title: Architecture
---

# Architecture

## Three layers

```
.claude/             The brain — agents and skills that do the thinking
distillary/          The hands — Python utilities agents call
brain/               The output — Obsidian vault with all knowledge
```

### .claude/ (16 agents, 9 skills)

Agents are individual workers with specific models:
- **Haiku** (11 agents): extraction, deduplication, entity linking, linking, entities, doctor, annotate, source-index, brain-index, bridge-builder, verify
- **Opus** (5 agents): grouping, pyramid building, concept mapping, comparison, research, explore

Skills are orchestration workflows that chain agents:
- `distillary-add-source`: full pipeline from file to brain (asks user about chunk storage)
- `distillary-research`: deep iterative question-answering with 6 strategies + 10 advanced methods
- `distillary-retrieval`: self-contained skill for querying published brains
- `distillary-publish`: Quartz build + agent.json generation

### distillary/ (8 Python files)

```
extraction/loader.py  — extract_text(), split_text() — supports EPUB, PDF, TXT, HTML, MD
notes.py              — Note dataclass, parse/serialize, wikilink helpers, backing_of()
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
  _index.md                        Start here
  _suggestions.md                  Doctor findings
  *.base                           Analytical Bases
  sources/                         Processed sources (agent-generated)
    {source-slug}/
      _source.md                   Metadata (title, author, type, year, publishable)
      _index.md                    Narrative overview of this source
      chunks/                      Source text chunks (OPTIONAL — user chooses)
        chunk_00.txt
        chunk_01.txt
      claims/
        {root-thesis}.md           Layer 3: single thesis
        structure/                 Layer 2: major arguments
        clusters/                  Layer 1: thematic groups
        atoms/                     Layer 0: individual claims with backing + passages
      entities/
        concepts/                  Abstract ideas, principles
        people/                    Scholars, historical figures
  shared/                          Cross-source connections
    concepts/                      Bridge entities (source/cross-vault tag)
    evidence/                      Shared evidence hubs (same citation across sources)
    analytics/                     Comparison, mapping, graphs, stats
  personal/                        Your voice
    annotations/                   Reactions to claims
    notes/                         Freeform thinking
    questions/                     Things to explore
    research/                      Deep research outputs
```

## The claim format (v4.0)

Every atom claim can have up to 4 layers of information:

```
What is claimed     → proposition, body text
How it's argued     → backing (category, subtype, strength, warrant)
Where it's from     → passages (chunk file, lines, snippet)
How certain         → confidence (exact / synthesized / inferred)
```

This makes claims not just assertions but **auditable, evidence-graded, source-traceable arguments**.

## Agent pipeline (11 steps)

```
 1. Extract + split text → save chunks (if user chose "yes")
 2. Extract claims with backing + passages
 3. Dedupe (merge passages) + entities
 4. Entity-link (add wikilinks, preserve passages/backing)
 5. Group + pyramid (from linked claims, preserve passages/backing)
 6. Link (tensions, patterns)
 7. Verify (optional — spot-check claims against chunks)
 8. Assemble into brain
 9. Post-process (reinforce links, entity hubs, doctor flags missing passages)
10. Auto-bridge (concept-mapper + bridge-builder)
11. Update brain index
```

**Critical rule:** Always use agent definition files (`.claude/agents/{name}.md`). Never rewrite agent instructions from memory. The definition files contain tested rules that prevent data loss.

## Design decisions

- **Agents are the pipeline, Python is the plumbing.** Agents do extraction, grouping, comparison. Python does file I/O, link fixing, validation.
- **Haiku for bulk, opus for reasoning.** Parallel haiku agents = minutes not hours. Opus only where deep reasoning matters.
- **Post-processing catches agent mistakes.** `fix_ghost_links`, `_wire_parent_links`, `_split_frontmatter` handle format inconsistencies mechanically.
- **One vault, not many.** Everything in `brain/`. Sources accumulate. Bridges grow. Your annotations are part of the graph.
- **Static publishing.** Quartz generates a website. `agent.json` makes it agent-queryable. No server needed.
- **Backlinks are the search engine.** Entity pages + backlinks = "what does this brain know about X?" No keyword search needed.
- **Entity-link before group.** Wikilinks are added to claims BEFORE grouping, so atom files written to the vault already contain entity links. No manual patching needed.
- **Backing captures argumentation.** 9 universal categories work across any domain. The same framework handles Islamic jurisprudence, cybersecurity regulation, academic research, and business books.
- **Chunks always stored, publish-gated.** Chunks are always saved locally during ingestion (they cost nothing, enable full fact-checking). The `publishable` field in `_source.md` controls whether chunks are included when publishing to the web. Copyrighted source chunks stay local; public domain chunks get published.
- **Passages are lightweight.** Claims store only pointers (chunk + lines + ~15-word snippet), not full text. The full context stays in chunk files. This keeps claims clean while enabling full traceability.
