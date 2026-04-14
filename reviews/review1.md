# Distillary Pipeline Review — Honest Self-Reflection

## What we built

Two Obsidian vaults from two books using a multi-agent Claude pipeline:

| | Lean Startup | Mom Test |
|---|---|---|
| Input | 554K chars, 32 chunks | 175K chars, 11 chunks |
| Extracted claims | 598 | 201 |
| After dedupe | 561 | 148 |
| Entities | 30 | 44 |
| Layer-1 parents | 130 | 35 |
| Layer-2 clusters | 10 | 8 |
| Root note | 1 | 1 |
| Files in vault | 172 | 78 |
| Pipeline time | ~20 min | ~12 min |

---

## What went well

### 1. The agent architecture is dramatically faster than sequential API calls

The Gemini sequential approach was estimated at 2+ hours for one book. The parallel
haiku/opus agent approach did it in 20 minutes. The key insight: extraction is
embarrassingly parallel — every chunk is independent. Haiku handles it in seconds
per agent, and 16 agents running simultaneously collapse a 45-minute step into 2.5
minutes.

### 2. The haiku/opus split is the right division of labor

Haiku is perfect for extraction, dedupe, and entity identification — these are
pattern-matching tasks that don't need deep reasoning. Opus is needed for grouping
(deciding which claims form a coherent argument) and pyramid building (creating
the hierarchical thesis structure). The cost/speed tradeoff works well.

### 3. Root notes are genuinely good summaries

Both root notes read as honest, structured thesis statements of their respective books.
The Lean Startup root captures all 11 major themes. The Mom Test root captures the
8 key argument clusters. You could read either root and get a real understanding of
the book's argument in one paragraph.

### 4. The YAML frontmatter and tag system works as designed

Every note has proper tags across all dimensions (priority, certainty, stance, domain,
role, source). This means Dataview queries and graph view color groups will work
immediately in Obsidian. The filtering infrastructure is solid.

### 5. Entity extraction identified real concepts

The Mom Test produced 44 entities including technical terms like "The Pathos Problem",
"Zombie leads", "Earlyvangelists", and "Vision-Framing-Weakness-Pedestal-Ask" — all
genuinely important concepts from the book that deserve their own nodes.

---

## What's broken or missing

### 1. CRITICAL: Layer-0 atomic claims are NOT in the vault

This is the biggest failure. The pyramid opus agent was asked to write layer-1 parents
+ layer-2 + root. It did that correctly. But the **original atomic claims (layer 0)
were never written to the vault**.

- Lean Startup: 561 deduped claims exist in `tmp/deduped_claims.md` but 0 are in `vault/`
- Mom Test: 148 deduped claims exist in `tmp2/deduped_claims.md` but 0 are in `vault-mom-test/`

This means **the bottom of the pyramid is invisible**. Layer-1 notes reference
layer-0 children via `[[wikilinks]]`, but those links are all ghosts — there's no
file to click through to. The drill-down experience is broken at the most important
level.

**Impact**: 561 of 698 wikilinks in the Lean Startup vault are unresolved ghosts.
148 of 191 in the Mom Test vault. Most of these are supposed-to-be-real claim links,
not intentional ghost concepts.

**Fix**: Simple — write the deduped claims to the vault alongside the pyramid notes.
One Python call.

### 2. Lateral links were computed but never merged into the vault

Three haiku agents did linking work (tensions, patterns, evidence) and wrote results
to `tmp/results/link_0.md`, `link_1.md`, `link_2.md`. But during final assembly,
I used only the pyramid file + entities. The lateral links were dropped.

**Impact**: No `Tension with`, `Same pattern as`, `Supported by`, or `Challenged by`
bullets appear in any vault note. The cross-cutting connections that make the graph
view interesting are missing.

**Fix**: Merge the link results into the claim notes before writing the vault, or
run linking as a post-processing step on the written vault.

### 3. Entity linking was computed but not merged

