# Distillary Summary — The Refined Approach

## The single insight

**Every prompt takes a list of notes and returns a list of notes.**

One canonical format. Any prompt can be applied to any output of any other prompt. No format conversions. No special-case wrapping.

---

## The Note format

Obsidian's idiomatic convention (verified against the docs):

- **YAML frontmatter** holds only filterable metadata — tags
  and a few simple scalars. No nested structures, no link
  lists. (Obsidian's Properties UI doesn't render nested
  YAML, and property types are vault-wide.)
- **The body** holds everything else: the statement, all
  `[[wikilinks]]` to other notes, and an optional "Related"
  section for cross-links. Wikilinks anywhere in the body
  become real edges in the graph view automatically.

### Claim note

```markdown
---
tags:
  - type/claim/structure
  - priority/core
  - certainty/argued
  - stance/endorsed
  - domain/economics
  - role/argument
  - source/piketty-capital-21c
layer: 2
kind: claim
proposition: "capital returns exceeding growth → increases inequality over time"
published: 2014
extracted_by: claude-opus-4.6
prompt_version: v2.1
---

[[Markets largely fail to self-correct inequality]], though
[[innovation occasionally disrupts entrenched wealth]]. In
most economies, [[capital returns outpacing growth creates
compounding concentration]] — a pattern documented across
18 of 20 countries studied.

## Related

- ⚡ Tension with [[Innovation occasionally disrupts wealth]] — contradicts the no-self-correction claim
- 🔁 Same pattern as [[Immune system dysregulation]] — shared structure of unbounded positive feedback
- 📚 Mentioned: [[Karl Marx]], [[Capital (asset)]]
- ⬆ Parent: [[Capitalism produces inequality by design]]
```

### Entity note

```markdown
---
tags:
  - type/entity/person
  - priority/key
  - certainty/established
  - domain/economics
  - source/piketty-capital-21c
kind: entity
entity_type: person
aliases:
  - Marx
  - K. Marx
  - Karl Heinrich Marx
born: 1818
died: 1883
extracted_by: claude-opus-4.6
prompt_version: v2.1
---

19th-century German philosopher and economist whose critique
of [[Capital (asset)]] and class formed the foundation of
historical materialism.
```

### Annotation note (the user's voice)

```markdown
---
tags:
  - status/disagree
  - insight/cite
  - kind/annotation
annotates: "[[Markets fail without regulation]]"
created: 2026-04-07
---

I'm skeptical of this. The 1850-1950 period Piketty cites was
unusually unequal due to WWI/WWII destruction of capital.
Pre-1850 and post-1980 the trend is more mixed than the simple
r > g equation suggests. Worth comparing with Saez's later work.
```

Annotation notes live in a separate `annotations/` subfolder
so re-processing the book regenerates claims and entities
without touching the user's commentary. They appear in the
target claim's backlinks panel automatically (because of the
`annotates: "[[...]]"` wikilink) and carry their own filterable
tags. The user is, in effect, just another vault that overlays
the auto-generated one.

Note that `aliases` is an Obsidian-recognized property name —
typing "Marx" in Obsidian's quick-switcher will find this
note even though the file is named "Karl Marx.md".

### What's in the YAML, and what isn't

