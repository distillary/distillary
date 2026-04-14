# Distillary — Knowledge Distillation with Claude Agents

Turn any knowledge source into a navigable brain vault using parallel Claude agents. Books, YouTube videos, podcasts, articles, lectures — anything with ideas gets distilled into the same format. Shared concepts bridge sources. Your annotations are first-class.

## Engineering principle

**Always fix root causes, not byproducts.** When something breaks, trace the issue to its origin — the agent prompt, the parser, or the post-processing code — and fix it there. Never patch outputs manually. If an agent produces malformed YAML, fix the agent prompt AND add normalization to `_normalize_note_meta()`. If a parser misreads content, fix the parser regex. Every fix must be in code so the next run produces correct output automatically.

## How agents navigate the brain

Entity pages are question-answering hubs. Their backlinks are the answer.

**"What does the brain know about X?"** → find the entity for X → its backlinks ARE claims about X from every source. Follow backlinks to read evidence. Follow wikilinks in claims to discover related concepts. Understanding builds through connections, not data dumps.

`agent.json` → entity page → backlinks → specific claims. ~2,500 tokens for a complete multi-source answer with citations.

## The Brain

`brain/` is the single Obsidian vault. Everything lives inside it.

```
brain/
  _index.md                    — start here
  _suggestions.md              — doctor findings
  *.base                       — analytical Bases
  sources/                     — processed sources (agent-generated)
    {source-slug}/
      chunks/                  — source text chunks for fact-checking (OPTIONAL — omit for copyrighted material)
      claims/{atoms,structure,clusters}
      entities/{concepts,people,companies,works}
      _source.md               — metadata: type, author, url, date
  personal/                    — your own notes (human-written)
    annotations/               — reactions to claims
    notes/                     — freeform thinking
    questions/                 — things to explore
  shared/                      — cross-source connections
    concepts/                  — bridge entities spanning sources
    analytics/                 — comparisons, mappings, stats
  .obsidian/snippets/
```

## Source types

Any source that contains ideas can be ingested:

| Type | Input | How it's extracted |
|---|---|---|
| Book | EPUB, PDF, TXT | `extract_text()` from file |
| YouTube video | URL | Transcript via `yt-dlp` or YouTube API |
| Podcast | URL or audio file | Transcript via Whisper or API |
| Article | URL | Web fetch → clean text |
| Lecture notes | PDF, markdown | `extract_text()` from file |
| Research paper | PDF | `extract_text()` from file |
| Personal notes | markdown | Already in the brain — just link |

The extraction step produces text. Everything after that is the same pipeline: extract claims → dedupe → entities → group → pyramid → link → assemble.

## Source metadata

Every source folder has a `_source.md` with metadata:

```yaml
---
title: "The Lean Startup"
author: "Eric Ries"
type: book
published: 2011
url: ""
source_slug: ries-lean-startup
ingested: 2026-04-07
extracted_by: claude-haiku-4.5
chunks_available: true       # false for copyrighted sources
chunks_reason: "public_domain"  # or "copyrighted", "proprietary", "excluded_for_publishing"
---
```

This enables filtering by source type, author, date, and medium. The `chunks_available` field tells agents whether fact-checking against source text is possible for this source.

## Agents

### Source processing (single-source pipeline)

| Agent | Model | Job |
|---|---|---|
| `extract` | haiku | Text chunk → atomic claims with `source_ref`, `backing`, and `passages` |
| `dedupe` | haiku | Merge duplicate claims (combine `passages` lists, preserve `backing`) |
| `entities` | haiku | Identify people, concepts, companies |
| `entity-link` | haiku | Add `[[wikilinks]]` to claim bodies (preserve `passages` + `backing` in frontmatter) |
| `link` | haiku | Find tensions, patterns, evidence |
| `group` | opus | Cluster claims into parents (L0→L1) — preserve `backing` + `passages` on atoms |
| `pyramid` | opus | Build hierarchy to root (L1→L2→L3) |
| `verify` | haiku | Fact-check claims against source chunks via `passages` field |
| `source-index` | haiku | Write compelling source index page with narrative, not mechanical tables |

### Brain-level operations

| Agent | Model | Job |
|---|---|---|
| `doctor` | haiku | Fix orphans, ghost links, suggest explorations, flag claims missing `passages` |
| `combine` | haiku | Merge sources into brain structure |
| `concept-mapper` | opus | Find same-concept-different-name pairs across sources |
| `compare` | opus | Write synthesis essay comparing sources |
| `bridge-builder` | haiku | Create unified entity notes from mapping |
| `analytics` | haiku | Generate cross-source reports: statistical profiles, entity overlap, set operations, graph analytics |
| `annotate` | haiku | Help user write annotations in proper format |
| `research` | opus | Deep research agent — iteratively searches brain to answer questions, checks evidence quality, cross-references sources |
| `explore` | opus | Suggest what to investigate based on gaps + interests |

### Rules (enforced in all agents)

- **DO NOT number notes**
- **DO NOT use `# H1` section dividers**
- **Parent format**: `Parent: [[Title]]` (no quotes)
- **Keep titles under 150 characters**
- **Preserve full body text** when editing
- **Preserve `backing` and `passages` fields** — any agent that writes or modifies atom claims must keep these fields intact. Dedupe merges them; all others copy them unchanged.
- **Chunks are optional but recommended** — saved to `brain/sources/{slug}/chunks/` for fact-checking. For copyrighted or proprietary sources, chunks can be omitted (claims still work without them — `passages` field becomes unverifiable but the claim itself is still valid). When publishing a brain, exclude `chunks/` directories to avoid sharing copyrighted source text. The `passages` field on claims remains useful as a reading reference even without the chunk files.

## Skills

