# Review 4 — The Brain as the Standard

## The shift

The unit of work is no longer "process a book into a vault." It's "grow a brain."

The brain is one Obsidian vault. Everything lives inside it — books you've read, your own notes, concepts that bridge sources, analytics that reveal patterns. When you process a new book, it goes into `brain/books/{slug}/`. When you write your own thoughts, they go into `brain/personal/`. When agents find connections between sources, bridges go into `brain/shared/`.

This changes the architecture. The brain isn't a output — it's the workspace.

## New structure

```
brain/
  _index.md                    — entry point, links to everything
  _suggestions.md              — doctor findings across all sources
  *.base                       — analytical Bases
  
  books/                       — processed books (agent-generated)
    lean-startup/
      claims/{atoms,structure,clusters}
      entities/{concepts,people,companies}
    mom-test/
      claims/...
      entities/...
    [next-book]/               — add more books incrementally
      ...
  
  personal/                    — your own notes (human-written)
    annotations/               — reactions to specific claims
    notes/                     — freeform thinking
    questions/                 — things you want to explore
  
  shared/                      — cross-source connections (agent-discovered)
    concepts/                  — bridge entities spanning sources
    analytics/                 — comparison essays, mappings, graphs
    tensions/                  — unresolved contradictions worth thinking about
  
  .obsidian/snippets/          — CSS
```

## What changes in .claude/

### The brain agent

A new top-level agent that manages the brain vault. It knows:
- Where the brain lives
- What books are in it
- What bridges exist
- What's been annotated

When you say "process this book," it runs `distillary-decompose` and puts the result in `brain/books/{slug}/`. When you say "what connects these two books," it runs `concept-mapper` + `bridge-builder` scoped to those books. When you say "what should I explore next," it reads `_suggestions.md` and your annotations.

### Personal vault integration

The brain isn't read-only. You add notes to `brain/personal/`:

```markdown
## My reaction to validated learning
---
tags:
  - kind/annotation
  - annotates/lean-startup
  - status/disagree
---

I think Ries overstates the case for metrics. In my experience,
the best startups I've seen operated on [[Gut reactions]] more
than [[Innovation Accounting]]. The Mom Test's approach of
[[Commitment]] as validation feels more honest than dashboards.

Parent: [[Validated Learning]]
```

This note appears in the graph connected to `[[Validated Learning]]` and `[[Commitment]]`. Your voice becomes part of the knowledge structure. Agents can read your annotations and surface patterns: "You disagree with 80% of measurement claims but endorse all conversation methodology claims — you trust qualitative over quantitative."

### Skills update

| Skill | What changes |
|---|---|
| `distillary-decompose` | Output goes to `brain/books/{slug}/` not a standalone vault |
| `distillary-combine` | Replaced by `fractal-bridge` — runs on books already in brain |
| `distillary-doctor` | Scopes to entire brain, not one vault |
| `distillary-publish` | Publishes the whole brain, not individual vaults |
| NEW: `fractal-add-book` | Extract + decompose + auto-bridge to existing books |
| NEW: `fractal-annotate` | Help user write annotations with proper format + tags |
| NEW: `fractal-explore` | Suggest what to read/explore based on gaps and interests |

### Agent updates

| Agent | What changes |
|---|---|
| `concept-mapper` | Runs across ALL books in brain, not just two |
| `bridge-builder` | Incrementally adds bridges when a new book arrives |
| `compare` | Can compare any N books, not just two |
| NEW: `annotate` | Helps write annotations in proper format |
| NEW: `explore` | Reads annotations + suggestions, recommends next steps |

## Why this is better

### 1. Incremental growth

Current: process book → get vault → done. Each book is isolated.
Brain: process book → it joins the brain → agents find connections to everything already there.

Book #3 arrives. The concept-mapper runs against books #1 and #2 automatically. Bridge entities get created. The graph grows. Your annotations on book #1 now connect to claims in book #3 that you haven't read yet.

### 2. Your voice is first-class

Current: the vault is LLM-generated. You're a consumer.
Brain: `personal/` is yours. Annotations link to claims. Questions link to gaps. Your reactions are queryable data.

A Base that shows "all claims I disagree with, grouped by book" is a mirror of your intellectual biases. That's useful.

### 3. The frontier is visible

Ghost links from ALL books accumulate. A concept that book #1 mentions as a ghost and book #3 mentions as a ghost is probably important — it's on the frontier of the entire field, not just one author's blind spot.

The `explore` agent reads the brain-wide ghost list, cross-references with your annotations, and says: "You've marked 3 claims about [[customer development]] as 'interesting' but this concept has no entity note. Here's what 4 books say about it. Want me to promote it?"

### 4. Publishing is sharing your perspective

When you publish the brain, it includes your annotations. That's not just a processed book — it's your interpretation. Someone else's brain on the same books would have different annotations, different promoted ghosts, different bridges they chose to explore.

The community isn't sharing raw vaults. It's sharing perspectives on the same material.

## What NOT to change

- The note format stays the same (YAML frontmatter + wikilinks)
- The agent architecture stays the same (haiku bulk, opus reasoning)
- The post-processing stays the same (fix_vault, reinforce, doctor)
- The tag taxonomy stays the same (priority, certainty, stance, domain, role, source)

The brain is an organizational pattern, not a new system. Everything we built still works. It just lives in one place instead of scattered across vault-v1, vault-v2, vault-v3, vault-combined.

## Implementation priority

1. **Update CLAUDE.md** — make brain the standard, document the structure
2. **Update `distillary-decompose` skill** — output to `brain/books/{slug}/`
3. **Add `fractal-add-book` skill** — decompose + auto-bridge
4. **Add `annotate` agent** — help write personal notes
5. **Add `explore` agent** — suggest what to investigate
6. **Update `distillary-publish`** — publish entire brain
7. **Clean up old vaults** — move vault-* to deprecated or delete