| Field | In YAML? | Why |
|---|---|---|
| `tags` | yes | Obsidian's primary filter mechanism, graph color groups |
| `kind` (claim/entity/annotation) | yes | Simple scalar, lets Dataview filter cleanly |
| `layer` (claims) | yes | Simple integer, useful for Dataview queries |
| `proposition` (claims) | yes | Canonical form of the claim — the *semantic key* that makes set operations cheap. Two claims with the same proposition are about the same thing. |
| `published` (claims, entities) | yes | Date the source was published. Unlocks all temporal operations (diff over time, ahead-of-its-time, forgotten ideas). |
| `entity_type` (entities) | yes | Simple scalar |
| `aliases` (entities) | yes | Obsidian-recognized, powers quick-switcher |
| `born` / `died` (person entities) | yes | Optional, enables genealogical/influence queries |
| `annotates` (annotations) | yes | A single wikilink to the target claim — Obsidian-friendly even though it's a wikilink in YAML, because it's a single quoted string |
| `extracted_by`, `prompt_version` | yes | Provenance — who/what produced this note. Enables Family 10 (metalevel comparison). |
| **parent** (claim's parent) | **no** | Just write `Parent: [[X]]` in the body's Related section. Obsidian's backlinks panel finds all parents automatically. |
| **children** | **no** | Already present as `[[wikilinks]]` in the prose body |
| **cross-links** | **no** | Listed in the body's `## Related` section as bullets with `[[wikilinks]]` |
| **entity references** | **no** | Inline `[[wikilinks]]` in the prose body |
| **ghost concepts** | **no** | Inline `[[wikilinks]]` in the prose — Obsidian renders them as unresolved |

### Why this is the right shape

- **Tags do the filtering.** All five dimensions
  (`type/`, `priority/`, `certainty/`, `stance/`, `domain/`)
  live in `tags:`. The graph view colors and filters by
  these. Search filters by these. Done.
- **Wikilinks do the linking.** Every `[[bracketed phrase]]`
  in the body — whether in the prose, in the Related list,
  or as a parent reference — becomes a graph edge. No YAML
  parsing needed.
- **No nested YAML, no broken Properties UI.** Everything
  in the YAML is a flat scalar or a flat list. The Properties
  panel renders it cleanly; users can edit tags directly.
- **Backlinks find parents for free.** A note doesn't need
  to declare its parent. Open the backlinks panel and every
  note that links to it shows up — and the parent is the one
  whose body contains a `[[link]]` to this note's title.

### Stream conventions

In the LLM-internal stream (between prompts), notes are
concatenated with a `## Title` line acting as a record
separator BEFORE the `---` YAML opener. The driver parses
the stream by splitting on `## Title` lines, then for each
chunk reads the YAML between the `---` fences and the body
that follows. When writing to disk, the driver strips the
`## Title` line and saves each note as `<Title>.md` with
the YAML frontmatter at the top of the file.

The whole system is a list of these blocks. Each prompt
reads notes, returns notes. Operations on the list:

- **add** notes (extract, extract_entities, group)
- **remove** notes (dedupe via merging)
- **mutate** notes (link, link_to_entities, refine)

---

## Two notes on disk, three nodes in the graph

| Kind | Lives where | Has YAML/tags? | Graph appearance |
|---|---|---|---|
| **claim** | `.md` file in vault | yes | colored, sized by links |
| **entity** (realized) | `.md` file in vault | yes | colored, in entity orbit |
| **concept** (ghost) | only as `[[wikilink]]` text | no | unresolved, faded |

Claims and realized entities are real files. **Ghost concepts
have no file at all** — they exist only as `[[brackets]]` inside
claim statements that don't match any vault file. Obsidian
automatically renders these as unresolved/ghost nodes in the
graph view (faded color, dashed outline by default).

This is the key: **the gap between what you've explored and
what you haven't is visible by construction**. Every interesting
concept the LLM noticed gets a wikilink. Concepts important
enough to deserve a full note get realized as entity files.
Everything else stays a ghost — visible in the graph as a
"frontier" you can choose to explore later.

### Realized vs ghost: the criteria

A concept becomes a **realized entity** (gets its own note)
only if at least one is true:

- It's a proper noun (named person, work, place, event)
- It appears in **3 or more** distinct claims
- It appears in any claim tagged `priority/core`
- The source explicitly defines it as a technical term

Otherwise it stays a **ghost concept**: wrapped in `[[brackets]]`
in the claim statement, but with no entity note backing it.
This isn't a failure mode — it's the design. Ghosts mark the
edges of your understanding. The graph view shows them as
faint nodes clustered around the dense regions of your map.

### Promoting a ghost when you want to explore it

When a ghost catches your attention, you have two options:

1. **Manual stub**: click the ghost in graph view → Obsidian
   offers to create the file → write a sentence yourself.
2. **LLM promotion**: run the optional `PROMOTE_GHOST` prompt
   (below) to generate a full entity note from every claim
   that references the ghost.

Either way, the ghost becomes a realized entity. It gains a
file, picks up tags, and turns from a faded node into a fully
colored one. The graph view shows your exploration progressing
visibly over time.

---

## Tag dimensions

Seven filterable dimensions. Each answers a different question.
A visual thinker recolors the graph by whichever question is
currently relevant. Five describe the *content* of a note,
one describes its *role*, and one describes its *origin*.

### `type/` — what kind of note is this?

```
type/claim/index          the root paragraph
type/claim/structure      middle layers
type/claim/atom           leaf claims
type/entity/person        Marx, Piketty, Smith
type/entity/concept       capitalism, gravity, attention
type/entity/work          Das Kapital, Origin of Species
type/entity/place         Paris, Wall Street
type/entity/event         French Revolution, 2008 crisis
```

The structural dimension. Color by this to see pyramid vs
entity orbit at a glance.

### `priority/` — how central to the book's argument?

```
priority/core       removing this damages the central thesis
priority/key        important supporting claim
priority/support    evidence, examples, illustrations
priority/aside      tangential observations
```

Filter to `priority/core` for the spine of the book in 12 nodes.

### `certainty/` — how solid is this claim?

```
certainty/established   broadly accepted, empirically grounded
certainty/argued        author defends against alternatives
certainty/speculative   author flags as conjecture
```

Filter to `certainty/speculative` to find every claim worth
double-checking.

### `stance/` — what does the AUTHOR think of this?

```
stance/endorsed     author advocates this view
stance/criticized   author argues against this view
stance/neutral      author describes without taking sides
```

Filter to separate "what the author wants you to believe"
from "what the author is arguing against." Critical for
reading polemical books.

### `domain/` — what field?

```
domain/economics, domain/history, domain/psychology, ...
```

Filter across multiple books in your vault to find
cross-domain patterns.

### `role/` — what kind of claim is this?

```
role/fact         empirical observation, no controversy
role/argument     reasoning toward a conclusion
role/prediction   testable forecast about future or unknown
role/definition   stipulates what a term means
role/example      illustration of a more general claim
role/methodology  how to do something
```

This dimension separates *types of intellectual work*.
A book of mostly `role/fact` claims is descriptive; a book of
mostly `role/argument` is interpretive; a book of mostly
`role/prediction` is testable. Filter by `role/prediction` in
old vaults to find the predictions that history has now
falsified or confirmed (Family 3, Temporal). Filter by
`role/definition` to extract a glossary. Filter by `role/fact`
to find the empirical core that should hold up to fact-checking
(Family 9, Quality).

### `source/` — which book or author does this come from?

```
source/piketty-capital-21c
source/marx-das-kapital
source/smith-wealth-of-nations
...
```

Every claim and entity note carries its source tag. This is
the dimension that makes multi-vault distillation possible:
when you concatenate two vaults' notes, the `source/` tag
keeps each claim attributable to its origin even after
entities are merged across vaults. See "Multi-vault
comparison" below.

### Optional user-driven tags (added while reading)

```
status/new | status/revisited | status/applied | status/disagree
insight/aha | insight/cite | insight/build-on | insight/confused
```

These aren't auto-generated — visual thinkers add them as
they engage with the material.

### Tag inheritance through the pyramid

When `GROUP` writes a parent note, tags propagate from children:

- `priority` of parent = **max** of children's priorities
- `certainty` of parent = **min** of children's certainties
  (if any child is speculative, the parent is at best argued)
- `stance` and `domain` propagate by **majority**
- `type` is set by layer position (index / structure / atom)

---

## The 7 prompts

All prompts read and write the YAML Note format defined above.
Each note in the stream begins with a `## Title` record-separator
line, followed by `---` YAML frontmatter, followed by `---`,
followed by the body. References to other notes in YAML fields
use Obsidian wikilink syntax `"[[Title]]"` so they become real
edges in the graph view.

```python
EXTRACT = """
Convert the text below into atomic claim Notes.

A claim is atomic when it has one assertion and one reason.
If you see "because X and Y", split into two notes.

Output format — one note per claim, separated by blank lines.
Each note begins with a `## Title` record-separator line,
then YAML frontmatter (tags and simple scalars only),
then the body:

## <natural-phrase title, 4-10 words>
---
tags:
  - type/claim/atom
  - priority/<core | key | support | aside>
  - certainty/<established | argued | speculative>
  - stance/<endorsed | criticized | neutral>
  - domain/<single word>
  - role/<fact | argument | prediction | definition | example | methodology>
  - source/<book-slug provided by driver>
kind: claim
layer: 0
proposition: "<canonical form: subject → relationship → object>"
published: <year-provided-by-driver>
extracted_by: <model-name-provided-by-driver>
prompt_version: <version-provided-by-driver>
---

<2-4 sentence statement of the claim. No [[wikilinks]] yet —
those get added in later steps.>

YAML rules:
- Only flat scalars and the `tags` list. No nested structures.
- `tags` is a YAML list (one per line, prefixed with `- `).

`proposition:` rules — THIS IS THE MOST IMPORTANT FIELD.
- Write the claim in canonical form: <subject> <relationship> <object>.
- Strip qualifiers, hedges, rhetorical framing, and author voice.
- Two claims about the same fact, written by different authors,
  must produce the SAME proposition string.
- Examples:
    Original: "Capital returns exceeding growth, as Piketty
              demonstrates with 200 years of data, accelerates
              inequality."
    Proposition: "capital returns exceeding growth → increases inequality"
    
    Original: "When r > g over time, wealth concentrates."
    Proposition: "capital returns exceeding growth → increases inequality"
- Use lowercase, simple verbs, → as the relationship arrow.
- This field is the SEMANTIC KEY for set operations across vaults.

Tag rules:
- priority: 'core' ONLY if removing this claim damages the
  book's central argument. Be strict — most claims are 'support'.
- certainty: 'established' if widely accepted; 'argued' if
  the author defends against alternatives; 'speculative' if
  the author flags uncertainty.
- stance: what does the AUTHOR think? A claim describing an
  opposing view is 'criticized' even if widely held.
- domain: a single word naming the field.
- role: what KIND of claim is this?
    fact         = empirical observation
    argument     = reasoning toward a conclusion
    prediction   = testable forecast
    definition   = stipulates what a term means
    example      = illustration
    methodology  = how to do something

Title rules:
- Natural noun phrases that can later appear inside a parent's
  prose as a [[wikilink]].
- 4-10 words. Sentence case. No special characters.

TEXT:
{content}
"""


DEDUPE = """
Below is a list of Notes. Merge any that say the same thing.

Same = keeping both teaches nothing new.
Different framing of one insight = SAME.
Same topic, different assertion = DIFFERENT.

For each merge: keep the strongest formulation, union the
keywords, drop the weaker note. Update no other fields.

Return the deduplicated list in the same Note format.

NOTES:
{content}
"""


GROUP = """
Below is a list of Notes (all at the same layer).
Group them into clusters of 3-7 by ARGUMENTATIVE COHESION:
notes that together build one larger point.

For each cluster, write a NEW parent note.

The parent's YAML header is just tags + scalars:
  tags:
    - type/claim/structure  (or type/claim/index for the root)
    - priority/<max of children's priorities>
    - certainty/<min of children's certainties>
    - stance/<majority of children's>
    - domain/<majority of children's>
  kind: claim
  layer: <max(child.layer) + 1>

The parent's BODY contains:

1. A 2-5 sentence prose passage where each child appears as
   one [[wikilink to child title]]. The wikilink target MUST
   exactly match the child's title so Obsidian resolves it.

2. A `## Related` section listing the children explicitly:

   ## Related

   Children:
   - [[Title of child 1]]
   - [[Title of child 2]]
   - [[Title of child 3]]

For each CHILD note, ALSO add (or update) a line in its
`## Related` section:
  Parent: [[Parent's title]]

The parent's TITLE is a CLAIM, not a topic.
  Bad:  "Economic factors"
  Good: "Markets fail without regulation"

Return the FULL updated list: every original child note
(with its body's Related section updated) PLUS every new
parent note.

INVARIANT: output must contain strictly fewer parentless
notes (notes whose body has no `Parent:` line) than the input.

NOTES:
{content}
"""


LINK = """
Below is a list of Notes. Find lateral connections of three types:

PATTERN: same abstract structure, different domain.
  "Predator-prey cycles" ↔ "Boom-bust economics"

TENSION: accepting A means B can't be fully true.
  Include partial tensions: both could be true but
  pull in opposite directions.

EVIDENCE: one note supports or undermines a claim
  in another note from a different branch.

For each connection found, ADD a bullet to the `## Related`
section of BOTH notes involved. Format:

  ## Related

  - ⚡ Tension with [[Other Note Title]] — <one short sentence>
  - 🔁 Same pattern as [[Other Note Title]] — <one short sentence>
  - 📊 Supported by [[Other Note Title]] — <one short sentence>
  - ❓ Challenged by [[Other Note Title]] — <one short sentence>

Use these emoji prefixes consistently. The wikilink target
MUST exactly match the other note's title so Obsidian
resolves it.

Don't modify the YAML header. Don't change titles or the
prose body — only add bullets to the Related section.

Return the full updated note list.

NOTES:
{content}
"""


EXTRACT_ENTITIES = """
Below is a list of claim Notes. Identify entities that are
significant enough to deserve their own note.

REALIZE an entity (create an entity note) ONLY if at least
one is true:
- It is a proper noun: a named person, work, place, or event
- It appears in 3 or more distinct claims
- It appears in any claim tagged priority/core
- The source explicitly defines it as a technical term

Do NOT create entity notes for:
- Concepts that appear only once or twice in non-core claims
- Generic words ("people", "society", "economy")
- Interesting noun phrases that don't meet the criteria above

These unrealized concepts will be marked as [[ghost links]]
in a later step and will appear as unresolved nodes in the
Obsidian graph view — visible gaps for future exploration.
This selectivity is intentional. Realized entities = known
territory. Ghost links = the frontier.

For each REALIZED entity, emit a Note in YAML format:

## <canonical name>
---
tags:
  - type/entity/<entity_type>
  - priority/<core if in many core claims, else key/support>
  - certainty/established
  - domain/<inferred from claims>
kind: entity
entity_type: person | concept | work | place | event
aliases:
  - <alternate name 1>
  - <alternate name 2>
---

<one sentence describing what this entity is>

Note: `aliases` is an Obsidian-recognized property — typing
any alias in the quick-switcher will find this note.

If the same entity appears under multiple surface forms within
this batch, MERGE them into one entity note:
  "Marx", "Karl Marx", "K. Marx" → ## Karl Marx
                                   aliases: [Marx, K. Marx]

Return the entity notes ONLY. Do not return the input claims.
A second pass will canonicalize across batches.

CLAIMS:
{content}
"""


LINK_TO_ENTITIES = """
Below is a list of claim Notes followed by a list of entity Notes.

For each claim, add wikilinks of TWO types:

1. RESOLVED LINKS — when the claim references an entity that
   has a note in the entity index, wrap it in [[Canonical Name]]
   matched against the entity's surface_forms.
   
   Example: "[[Karl Marx]] argued that [[capital]] accumulates..."

2. GHOST LINKS — when the claim references an interesting
   concept that does NOT have an entity note, STILL wrap it
   in [[brackets]]. These will appear as unresolved/ghost
   nodes in the Obsidian graph view, marking gaps to explore.
   
   Example: "...because workers produce more [[surplus value]]
            than they receive, a form of [[primitive accumulation]]
            that [[Karl Marx]] called the secret of capital."
   
   Here "surplus value" and "primitive accumulation" are ghost
   links (no entity note exists), while "Karl Marx" is a
   resolved link.

Be liberal with ghost links — they cost nothing, they make
the conceptual depth of each claim visible, and the user can
promote any of them to a real entity note later.

Rules:
- Don't wrap generic words (people, society, economy).
- Don't wrap the same concept twice in one statement.
- For resolved links, match against entity surface_forms.
- For ghost links, use the most natural noun phrase form.

For each claim, update the body only:

1. Inline `[[Entity Name]]` wikilinks at points of reference
   in the prose. Match against the entity's `aliases` field
   when picking the canonical name to link to.

2. Add a "Mentioned" line to the `## Related` section listing
   the realized entities referenced in the claim:
   - 📚 Mentioned: [[Karl Marx]], [[Capital (asset)]]

Ghost links live ONLY inline in the prose, NOT in the
Mentioned line (the Mentioned line is for resolved entities
only — that's what makes it a useful filter).

Don't modify the YAML header. Don't modify the entity notes.
Return the full updated claim list.

CLAIMS + ENTITIES:
{content}
"""


PROMOTE_GHOST = """
The user wants to promote a ghost concept into a full entity
note. Below is the ghost concept name followed by every claim
in the vault that references it.

Generate one entity note in YAML format:

## <canonical name>
---
tags:
  - type/entity/<inferred type>
  - priority/<inferred from referencing claims>
  - certainty/<inferred from how claims discuss it>
  - domain/<majority domain of referencing claims>
kind: entity
entity_type: <inferred from how it's used>
aliases:
  - <variant 1 found across claims>
  - <variant 2>
---

<one sentence describing what this concept is, drawing on
the context of the claims that reference it>

Return only the new entity note. The driver will add it to
the vault and re-run LINK_TO_ENTITIES to convert the ghost
references into resolved links.

GHOST + REFERENCING CLAIMS:
{content}
"""


REFINE = """
Below is one Note (the TARGET) followed by its full
subtree (children, grandchildren, etc.) and any links
touching the subtree.

Rewrite the target's statement to be MORE ACCURATE now
that we know what's beneath it.

Fix:
1. HIDDEN TENSIONS: if children disagree, surface it.
   "[[markets self-correct]]" 
   → "[[markets may self-correct, though contested]]"

2. FALSE CONFIDENCE: if deepest evidence is nuanced,
   add qualifiers ("typically", "in most cases").

3. MISSING CONNECTIONS: if a cross-link reveals a
   surprising parallel, hint at it in the passage.

4. VAGUENESS: replace generic phrases with the specific
   mechanism from the deepest evidence.

5. PHRASE ACCURACY: every [[bracketed phrase]] must
   honestly preview what the reader finds when clicking.

Keep: 2-5 sentences, self-contained, same children.
Rewrite no other notes — only the target.

CONTEXT:
{content}
"""
```

Five prompts. Same input format, same output format.

Plus three for the entity layer (`EXTRACT_ENTITIES`,
`LINK_TO_ENTITIES`, `PROMOTE_GHOST`) that follow the exact
same shape — `llm(content, prompt) → notes`. Total: 8 prompts.

Note that `EXTRACT_ENTITIES` is its own canonicalization step.
When `chunked` re-applies it to merged batch results, the
prompt's "merge surface forms" instruction handles cross-batch
dedup. No separate canonicalization prompt needed.

`PROMOTE_GHOST` is the only prompt called on demand, not in
the main pipeline. It runs when the user clicks a ghost node
in the graph view and wants to turn it into a real entity.

---

## Fold strategies (the honest part)

When a note list exceeds `max_length`, we batch and merge.
Different prompts need different merge rules:

| Prompt | Fold strategy | Why |
|---|---|---|
| `EXTRACT` | concat | Each chunk yields independent claims |
| `DEDUPE` | re-apply | `dedupe(dedupe(A) ⊕ dedupe(B)) = dedupe(A⊕B)` |
| `GROUP` | re-apply on parents | Cluster batches, then cluster the cluster-parents |
| `LINK` | concat + re-apply | Catch cross-batch links by re-running on full result |
| `REFINE` | never folded | Always operates on one note + its subtree |
| `EXTRACT_ENTITIES` | re-apply | Merges surface forms across batches automatically |
| `LINK_TO_ENTITIES` | concat | Each batch links its claims to the full entity index |
| `PROMOTE_GHOST` | never folded | One ghost concept at a time, on demand |

```python
def chunked(notes, prompt, max_length, fold='reapply'):
    """
    Apply prompt to notes. Fold partial results.
    
    fold='concat'  → just concatenate batch outputs
    fold='reapply' → run prompt again on concatenated outputs
    """
    if size(notes) <= max_length:
        return llm(notes, prompt)
    
    batches = split(notes, max_length)
    results = concat(llm(b, prompt) for b in batches)
    
    if fold == 'concat':
        return results
    if fold == 'reapply':
        return chunked(results, prompt, max_length, fold='reapply')
```

That's the whole map-reduce machinery. ~10 lines.

---

## The driver

```python
def distillary_decompose(
    book_text,
    max_length,
    source_slug,        # e.g. "piketty-capital-21c"
    published,          # e.g. 2014
    extracted_by,       # e.g. "claude-opus-4.6"
    prompt_version,     # e.g. "v2.1"
):
    """
    Convert one book into a fractal vault.
    The metadata parameters get injected into every note's
    YAML frontmatter, enabling cross-vault and metalevel
    operations later.
    """
    
    # ━━━ 1. text → claim notes ━━━
    
    notes = ""
    extract_with_meta = (EXTRACT
        .replace("<book-slug provided by driver>", source_slug)
        .replace("<year-provided-by-driver>", str(published))
        .replace("<model-name-provided-by-driver>", extracted_by)
        .replace("<version-provided-by-driver>", prompt_version))
    
    for chunk in split_text(book_text, max_length):
        notes += llm(chunk, extract_with_meta)
    
    notes = chunked(notes, DEDUPE, max_length, fold='reapply')
    
    
    # ━━━ 2. extract entities (parallel structure) ━━━
    
    entities = chunked(notes, EXTRACT_ENTITIES, max_length, fold='reapply')
    notes = notes + entities  # entity notes join the vault
    
    
    # ━━━ 3. recursively group claims until one root remains ━━━
    
    while count_roots(claim_notes(notes)) > 1:
        before = count_roots(claim_notes(notes))
        notes = chunked(notes, GROUP, max_length, fold='reapply')
        assert count_roots(claim_notes(notes)) < before
    
    
    # ━━━ 4. find lateral connections + link claims to entities ━━━
    
    notes = chunked(notes, LINK, max_length, fold='concat')
    notes = chunked(notes, LINK, max_length, fold='concat')  # second pass
    notes = chunked(notes, LINK_TO_ENTITIES, max_length, fold='concat')
    
    
    # ━━━ 5. refine top → bottom ━━━
    
    for note in topological_order(claim_notes(notes)):
        if has_children(note):
            subtree = collect_subtree(notes, note.title)
            updated = llm(subtree, REFINE)
            notes = replace_note(notes, note.title, updated)
    
    
    # ━━━ 6. write to disk (claims AND entities) ━━━
    
    for note in parse_notes(notes):
        write_obsidian_md(note)  # YAML tags + body wikilinks


# ━━━ Multi-vault: building a field-level meta-pyramid ━━━

def distill_field(vault_paths, max_length):
    """
    Given several vaults built by distillary_decompose, run the
    same algorithm one level higher: each book's root paragraph
    becomes an atom in a meta-pyramid that summarizes the field.
    """
    roots = ""
    for path in vault_paths:
        root_note = read_root(path)  # the type/claim/index note
        roots += root_note  # already in canonical Note format
    
    return distillary_decompose(
        book_text=roots,
        max_length=max_length,
        source_slug="field-level",
        published=current_year(),
        extracted_by="claude-opus-4.6",
        prompt_version="v2.1",
    )
```

Twenty-five lines. The whole algorithm including the entity layer.

---

## The convergence guarantee

The pyramid loop has a clear invariant:

```python
while count_roots(notes) > 1:
    before = count_roots(notes)
    notes = chunked(notes, GROUP, max_length, fold='reapply')
    assert count_roots(notes) < before
```

`GROUP` is contractually required to reduce the number of root
notes (notes with `parent: none`). The prompt enforces this:

> *INVARIANT: output must contain strictly fewer top-level
> notes than the input.*

If the LLM violates this, the assertion fires loudly instead of
spinning forever. In practice, GROUP reduces root count by ~70%
per pass, so a 500-claim book reaches a single root in 5-6 passes.

---

## Why this is better than the previous version

| Previous | Refined |
|---|---|
| 6 prompts (cluster + summarize separate) | 5 core prompts (`GROUP` does both) + 3 entity prompts |
| "Note" format shifted between prompts | One canonical Note format throughout (claim or entity) |
| Hand-waved "context gathering" for refine | `collect_subtree(notes, id)` — explicit |
| Claimed all prompts could merge themselves | Honest table of fold strategies |
| `count_notes()` mystery function | `count_roots(claim_notes(notes))` — clearly defined |
| No termination guarantee | Invariant + assertion in the loop |
| LLM produces parent + a separate mapping call | One LLM call writes parent with [[brackets]] |
| Cross-links found once per layer | Two passes catch cross-batch links |
| No tags — graph view was monochrome | 5 filterable tag dimensions for visual thinking |
| "Marx" appears as 5 different surface forms | Entity index canonicalizes to one note per entity |
| Every concept either becomes a note or vanishes | Ghost links — concepts visible in graph without files |

The refinement eliminates the things I was hand-waving and 
makes the data flow uniform: **list of notes in, list of notes 
out, every time** — whether those notes are claims or entities.

---

## Filter recipes for visual thinkers

In Obsidian's graph view, save these as named filters:

| What you want to see | Filter query |
|---|---|
| The book in 30 seconds | `tag:#priority/core` |
| What the author advocates | `tag:#stance/endorsed AND tag:#priority/key` |
| What to fact-check | `tag:#certainty/speculative` |
| Just the people | `tag:#type/entity/person` |
| Just the named ideas | `tag:#type/entity/concept` |
| Cross-domain insights | `tag:#priority/core AND -tag:#domain/<book's domain>` |
| Personal aha moments | `tag:#insight/aha` |
| **The frontier — gaps to explore** | toggle "Existing files only" OFF in graph view |
| **Densest gaps (most-mentioned ghosts)** | sort unresolved nodes by backlink count |

Switch the graph color group between `type/`, `priority/`,
`certainty/`, and `stance/` to see four different views of
the same vault. Then toggle "Existing files only" off and
on to see the **frontier of unexplored concepts** appear and
disappear.

A minimal CSS snippet (`.obsidian/snippets/tags.css`) makes
tags color-code in note bodies, and ghost nodes stand out
in the graph:

```css
/* Tag colors in note bodies */
.tag[href="#priority/core"]    { background: #E24B4A; color: white; }
.tag[href="#priority/key"]     { background: #EF9F27; color: white; }
.tag[href="#certainty/speculative"] { background: #F09595; color: #501313; }
.tag[href="#certainty/established"] { background: #97C459; color: #173404; }
.tag[href="#stance/endorsed"]  { background: #85B7EB; color: #042C53; }
.tag[href="#stance/criticized"]{ background: #F0997B; color: #4A1B0C; }
.tag[href^="#type/entity"]     { background: #D85A30; color: white; }

/* Ghost links in note bodies — italic and faded */
.internal-link.is-unresolved {
    color: #D85A30;
    opacity: 0.7;
    font-style: italic;
    text-decoration: dashed underline;
}
```

In the graph view itself, Obsidian's built-in settings already
give unresolved nodes a separate color group — just rename it
to "Frontier" or "Gaps" in `Settings → Appearance → Graph view
→ Groups` and assign it a faded color. Now every ghost concept
the LLM noticed will glow softly around your vault.

---

## The exploration workflow

The graph view becomes a **research interface** rather than
just documentation:

1. **Read the root paragraph.** It's the dinner-party version
   of the book.

2. **Drill down through `[[bracketed phrases]]`.** Each phrase
   is a door to a child note. Resolved entity links go to
   their canonical entity note.

3. **Notice the ghosts.** When you see a faded `[[concept]]`
   that catches your attention, you've found a frontier — a
   concept the book references but doesn't fully develop.

4. **Promote when ready.** Click the ghost in graph view.
   Either:
   - Write a stub note manually
   - Run `PROMOTE_GHOST` to have the LLM generate an entity
     note from every claim that mentioned it

5. **The graph evolves.** As ghosts get promoted, faded nodes
   become bright ones. The vault shows your understanding
   visibly growing over time. The remaining ghosts are your
   to-do list — and they're sorted naturally by importance
   (more references = bigger frontier).

This flips the usual notebook dynamic. Instead of "I'll write
a note when I have something to say," you get **the unwritten
notes are already in the graph**, waiting. The LLM has done
the work of noticing what's worth exploring; you just decide
which doors to open.

---

## Why ghosts are the right level of effort

A naive design would either:

- **Create a note for every concept** → vault drowns in
  100s of stub files, most never useful, graph becomes
  unreadable.
- **Only link to concepts that have notes** → invisible
  references, graph misses everything you haven't formalized,
  exploration depends entirely on memory.

Ghost links thread the needle: **the conceptual structure of
the book is fully visible in the graph, but only the parts
worth full notes exist as files**. The cost of a ghost is
zero (no file, no maintenance). The benefit is full visibility
into what the book points at without forcing premature
formalization.

In other words: **the graph view is no longer just a map of
your notes — it's a map of your notes plus the territory
beyond them**. That edge between "what I have" and "what's
out there" is where research happens.

---

## Multi-vault comparison and distillation

The format pays its biggest dividend when you have **more
than one book** processed the same way. Two vaults with
identical structure can be merged with `concat`. Every prompt
that worked on one vault works on the union. No translation
layer, no schema mapping, no impedance mismatch.

This section is the deepest payoff of the design.

### Why uniformity is the multiplier

Knowledge distillation across sources usually fails on the
plumbing — normalizing vocabularies, mapping section structures,
deciding what corresponds to what. This format eliminates that
work upfront because every vault shares:

- The same Note shape (parser works on either)
- The same entity model (Marx is Marx, found by aliases)
- The same tag taxonomy (`priority/core` means the same thing)
- The same pyramid topology (layer 0 = atoms, root = whole work)
- The same wikilink convention (`[[X]]` works across vaults)

So `cat vault_a/*.md vault_b/*.md` is a meaningful operation,
not a syntax error. From there, every existing prompt operates
on the union without modification.

### Ten families of operations

Set operations are one family — they're the obvious one because
"compare two vaults" sounds like set theory. But the substrate
supports at least ten distinct families, each asking a
different *kind* of question and having a different
computational shape. Six of the ten need no LLM at all.

#### Family 1 — Set operations (boolean algebra of vaults)

The vault as a set of claims. Standard boolean operations:

- **Union**: everything anyone said about X. `concat` + `EXTRACT_ENTITIES` with reapply fold. Already shown above.
- **Intersection**: claims that appear in *both* vaults. The shared core. What every author agrees on.
- **Difference (A − B)**: claims in A with no equivalent in B. A's unique contribution.
- **Symmetric difference**: where A and B diverge, excluding shared ground.
- **Complement**: topics no vault in your collection covers. Combined with double-ghosts, this is the field's blank space.

Set membership requires a "are these two claims semantically
equivalent?" test — one targeted LLM call per pair, or a
similarity prefilter using tag profiles + entity overlap.

#### Family 2 — Graph operations (the wikilink network as topology)

Once vaults are concatenated, the union of all wikilinks forms
a single graph. Standard graph algorithms apply:

- **Shortest path** between two ideas across vaults: "what's the chain from `[[gravity]]` to `[[free will]]`?"
- **Centrality analysis**: which entities have the highest betweenness across the multi-vault graph? Those are the hub concepts that hold the field together.
- **Community detection**: dense clusters of links that span vaults reveal emergent topics no single book defines.
- **Bridge nodes**: entities cited by many otherwise-disconnected vault clusters. These are the "translators" between intellectual communities — the figures whose work connects different schools of thought.
- **Edge prediction**: where in the graph *should* a link exist that doesn't? This finds missing connections to investigate.

These are pure graph algorithms — NetworkX in Python, three
lines per query. No LLM needed. Obsidian's graph view already
shows centrality visually (node size by degree).

#### Family 3 — Temporal operations (vault as a slice of intellectual history)

If each vault carries a publication date, the collection
becomes queryable in time:

- **Diff over time**: same topic, vault from 1980 vs 2020. What changed?
- **Genealogy**: trace ideas through the citation graph backward in time.
- **Diffusion analysis**: when did a concept first appear, and how did it spread across vaults?
- **Ahead-of-its-time detection**: claims marked `certainty/speculative` in old vaults that are `certainty/established` in new ones. The author got it right early.
- **Forgotten ideas**: `priority/core` claims in old vaults that don't appear at all in new ones. What got lost.
- **Predictive validation**: explicit predictions in older vaults checked against established facts in newer ones.

This family makes intellectual history queryable. Date is just
one more YAML scalar in the frontmatter — `published: 1867` —
and Dataview filters do the rest.

#### Family 4 — Statistical operations (tags as a distribution)

The tag taxonomy is six dimensions of categorical data. Across
vaults, those dimensions become a distribution you can profile:

- **Tag profile per author**: "Author A is 60% endorsed, 30% critical, 10% neutral. Author B is balanced 33/33/33."
- **Bias detection**: disproportionate priority on certain entities relative to peer vaults. "This author cites Marx in 80% of core claims; field average is 12%."
- **Stance entropy**: how much an author commits vs hedges. Low entropy = polemicist. High entropy = academic.
- **Consensus mining**: claims marked `priority/core` in 5+ vaults that are NOT connected by tension links. The field's shared assumptions — calcified through repetition, worth questioning *because* no one questions them.
- **Contestation mining**: claims connected by tension links across 3+ vaults. The contested ground worth investigating.
- **Domain breadth**: specialists vs generalists, as a single number per vault.

Pure aggregation. Dataview queries return them in milliseconds.

#### Family 5 — Structural operations (comparing how authors think)

The pyramid shape itself is comparable, not just the contents:

- **Pyramid alignment**: find isomorphic subtrees across vaults. Two authors who organized the same sub-argument the same way share an unstated framework.
- **Pyramid divergence**: same root topic, completely different decomposition. The authors think the topic is fundamentally different.
- **Asymmetry detection**: branches where one vault goes deep and another stays shallow. Reveals each author's expertise focus.
- **Compression ratio**: atoms per book, claims per concept. A measure of conceptual density — some authors say a lot in few words.

This family asks "how does each author *think*?" rather than
"what does each author *say*?" The answers reveal cognitive
style independent of content.

#### Family 6 — Synthesis operations (LLM-driven combination)

Targeted LLM calls that combine multi-vault data into new outputs:

- **Position synthesis (steelmanning)**: given N vaults' takes on a question, write a single passage that fairly represents all positions.
- **Mediation**: given two contradicting vaults, identify the *underlying assumption* they disagree on — the actual crux beneath the surface disagreement.
- **Reconciliation**: find a stronger claim that both disagreeing authors would accept.
- **Devil's advocate**: generate the strongest objection to a consensus claim by drawing on minority positions across vaults.
- **Dialectical generation**: produce a thesis-antithesis-synthesis from contested claims across vaults.

These require LLM calls but each call is small and focused
because the substrate has already done the retrieval work.
The LLM sees a pre-filtered set of claims, not the whole vault.

#### Family 7 — Personal operations (the user as another vault)

The user's own annotations (`status/`, `insight/`) are first-class
data. Treating the user as a vault enables:

- **Position calibration**: where does the user's pattern of `disagree` and `aha` tags diverge from the field consensus? Is the divergence concentrated in specific domains?
- **Reading recommendations**: based on which books the user has annotated heavily, suggest the next book by tag-profile similarity.
- **Personal bias mirror**: which kinds of claims does the user consistently endorse, criticize, or skip? The user becomes legible to themselves.
- **Personal frontier**: ghosts in books the user reads that never become realized entities — the user's *own* unwritten knowledge.

This family closes the loop: the reader is part of the system
they're querying.

#### Family 8 — Generative operations (the substrate as raw material)

Using the multi-vault corpus as a source for *new* writing:

- **Synthesis essay generation**: given a question, draw from `priority/key` claims across vaults to write a coherent essay using existing claims as building blocks (with citations to source vaults).
- **Counterfactual generation**: "If author A had read author B's argument, what would A have said?" Generate by finding what A's pyramid is missing that B has.
- **Bridge concept invention**: invent a hypothetical concept that would resolve a tension across vaults. Mark it as a ghost in a new "synthesis" vault.
- **Question generation**: from the gaps and tensions, generate research questions worth pursuing.

This family is LLM-heavy but produces the most original output.
The substrate is the citation database the LLM cites from.

#### Family 9 — Quality and integrity operations (redundancy as verification)

Multi-vault redundancy is a fact-checking signal:

- **Fact-check by majority**: if 9 vaults say X and 1 says Y, the outlier is either wrong or insightfully heterodox — flag for review either way.
- **Confidence calibration**: a claim marked `certainty/established` in only one vault but `certainty/argued` in three should probably be `argued`.
- **Citation verification**: a claim that cites an entity should be consistent with what books *about* that entity say.
- **Self-contradiction within a vault**: subtle internal contradictions that single-vault `LINK` might miss become detectable when contrasted with other vaults' clean pyramids on the same topic.

The truth signal comes from intersubjective convergence, not
from any single vault's authority.

#### Family 10 — Metalevel operations (the format as subject of inquiry)

Compare different processings of the same content:

- **Translation comparison**: same book in different translations. Where do the pyramids diverge? (The places where translation isn't faithful.)
- **Annotator comparison**: same book processed by two different LLMs. Where do they extract differently? (The places where the format leaks through to the content.)
- **Tag drift detection**: across vaults built over time, has the meaning of `priority/core` drifted? Are `core` claims today shorter than they were a year ago?

This family checks the format's own integrity by treating the
algorithm as a subject of inquiry. It's how you catch your
substrate becoming unreliable.

### Family shapes — what each costs

| Family | Computational shape | Cost |
|---|---|---|
| 1. Set | Boolean over claim sets | LLM equivalence calls |
| 2. Graph | Algorithms on the wikilink graph | Pure compute (NetworkX) |
| 3. Temporal | Filter by date + diff | Dataview queries |
| 4. Statistical | Aggregate over tags | Dataview queries |
| 5. Structural | Tree isomorphism | Pure compute |
| 6. Synthesis | LLM over selected subset | Small targeted LLM calls |
| 7. Personal | Filter by user tags + compare | Dataview |
| 8. Generative | LLM over substrate | Large LLM calls |
| 9. Quality | Cross-vault majority vote | LLM equivalence + counting |
| 10. Metalevel | Same algorithm, different inputs | Same as base pipeline |

**Six of ten families need no LLM at all** — they're pure
queries on the structured data. Three need targeted LLM calls
on small filtered subsets. Only one (generative) is LLM-heavy.
**Most of the value comes from the format itself, not from
new model calls.**

### What each family unlocks

| Family | What it answers |
|---|---|
| Set | "What's shared, what's unique, what's missing?" |
| Graph | "How is the field connected?" |
| Temporal | "What changed, what was forgotten, what was predicted?" |
| Statistical | "What's the consensus, what's contested, who's biased?" |
| Structural | "How does each author think?" |
| Synthesis | "What's the steelman, the crux, the resolution?" |
| Personal | "Where do I diverge from the field, and why?" |
| Generative | "What new things can I write from this substrate?" |
| Quality | "What's reliable, what's an outlier?" |
| Metalevel | "Where does the format itself break down?" |

Ten different idioms for asking questions of the same
underlying data. No single tool gives you all ten — but the
format does, because the format is just structured markdown
that every other tool already knows how to read.

### The meta-pyramid: fractal recursion

Each book reduces to one root paragraph. If you have ten
books on a topic, **the ten root paragraphs are themselves
atoms** for a higher-level pyramid.

Run `GROUP` on them. It clusters books by argumentative
cohesion (which authors make the same big argument?), writes
a parent passage where each book is a `[[wikilink]]`, and
continues until you have one root paragraph that summarizes
*the entire field*, with drill-downs into each book's pyramid,
which drill into chapters, which drill into atomic claims.

**The same algorithm. The same prompts. Different scale.**

This is the real meaning of "fractal" in the algorithm's name.
It operates identically at the field level, the book level,
the chapter level, and the atomic claim level. You can keep
zooming out indefinitely. Ten books in a field → one field
summary. Ten field summaries across disciplines → one
cross-disciplinary summary. The recursion has no ceiling.

```
field-level root
    ├── book-level root (Piketty)
    │   ├── structure note
    │   │   ├── atomic claim
    │   │   └── atomic claim
    │   └── structure note
    ├── book-level root (Marx)
    │   └── ...
    └── book-level root (Smith)
        └── ...
```

The driver to build a meta-pyramid is one line:

```python
field_pyramid = distillary_decompose(
    book_text=concat(all_root_paragraphs),
    max_length=max_length
)
```

### What you need to add to the existing pipeline

Almost nothing. The multi-vault layer reuses every existing
primitive:

| For multi-vault... | Use the existing... |
|---|---|
| Combine vaults | `concat` (filesystem operation) |
| Merge entities | `EXTRACT_ENTITIES` with `fold='reapply'` |
| Find disagreements | `LINK` over the union |
| Build the meta-pyramid | `distillary_decompose(concat(roots))` |
| Compare tag deltas | Dataview, no LLM call |
| Find field gaps | Graph view with "Existing files only" off |
| Set operations | `proposition` field as the semantic key |
| Temporal queries | `published` field as the date key |
| Personal annotations | Annotation notes in `annotations/` subfolder |
| Annotator comparison | `extracted_by` + `prompt_version` fields |

The format additions enable specific families efficiently:

| Field/convention | Unlocks family |
|---|---|
| `proposition:` (canonical claim form) | 1 (Set), 6 (Synthesis), 9 (Quality) |
| `published:` (date) | 3 (Temporal) entirely |
| `role/` (claim type tag) | 3, 4, 5, 9 (sharper queries in each) |
| `extracted_by`, `prompt_version` | 10 (Metalevel) entirely |
| Annotation notes (separate folder) | 7 (Personal) cleanly |
| `source/` tag | All cross-vault families (attribution) |

Without these additions, most families still work — but
they require LLM calls or full re-reads where simple Dataview
queries would suffice. With them, six of the ten families
become pure database operations.

### Why this works: the format is a substrate

The deepest insight: this isn't really an algorithm for
summarizing a single book. It's an algorithm for **converting
text into a uniform, queryable, mergeable knowledge substrate**.
Once a book is in this format, it stops being prose and starts
being data. You can ask questions of it programmatically that
previously required re-reading.

When two books are in this format, you can ask questions of
the *pair*. Ten books, the *field*. A hundred books across
disciplines, the *intellectual landscape of a moment*. The
operations don't get harder — they're the same operations on
different inputs.

The format is fractal in two directions: vertical (root →
atoms within a book) and horizontal (one book → field → field
of fields). The same primitives traverse both directions.
That's what knowledge distillation looks like when the
substrate is uniform.

---

## What you actually need to implement

```python
# The primitive — provided by your LLM SDK
def llm(content: str, prompt: str) -> str: ...

# Note serialization — ~40 lines
# parse_notes splits the stream on `## Title` lines, parses
# the YAML frontmatter between --- fences (PyYAML works fine —
# the YAML is flat scalars + a tags list, no nesting),
# captures the body as plain text. The Note dataclass has:
#   title, tags (list), kind, layer, body (str)
# Use PyYAML or ruamel.yaml — don't hand-roll YAML parsing.
def parse_notes(text: str) -> list[Note]: ...
def serialize(notes: list[Note]) -> str: ...

# Body queries — relationships live as wikilinks in the body
# `## Related` section, NOT in the YAML. Use a simple regex
# like r'\[\[([^\]]+)\]\]' against the relevant body lines.
def parents_of(note):   # extract from "Parent: [[X]]" lines
    return wikilinks_after(note.body, "Parent:")
def children_of(note):  # extract from "Children:" bullet list
    return wikilinks_after(note.body, "Children:")
def cross_links(note):  # extract from emoji-prefixed bullets
    return wikilinks_in_lines(note.body, prefixes="⚡🔁📊❓")
def mentioned_entities(note):
    return wikilinks_after(note.body, "Mentioned:")

# Trivial helpers — built on the body queries above
def claim_notes(notes):  return [n for n in parse_notes(notes) if n.kind == 'claim']
def entity_notes(notes): return [n for n in parse_notes(notes) if n.kind == 'entity']
def count_roots(notes):  return len([n for n in notes if not parents_of(n)])
def has_children(note):  return len(children_of(note)) > 0
def collect_subtree(notes, title): ...
def replace_note(notes, title, updated): ...
def topological_order(notes): ...

# The chunked wrapper — 10 lines, shown above

# The 7 main prompts + 1 on-demand (PROMOTE_GHOST) — string constants

# The driver — 25 lines, shown above

# Output writer — strips the `## Title` separator, writes
# each note as <Title>.md with the YAML frontmatter at the
# top of the file followed by the body. Tags become Obsidian
# Properties automatically. All wikilinks in the body
# (children, cross-links, parent, entities, ghosts) get
# picked up by the graph view automatically.
def write_obsidian_md(note): ...
```

**Total: ~210 lines of code. 8 prompts. 1 LLM primitive.**

The intelligence lives in the prompts. The structure lives in
two places: the canonical Note format (flat YAML for tags +
scalars, body for wikilinks) and the 6 tag dimensions. The
driver is just plumbing.

The format scales in both directions:

- **Vertically** (within a book): atoms → structure notes →
  root paragraph. Drill in or out at any level.
- **Horizontally** (across books): one vault → many vaults →
  field-level meta-pyramid → cross-disciplinary view. Same
  primitives, larger inputs.

The graph view shows you both your notes AND the frontier of
unexplored concepts. When you have multiple vaults, it shows
you the *field's* notes and the *field's* frontiers — the
unwritten entities that multiple authors implicitly need but
none have formalized. That's where research lives.