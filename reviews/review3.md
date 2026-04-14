# Review 3 — Cross-vault operations: what works, what doesn't, what to change

## What we tested

Five families of cross-vault operations between The Lean Startup and The Mom Test:

1. **Statistical profiles** — tag distribution comparison
2. **Graph analytics** — centrality, bridge nodes, shortest paths
3. **Set operations** — shared vs unique claims by proposition matching
4. **Entity overlap** — which concepts appear in both books
5. **Synthesis** — opus agent reading both roots and producing a comparison essay

## What actually works

### The synthesis essay is genuinely useful

The opus comparison (`vault-comparison.md`) produces real insight: Lean Startup
designs the learning system but leaves "how to talk to customers" as a black box.
Mom Test fills that exact gap. The tension analysis (speed vs patience, MVP vs
pre-product validation) is non-obvious. The reading order recommendation (Mom Test
first) is actionable.

This is the kind of output you can't get from reading either book alone.

### Graph analytics reveal real structure

"Pivot" is the most central concept in Lean Startup (0.49 degree centrality).
"Customer conversation" is the most central in Mom Test (0.70). These aren't
surprising, but the bridge nodes are — "Innovation teams need structural
autonomy" is the #2 bridge in LS, connecting the organizational layer to
the methodology layer. That's a structural insight about how the book's
argument is wired.

### Statistical profiles show how authors think

LS is 50% established / 40% argued certainty — Ries is defending positions.
MT is 51% argued / 47% established — Fitzpatrick presents more settled wisdom.
This isn't visible from reading the books. It's a fingerprint of authorial
style that only emerges from structured comparison.

## What doesn't work

### The files live outside both vaults

This is the fundamental problem. `vault-comparison.md` and `analytics/*.md`
sit in the project root, not inside any Obsidian vault. The `[[wikilinks]]`
in them reference notes from both vaults, but Obsidian can only resolve links
within a single vault. The analytics files are just markdown — you can read
them, but you can't click through to the actual claims.

**Fix**: Create a `vault-combined/` that contains notes from both books
plus the analytics. Wikilinks then resolve. The `source/` tag distinguishes
which book each claim comes from.

### Entity overlap is almost zero

Only 1 shared entity ("Pivot") across 72 + 81 entities. The books use
completely different vocabulary for similar concepts. Lean Startup has
"Validated Learning", Mom Test has "Customer conversation". Same idea,
different names. The entity overlap test is useless without semantic
matching — it only catches identical strings.

**Fix**: An opus agent should compare entity lists semantically, not by
exact name match. "Validated Learning" and "Customer learning" are the
same concept at different abstraction levels. The agent should produce a
concept-mapping table.

### Set operations are noisy

Keyword-overlap matching between propositions produces 41 "shared" pairs,
but most are false positives — claims that share common words ("customer",
"learning", "startup") without actually making the same point. The matching
needs semantic comparison, not bag-of-words.

**Fix**: Either use an LLM for pairwise equivalence checking (expensive
but accurate), or filter to propositions with 5+ keyword overlap (misses
subtle matches). The `proposition:` field was designed for this, but
it needs to be more strictly normalized across books.

### Analytics are static snapshots

The analytics files are generated once and go stale. If you edit the vault
(add annotations, promote ghosts, fix orphans), the analytics don't update.
They should be Obsidian Bases or Dataview queries that compute live.

**Fix**: Graph analytics can't be live (NetworkX isn't in Obsidian). But
statistical profiles and entity overlap CAN be Bases with formulas that
query both vaults. The comparison essay should be a note inside the vault,
not a standalone file.

## What to change

### 1. Combined vault for cross-book work

```
vault-combined/
  _index.md                  — links to both books' roots + analytics
  lean-startup/              — symlink or copy of LS vault
  mom-test/                  — symlink or copy of MT vault
  analytics/
    comparison.md            — the opus synthesis (lives here now)
    statistical-profiles.md
    graph-analytics.md
    entity-mapping.md        — semantic entity comparison (new)
  shared-entities/           — merged entities that appear in both books
```

Obsidian treats the combined vault as one graph. Notes from both books
appear together. Entity nodes that represent the same concept get merged.
The comparison essay is clickable.

