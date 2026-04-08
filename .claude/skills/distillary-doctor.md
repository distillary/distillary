---
name: distillary-doctor
description: Fix vault issues and suggest explorations. Triggers on "fix vault", "doctor vault", "check vault", "find issues", "suggest explorations", "find ghosts".
---

# Distillary Doctor — Fix + Discover

Run the doctor on a vault to fix mechanical issues and generate suggestions.

## Usage

```python
from distillary.doctor import doctor
stats = doctor("vault-path/")
# Writes _suggestions.md to the vault
```

Or in Claude Code, say:

> Fix my brain / Check my brain for issues

## What it fixes (mechanical, no LLM)

- **Orphan atoms**: finds claims with no parent, assigns to nearest L1 parent by domain tag match
- **Missing propositions**: generates proposition from note title for claims that lack one
- **Ghost notes**: creates stub entity notes for concepts mentioned in 3+ claims

## What it discovers (analytical)

- **Frontier concepts**: wikilink targets that appear in 3+ claims but have no file
- **Over-extracted entities**: entity notes referenced by 0-1 claims (too specific)
- **Remaining orphans**: atoms that couldn't be auto-assigned

## Output

Writes `_suggestions.md` with:
- Ghost concepts to explore (with mention counts)
- Discovered phrases that could become entities
- Orphan notes needing attention
- Auto-fixed assignments
- Over-extracted entities to consider removing

## Follow-up actions

After reviewing `_suggestions.md`:
- **Promote a ghost**: `distillary promote "concept name" vault/`
- **Remove over-extracted entity**: delete the .md file
- **Add annotations**: create notes in `annotations/` subfolder