The haiku entity-linking agent added `[[wikilinks]]` and `Mentioned:` lines to claims,
writing to `tmp/results/linked_claims.md` and `tmp2/results/linked_claims.md`. But
the final vault was written from the pyramid file (which has no entity links in the
body text of layer-0 claims — because layer-0 claims aren't in the pyramid file at all).

**Impact**: Claim bodies don't contain entity wikilinks. You can't click from a claim
to its referenced entities. The entity nodes exist in the vault but are disconnected
islands.

### 4. Parent/Children backlinks are inconsistent

The grouping agents were supposed to add `Parent: [[X]]` lines to every child and
`Children:` lists to every parent. But the final vault shows only 1 note with a
Parent link in each vault. The pyramid builder seems to have written parent-child
relationships only in the body prose (as inline wikilinks), not as structured
`## Related` sections.

**Impact**: Obsidian's backlinks panel won't reliably show the parent-child hierarchy.
You can navigate down (parent body has [[child]] links) but not up (children don't
have Parent: lines).

### 5. Dedupe was too conservative in some batches, too aggressive in others

- Lean Startup batch 4: 0 merges out of 100 notes (too conservative)
- Mom Test batch 1: 40 merges out of 101 notes (possibly too aggressive)

The dedupe quality depends heavily on which claims end up in which batch. Cross-batch
duplicates are never caught — if the same claim appears in batch 0 and batch 3, both
survive. A second-pass cross-batch dedupe was in the spec but never run.

### 6. No `proposition:` field in most notes

The spec defines `proposition:` as "THE MOST IMPORTANT FIELD" — the canonical semantic
key that makes set operations across vaults possible. The haiku extraction agents
sometimes included it and sometimes didn't, depending on the agent's interpretation.
Without consistent propositions, cross-vault dedup and comparison won't work.

### 7. Existing entity pages are not wikilinked in claim bodies

This is a separate issue from #3. Even in the notes that *are* in the vault (layer-1
parents), entity names appear as plain text when they should be `[[wikilinks]]`.

Measured impact:
- Lean Startup: "Pivot" appears without wikilink in **51 notes**, "Validated Learning"
  in 44, "The Lean Startup" in 42, "Innovation Accounting" in 24, "Five Whys" in 22.
- Mom Test: "Customer conversations" in 11, "Commitment" in 11, "The Mom Test" in 10.

The entity *files* exist. The entity *names* appear in claim text. But they aren't
wrapped in `[[brackets]]`, so they don't become clickable links or graph edges. This
makes the entity nodes appear disconnected in the graph when they should be the most
connected nodes in the vault.

**Fix**: A `fractal reinforce-links` agent that scans every claim body, matches entity
names and aliases against vault files, and wraps unlinked mentions in `[[wikilinks]]`.
This is a mechanical text replacement — haiku can do it in one pass per vault.

### 8. Parsing artifacts create bogus vault files

The note parser splits on `## Title` lines. But the note format also uses `## Related`
as a section header inside notes. The parser treated `## Related` as a note title and
created a `Related.md` file in both vaults — a bogus note with empty YAML and just a
Parent link as body. **Fixed**: deleted from both vaults.

Similarly, some grouping agents appended a `## Child-Parent Assignments` block at the
end of their output — a plain-text list mapping children to parents. This `##` header
was parseable as a note title. It didn't make it into the final vaults (the pyramid
agent didn't include it), but it's a latent bug: if the assembly step had used the
group files directly, `Child-Parent Assignments.md` would have appeared as a weird
note in Obsidian.

**Root cause**: The `## ` record separator conflicts with Markdown's own `## ` heading
syntax inside note bodies. The parser needs to distinguish between `## Title` at the
start of a new note (preceded by blank line or start of file) and `## Related` /
`## Child-Parent Assignments` inside an existing note's body.

**Fix**: Make `parse_notes()` smarter — only split on `## ` lines that are preceded
by `---` YAML closers or start of file, not on arbitrary `## ` lines mid-body.