| Skill | Triggers | What it does |
|---|---|---|
| `distillary-add-source` | "add book", "add video", "new source" | Full pipeline: ingest + decompose + auto-bridge |
| `distillary-decompose` | "decompose", "extract claims" | Core extraction pipeline (used by add-source) |
| `distillary-combine` | "combine", "merge vaults" | Cross-vault concept mapping + bridges |
| `distillary-doctor` | "fix", "check", "issues" | Fix + discover + suggestions |
| `distillary-publish` | "publish", "share" | Git + Quartz deploy + agent.json generation |
| `distillary-retrieval` | "query brain", "look up" | **Shareable** — give to any agent to query a published brain via URL |
| `distillary-use-brain` | "explore brain", "learn about" | Full navigation guide — 6 strategies by question type |
| `distillary-research` | "research", "investigate", "ابحث", "ما رأي" | Deep research — iterative search with evidence evaluation |
| `obsidian-bases` | "create base" | Analytical .base files |
| `quartz-rendering` | "add diagram", "add callout" | What Quartz can render: callouts, Mermaid, wikilinks, code, LaTeX, embeds |
| `docs-writing` | "write docs", "improve docs" | How to write good docs: text first, diagrams support, callouts highlight |

## Python utilities

```
distillary/
  extraction/loader.py     — extract_text(), split_text()
  notes.py                 — Note dataclass, parse_notes(), serialize()
  vault_ops.py             — fix_vault(), reinforce_links(), validate(),
                             build_entity_hubs(), fix_ghost_links()
  doctor.py                — doctor()
  cross_vault.py           — combine_vaults(), _build_bridges()
  sharing.py               — init_vault()
  publish.py               — publish(), preview()
```

Old API pipeline (Gemini/Anthropic/OpenAI) is in `deprecated/`.

## Workflows

### Add a source to the brain

```
1. Extract + split text (python) → save chunks to brain/sources/{slug}/chunks/
2. Extract claims with backing + passages — parallel extract agents (haiku)
3. Dedupe (merge passages lists) + entities — parallel haiku agents
4. Entity-link — haiku agent (add [[wikilinks]] to bodies, preserve passages/backing in frontmatter → linked_claims.md)
5. Group + pyramid — opus agents (**input: linked_claims.md**, preserve passages/backing on atoms)
6. Link — parallel haiku agents (cross-claim tensions, patterns)
7. Verify (optional) — haiku agent fact-checks sample of claims against chunks
8. Assemble into brain/sources/{slug}/ (python: fix_vault)
9. Post-process entire brain (python: reinforce + hubs + doctor flags missing passages)
10. Auto-bridge — concept-mapper (opus) + bridge-builder (haiku)
11. Update brain/_index.md
```

**CRITICAL: Always use agent definition files.** When launching any agent, point it to its `.claude/agents/{name}.md` file:

```
prompt="Read the agent instructions from .claude/agents/group.md FIRST, then follow them precisely.
[specific task details]"
```

DO NOT rewrite agent instructions inline. The agent files contain tested rules (wikilinks in body text, Parent format, title length, etc.) that get lost when instructions are rewritten from memory. Agent files are the source of truth.

### Add your own notes

Write to `brain/personal/annotations/` or `brain/personal/notes/`. Use `[[wikilinks]]` to link to claims and entities. The `annotate` agent helps with formatting.

### Explore what to read next

The `explore` agent reads your annotations, ghost links, and bridge gaps. It suggests specific concepts to promote, contradictions to investigate, and patterns in your thinking.

### Publish

Say "publish my brain" → Quartz static site on GitHub Pages with the full brain graph + agent.json API.

## Note format

```yaml
tags: [type/claim/atom, priority/core, certainty/argued,
       stance/endorsed, domain/X, role/argument, source/slug,
       backing/textual, strength/strong]
kind: claim
layer: 0
proposition: "subject → relationship → object"
source_ref: "Chapter 3: Steer"
published: 2011
extracted_by: claude-haiku-4.5
backing:
  - category: textual|transmitted|consensus|analogical|empirical|rational|experiential|authority|silence
    subtype: "domain-specific label"
    ref: "citation"
    snippet: "first ~15 words"
    strength: definitive|strong|moderate|weak|contested
    warrant: "why this evidence supports this claim"
passages:
  - chunk: "chunk_01.txt"
    lines: [10, 15]
    snippet: "first ~15 words of the source passage"
  - chunk: "chunk_03.txt"
    lines: [42, 48]
    snippet: "first ~15 words of another passage"
confidence: exact|synthesized|inferred
```

## Key design decisions

- **One vault (brain), not many** — everything connected, bridges grow incrementally
- **Any source type** — books, videos, podcasts, articles, papers all become the same note format
- **Haiku for bulk, opus for reasoning** — cost/speed tradeoff
- **Your voice is data** — annotations are queryable, bridge to claims
- **Post-processing catches agent mistakes** — `fix_ghost_links`, `_wire_parent_links`, `_split_frontmatter` handle format inconsistencies mechanically
- **`source/` tag on everything** — distinguishes sources, enables filtering
- **`source/cross-vault` tag** — marks bridge concepts that span sources
- **`_source.md` per source** — metadata: type, author, url, date for filtering and attribution
- **Chunks enable fact-checking (optional)** — `passages` field on claims references chunk files + line ranges + snippets. Full text stays in chunks, claims stay clean. For copyrighted sources, chunks can be excluded from publishing — the `passages` field still serves as a reading reference (chapter, page, section). For open/public domain sources, chunks provide full verifiability.
- **`backing` captures argumentation** — 9 universal categories (textual, transmitted, consensus, analogical, empirical, rational, experiential, authority, silence) with warrant explaining WHY evidence supports the claim