### 2. Semantic entity mapping (opus agent)

Instead of exact string matching, an opus agent reads both entity lists
and produces a mapping:

```markdown
## Entity Mapping

| Concept | Lean Startup | Mom Test | Relationship |
|---|---|---|---|
| Customer learning | [[Validated Learning]] | [[Customer conversation]] | Same concept, different scope |
| False signals | [[Vanity Metrics]] | [[False positive]] | Same pattern, different domain |
| Strategic change | [[Pivot]] | [[Pivot]] | Shared term |
| Incremental test | [[Minimum Viable Product]] | [[Commitment]] | Complementary — MVP tests product, commitment tests demand |
```

This is the most valuable cross-vault operation. It makes the conceptual
bridge between books visible.

### 3. Live Bases for cross-vault stats

In the combined vault, Bases can query both books:

```yaml
# Tag comparison Base
filters:
  and:
    - kind == "claim"
formulas:
  book: if(file.hasTag("source/ries-lean-startup"), "Lean Startup", "Mom Test")
views:
  - type: table
    groupBy:
      property: formula.book
    summaries:
      file.name: Filled
```

This replaces the static `statistical-profiles.md` with a live,
interactive view.

### 4. Don't generate what Obsidian can compute

The graph analytics (centrality, bridges) require NetworkX and can't run
in Obsidian. Those stay as static files — generated once, read-only.

But statistical profiles, entity lists, and claim counts ARE computable
by Bases. Don't generate markdown files for things Bases can do live.

**Rule**: If Obsidian can compute it → use a Base.
If it needs NetworkX/LLM → generate a static file.

## What's actually valuable

After testing all 5 operation families, the priority ranking for usefulness:

1. **Synthesis essay** (opus) — produces genuine insight you can't get otherwise
2. **Entity mapping** (opus) — makes the conceptual bridge visible
3. **Graph analytics** (NetworkX) — reveals structural patterns
4. **Statistical profiles** (tags) — author fingerprinting
5. **Set operations** (propositions) — needs semantic matching to be useful

The first two need an LLM. The last three are pure computation. The most
valuable operations are the ones where AI reasoning adds something that
mechanical comparison can't.

## Update: combined vault built

All analytics now live inside `vault-combined/` — 580 files, 6,348 links,
100% resolved. Every `[[wikilink]]` in the comparison essay and analytics
files is clickable. The entity mapping (10 same-concept pairs, 13
complementary pairs) is the most useful cross-vault artifact — it shows
that "Validated Learning" = "Conversation quality" at different abstraction
levels, and that "Vanity Metrics" = "Compliments" (quantitative vs
qualitative false signals).

### What's genuinely useful

- **The comparison essay** — reading it gives you understanding of the
  field that neither book alone provides. The meta-thesis ("two-layer
  discipline") is actionable: it tells you WHAT to read and in WHAT ORDER.
- **The entity mapping table** — scanning 10 rows of "same concept,
  different name" gives you the Rosetta Stone between two authors'
  vocabularies. This saves hours of confused re-reading.
- **The entity hubs** — in the combined vault, [[Pivot]] has 119
  backlinks from LS claims. [[Customer conversation]] has dozens from MT.
  These are genuine navigation hubs you can explore for hours.
- **The Bases** — Book Comparison base lets you toggle between "by book /
  by certainty / by role" views of all 420 claims. This is interactive
  exploration, not static analysis.

### What's not useful (honest)

- **Set operations by keyword matching** — 24 "shared" pairs but most are
  false positives. "Past behavior reveals priorities" matches "Customer
  Pivots Redefine Who Is Served" because they share the words "customer"
  and "more." That's noise, not signal. This needs semantic (LLM) matching.
- **Statistical profiles** — interesting to read once but not something
  you revisit. "LS is 50% established, MT is 51% argued" — ok, noted.
  Now what? There's no action to take from this.
- **Entity overlap by exact name** — only 1 shared entity (Pivot). This
  is why the semantic entity mapping exists. The exact-match version is
  misleading — it implies the books share nothing when they actually share
  most of their core concepts under different names.