### 9. No annotation layer

The spec describes an `annotations/` subfolder for user commentary. The code supports
it, but no annotations were generated. This is expected (annotations are user-created),
but the vault would benefit from a few seed annotations showing what they look like.

---

## What the pipeline architecture gets right conceptually but fumbles in execution

### The assembly step is the weak link

Every individual agent did its job well. The extraction agents produced clean YAML.
The grouping agents built coherent clusters. The linking agents found real connections.
The entity agents identified meaningful concepts.

The failure is in **assembly** — the step where I merge all results and write the
vault. I wrote `pyramid_notes + entity_notes` to the vault and called it done. But
the pyramid only contains layers 1-3. The deduped claims (layer 0), the lateral links,
and the entity-linked bodies were all sitting in `tmp/results/` files, never merged.

This is a classic orchestration bug: each worker produces correct output, but the
coordinator drops data when combining results.

### Agent output format wasn't constrained enough

Different agents interpreted "write notes to file" differently:
- Some wrote only the notes
- Some included commentary before/after
- Some used slightly different YAML conventions

A stricter output schema or a post-processing normalization step would help.

---

## Commands/agents that would complete the experience

### 1. `fractal fix-vault` — Assembly repair agent

Read all intermediate results from `tmp/` and properly assemble:
- Layer-0 atoms (from deduped claims)
- Layer-1 parents (from group results)
- Layer-2 clusters + root (from pyramid)
- Lateral links (merge into claim ## Related sections)
- Entity wikilinks (merge into claim bodies)
- Entity notes

This is the most urgent fix — it makes the existing work usable.

### 2. `fractal cross-dedupe` — Cross-batch deduplication

After initial batched dedupe, concatenate all results and run one more dedupe pass
(haiku) to catch duplicates that were split across batches.

### 3. `fractal validate` — Vault integrity checker

Automated checks:
- Every `[[wikilink]]` in a parent's Children list resolves to a real file
- Every child has a `Parent:` backlink
- Every claim has a `proposition:` field
- No duplicate titles
- Tag format consistency
- Layer numbers are coherent (parent.layer == max(children.layer) + 1)

### 4. `fractal refine` — Top-down refinement agent (opus)

The spec's Step 5 (REFINE) was never run. This walks the pyramid top-down and
rewrites parent statements to be more accurate given their children. Currently
parent prose was written at grouping time without seeing the full subtree.

### 5. `distillary promote <ghost>` — Ghost promotion

Already implemented in code but never used. Would let you click a ghost node in the
graph and generate a full entity note from all claims that reference it.

### 6. `fractal distill <vault1> <vault2>` — Cross-vault comparison

The spec's multi-vault distillation. Both books are about customer validation in
startups — a meta-pyramid comparing their approaches would be genuinely interesting.
The Mom Test is essentially the practical implementation guide for what Lean Startup
calls "validated learning."

### 7. Quality scoring agent

An opus agent that samples 20 random claims and scores them on:
- Atomicity (truly one assertion?)
- Proposition accuracy (canonical form?)
- Tag correctness (priority/certainty/stance right?)
- Body clarity (2-4 sentences, self-contained?)

This would calibrate overall vault quality without checking every note.

### 8. `fractal reinforce-links` — Wikilink reinforcement agent (haiku)

**This is the most immediately impactful missing command.** Scan every note in the
vault. For each entity that exists as a file, find every plain-text mention of that
entity (or its aliases) in any claim body and wrap it in `[[wikilinks]]`. Also find
claim titles that appear as plain text in other claims and wikilink them.

This is purely mechanical — no reasoning needed. A haiku agent reads the file list,
builds a lookup of entity names + aliases + claim titles, then does string matching
and replacement across every file. One pass, massive impact on graph connectivity.

The current state: "Pivot" exists as an entity file but appears as plain text in 51
notes. After reinforcement, those 51 notes would each have a clickable `[[Pivot]]`
link and 51 new edges in the graph view.

---

## Deep operations from the spec — not yet implemented as commands

The spec defines 10 families of operations that become possible once vaults exist.
None of these were built yet. Here's what each would look like as a command/agent:

### Family 1: Set operations — `fractal compare <vault1> <vault2>`

Boolean algebra of vaults. Now that we have both Lean Startup and Mom Test:

- **Union**: `fractal union vault/ vault-mom-test/ -o vault-combined/` — everything
  either book says about customer validation. Merge entities, dedupe claims.
- **Intersection**: `fractal intersect vault/ vault-mom-test/` — claims that appear
  in BOTH books. The shared core of customer validation theory.
- **Difference**: `fractal diff vault/ vault-mom-test/` — what Lean Startup says
  that Mom Test doesn't (and vice versa). Reveals each book's unique contribution.

Implementation: opus agent compares proposition fields pairwise. For 561 x 148 pairs,
use haiku for initial similarity screening (tag overlap + keyword match), then opus
for semantic equivalence judgment on the candidates.

### Family 2: Graph operations — `fractal graph-analyze <vault>`

Pure computation on the wikilink network (no LLM needed):

- **Centrality**: Which entities have the highest betweenness? These are the hub
  concepts holding the field together.
- **Bridge nodes**: Entities cited by otherwise-disconnected clusters.
- **Community detection**: Dense clusters that reveal emergent topics.
- **Shortest path**: `fractal path "Pivot" "Five Whys"` — what's the chain of
  reasoning connecting two ideas?

Implementation: Python script using NetworkX. Parse all `[[wikilinks]]` into edges,
run standard graph algorithms, output results as Dataview-queryable metadata.

### Family 3: Temporal operations — `fractal timeline <vault1> <vault2> ...`

Both books have `published:` fields (2011, 2013). With more books:

- **Diff over time**: Same topic, different decade. What changed in startup thinking?
- **Ahead-of-its-time**: Claims marked `speculative` in 2011 that became `established`
  by 2020.
- **Forgotten ideas**: `priority/core` claims in old vaults absent from new ones.

Implementation: Dataview queries filtered by `published:` date. No LLM needed for
basic temporal filtering. Opus agent for narrative synthesis of what changed.

### Family 4: Statistical operations — `fractal profile <vault>`

Tag distribution analysis (no LLM needed):

- **Tag profile**: "Lean Startup is 60% argued, 30% established, 10% speculative.
  Mom Test is 80% argued, 15% established, 5% speculative."
- **Stance entropy**: How much does the author commit vs hedge?
- **Domain breadth**: Specialist vs generalist score.
- **Consensus mining** (multi-vault): Claims marked `priority/core` in 3+ vaults
  that share NO tension links. The field's unquestioned assumptions.

Implementation: Python aggregation over YAML tags. Output as a summary note or
dashboard. Could feed into an opus agent for interpretation.

### Family 5: Structural operations — `fractal compare-structure <v1> <v2>`

Compare HOW authors think, not just WHAT they say:

- **Pyramid alignment**: Do both books decompose "customer validation" the same way?
- **Asymmetry**: Where does one book go deep and the other stays shallow?
- **Compression ratio**: Claims per concept. Mom Test is denser (fewer words, more
  claims per page).

Implementation: Tree comparison algorithms on the pyramid structure. Output as a
visual diff or summary note.

### Family 6: Synthesis operations — `fractal synthesize <topic> <vault1> <vault2>`

LLM-driven combination (opus):

- **Steelman**: Given both vaults' takes on "customer interviews", write a single
  passage that fairly represents both.
- **Mediation**: Where do the books disagree? What's the underlying crux?
- **Reconciliation**: Find a stronger claim both authors would accept.
- **Devil's advocate**: Generate the strongest objection to their shared assumptions.

This is where the substrate pays its biggest dividend — the LLM sees pre-filtered,
pre-structured claims, not raw book text.

### Family 7: Personal operations — `fractal annotate <vault>`

The user becomes another vault:

- **Position calibration**: Where do your `disagree` tags diverge from both books?
- **Reading recommendations**: Based on annotation patterns, suggest next book.
- **Personal bias mirror**: Which claim types do you consistently skip?

Implementation: Annotation notes in `annotations/` subfolder with `status/` and
`insight/` tags. Dataview queries compare user tags against vault distributions.

### Family 8: Generative operations — `fractal essay <question> <vault>`

Using the vault as a citation database (opus):

- **Synthesis essay**: "How should a startup validate customer demand?" — draw from
  both vaults' `priority/key` claims to write a coherent essay with citations.
- **Counterfactual**: "If Fitzpatrick had read Ries first, what would he have added?"
- **Question generation**: From gaps and tensions, generate research questions.

### Family 9: Quality operations — `fractal fact-check <vault1> <vault2>`

Multi-vault redundancy as verification:

- **Majority vote**: If both books say X, it's more credible. If they disagree, flag.
- **Confidence calibration**: A claim marked `established` in one vault but `argued`
  in another should probably be `argued`.
- **Self-contradiction**: Internal tensions that single-vault LINK might miss.

### Family 10: Metalevel operations — `fractal meta-compare`

Compare different processings of the same content:

- **Annotator comparison**: Same book processed by haiku vs opus. Where do they differ?
- **Tag drift**: Across vaults built over time, has `priority/core` drifted?
- **Format integrity**: Check if the algorithm's own substrate is reliable.

Implementation: Run the pipeline twice with different models, diff the results.

---

## Priority ranking for next implementation

If I were to build these as actual commands, the priority order would be:

| Priority | Command | Why | Effort |
|---|---|---|---|
| 1 | `fractal fix-vault` | Assembly bug blocks everything | 30 min |
| 2 | `fractal reinforce-links` | Biggest graph improvement | 20 min |
| 3 | `fractal validate` | Prevents shipping broken vaults | 30 min |
| 4 | `fractal cross-dedupe` | Quality improvement | 20 min |
| 5 | `fractal refine` | Makes parent notes more accurate | 40 min |
| 6 | `fractal compare` (Family 1) | Cross-vault insight — the real payoff | 1 hr |
| 7 | `fractal profile` (Family 4) | Quick statistical view, no LLM | 30 min |
| 8 | `fractal graph-analyze` (Family 2) | Centrality, bridges, paths | 1 hr |
| 9 | `fractal synthesize` (Family 6) | Opus-driven essay generation | 1 hr |
| 10 | `fractal essay` (Family 8) | Citation-backed writing | 1 hr |

Items 1-5 are fixes to the current pipeline. Items 6-10 are the deep operations
that make the format a true knowledge substrate rather than just a summary tool.

---

## Honest overall assessment

**The pipeline design is sound. The execution has a critical assembly bug.**

The good parts are genuinely good: the root notes, the entity extraction, the tag
system, the hierarchical grouping, the speed. An Obsidian user opening either vault
would see a clean graph with colored nodes, functional entity notes, and a readable
thesis at the top.

But the drill-down experience — the whole point of a fractal decomposition — is
broken because layer-0 atoms weren't written to the vault. You can read the root.
You can click into layer-2 clusters. You can click into layer-1 parents. But when
you try to click into the actual atomic claims that hold the evidence, you hit
ghost links. That's the opposite of what the system promises.

The fix is straightforward (write the missing files + merge the link data), but the
fact that it shipped broken reveals that the orchestration layer needs more discipline.
The `fractal validate` agent described above should run automatically before declaring
a vault complete.

**Score: 6/10 as shipped. 8.5/10 with the assembly fix and link merging applied.**

The remaining 1.5 points would come from: consistent proposition fields, cross-batch
dedupe, the refine step, and actual entity wikilinks in claim bodies.
