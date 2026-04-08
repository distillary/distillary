# Distillary

Turn any knowledge source into a navigable brain vault using parallel Claude agents. Books, YouTube videos, podcasts, articles, lectures — anything with ideas gets distilled into the same format. Shared concepts bridge sources. Your annotations are first-class.

#

## Agents

- **annotate** (haiku): Help user write annotations in the brain vault. Creates properly formatted notes in brain/personal/annotations/ with tags linking to specific claims.
- **bridge-builder** (haiku): Create bridge entity notes from concept mapping results. Merges aliases, inherits backlinks, adds cross-references.
- **combine** (haiku): Combine multiple book vaults into one with cross-references. Merges notes, resolves collisions, writes index.
- **compare** (opus): Compare two book vaults and produce a synthesis essay with shared ground, tensions, complementarity, and meta-thesis. Requires deep reasoning across both arguments.
- **concept-mapper** (opus): Find same-concept-different-name pairs across two book vaults. Creates bridge entity notes that unify the graph. Requires deep reasoning about semantic equivalence.
- **dedupe** (haiku): Deduplicate claim notes. Merge notes that say the same thing, keep the strongest formulation.
- **doctor** (haiku): Scan a vault for issues and suggest explorations. Fixes orphans, discovers ghost concepts, flags tensions.
- **entities** (haiku): Extract significant entities (people, concepts, companies, works) from claim notes.
- **entity-link** (haiku): Add [[wikilinks]] to claim bodies for entity references and ghost concepts.
- **explore** (opus): Analyze the brain vault and suggest what to explore next. Reads annotations, suggestions, ghost links, and patterns to recommend investigations. Requires reasoning about intellectual gaps.
- **extract** (haiku): Extract atomic claims from a book chunk. Use this agent to process text chunks into Distillary Note format.
- **group** (opus): Group claims into argumentative clusters and build parent notes. Requires deep reasoning about how claims relate.
- **link** (haiku): Find lateral connections (tensions, patterns, evidence) between notes and add Related bullets.
- **pyramid** (opus): Build the full pyramid from layer-1 parents up to a single root note. Requires deep reasoning about the book's overall argument structure.

## Skills

Skills are in `.claude/skills/` (Claude Code, OpenCode, OpenClaw) or described below for other tools.

For tools that don't support the SKILL.md standard, the key workflows are:

1. **Add a source**: Say "add [path to file] to my brain" — runs extraction, grouping, bridging
2. **Fix issues**: Say "fix my brain" or "check for issues" — runs doctor
3. **Publish**: Say "publish my brain" — builds static site with agent.json API
4. **Query a brain**: Give the agent the distillary-retrieval skill text + a brain URL

## Brain Structure

```
brain/
  sources/{slug}/          Per-source claims + entities
  shared/concepts/          Bridge entities spanning sources
  shared/analytics/         Cross-source comparison
  personal/                 Your annotations
```

## Note Format

Every note has YAML frontmatter with tags across 6 dimensions:
`priority/`, `certainty/`, `stance/`, `domain/`, `role/`, `source/`

Body has `[[wikilinks]]` for navigation and `## Related` sections for hierarchy.

See `.claude/CLAUDE.md` for full documentation.
