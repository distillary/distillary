# Distillary Pipeline Review 2 — v2 Vault Self-Reflection

## Progress since Review 1

The v2 vaults fixed the critical assembly bug. The numbers improved dramatically:

| Metric | v1 LS | v2 LS | v1 MT | v2 MT |
|---|---|---|---|---|
| Files | 172 | 771 | 78 | 282 |
| Link resolution | ~20% | 99.9% | ~22% | 99.7% |
| Layer-0 atoms | 0 | 630 | 0 | 238 |
| Lateral links | 0 | merged | 0 | merged |
| Entity wikilinks | 0 | 416 added | 0 | 212 added |
| Validation issues | unknown | 0 | unknown | 0 |

The `fix_vault`, `reinforce_links`, and `validate` commands work correctly.
Link resolution went from ~20% to 99.9%. That's the difference between a
broken vault and a functional one.

---

## New issues found in v2

### 1. CRITICAL: No folder organization — 771 files in one flat directory

Opening the Lean Startup vault in Obsidian shows 771 files in alphabetical
order. No folders, no hierarchy, no entry point. A new user has no idea
where to start. This is hostile to exploration.

The whole point of the fractal structure is navigability. The pyramid gives
you root → L2 → L1 → L0 drill-down. But the file explorer doesn't reflect
this at all. You have to know the root note title to find it.

**Needed structure:**
```
vault/
  _index.md                    ← Entry point, links to root + navigation guide
  claims/
    atoms/                     ← Layer-0 (630 files)
    structure/                 ← Layer-1 parents (130 files)
    clusters/                  ← Layer-2 grandparents (10 files)
    root.md                    ← Layer-3 root (1 file)
  entities/
    people/                    ← Eric Ries, Steve Blank, etc.
    concepts/                  ← Build-Measure-Learn, MVP, etc.
    works/                     ← The Lean Startup (book)
    companies/                 ← IMVU, Toyota, Intuit
  .obsidian/snippets/          ← CSS
```

This makes the vault navigable even without graph view. Users can browse
`claims/structure/` for the mid-level summary, or drill into `claims/atoms/`
for evidence. Entity types are browsable by category.

Obsidian resolves wikilinks across folders, so `[[Eric Ries]]` in an atom
still links to `entities/people/Eric Ries.md`. No link breakage.

### 2. No index/entry page

There's no `_index.md` or `START HERE.md` that:
- Names the book and author
- Links to the root note
- Explains the vault structure
- Lists key navigation paths (by priority, by domain, etc.)
- Shows tag filter recipes for graph view

Without this, a user opens the vault and is lost.

### 3. Root note links to entities instead of L2 children

The root note's first wikilinks go to `[[The Lean Startup]]` and
`[[Build-Measure-Learn]]` (entities), not to the layer-2 cluster notes.
This happens because `reinforce_links` replaced entity mentions in the
root's prose with wikilinks, which is correct for entities but confuses
the navigation — clicking the first link takes you to an entity stub,
not the next level of the argument.

The root should primarily link to its L2 children (the argument structure),
with entity links as secondary.

### 4. 52 orphan notes in Mom Test vault

52 notes have zero incoming AND zero outgoing links. These are mostly
entity notes (like "App stores", "B2B", "Desk research") and some atomic
claims that weren't wikilinked by any parent. They exist as disconnected
islands in the graph.

Causes:
- Entity linking only processed the first 100 claims (agent had a cap)
- Some entity notes were created for concepts that don't appear verbatim
  in any claim body (e.g., "App stores" — the claims say "app store")
- Some claims from later extraction batches didn't get picked up by grouping

### 5. 73 "unknown" kind notes in Lean Startup

73 notes have no `kind` field in their YAML. These are claims from the
grouped files where agents didn't always preserve metadata consistently.
The fix-vault code tries to infer kind from tags, but some notes have
inconsistent tag formats.

### 6. Some body text is just a Parent backlink

Several layer-0 atoms have bodies that read:
```
Parent: [[Some parent note title]]
```

That's it — no actual claim text. This happens when a grouping agent
wrote the child-to-parent assignment as the entire body instead of
appending it to the existing body. The original claim body was lost.

### 7. Entity notes have minimal bodies

Entity notes like `[[Validated Learning]]` have bodies like:
```
Validated learning is a rigorous method for demonstrating progress
when one is embedded in the soil of extreme uncertainty.
```

One sentence. No wikilinks to claims that reference the entity. No
"Referenced by" section. The entity exists as a node but doesn't
help you navigate to the claims that discuss it. In a well-built
vault, an entity page would be a hub showing all related claims.

---

## What to build next

### Priority 1: Folder organization + index page

Create `_index.md` as the vault entry point with:
- Book title, author, publication year
- Link to root note
- Table of contents (L2 clusters as a bulleted outline)
- Quick filters for graph view
- Stats (total claims, entities, layers)

Organize files into subfolders by layer and entity type. Obsidian
handles cross-folder wikilinks natively.

### Priority 2: Entity hub pages

Each entity note should include a "Referenced by" section listing
every claim that mentions it. This turns entities from dead-end stubs
into navigation hubs. Pure text processing — no LLM needed.

### Priority 3: Fix orphan notes

Run a second pass of entity linking on ALL claims (not just first 100).
Match entity aliases case-insensitively. Promote remaining orphans by
finding the nearest parent or creating new groupings.

### Priority 4: Restore lost claim bodies

For layer-0 atoms whose body is just a Parent backlink, restore the
original body from the deduped claims file and re-append the Parent line.

### Priority 5: Cross-vault operations

Now that both vaults are clean, implement:
- `fractal compare vault-lean-startup-v2/ vault-mom-test-v2/` — find
  shared claims, unique contributions, and tensions between the books
- `fractal distill vault-lean-startup-v2/ vault-mom-test-v2/` — build
  a meta-pyramid from both books' roots

These are the operations that make the format a true knowledge substrate
rather than just a summary tool.
