Find and fix brain issues.

Brain to check: $ARGUMENTS

**Examples:**

```
/dist:doctor
/dist:doctor brain-legal/
```

**What it finds:**
Read `.claude/agents/doctor.md` FIRST. Checks for:
- Orphan notes (no parent, no backlinks)
- Ghost links (wikilinks pointing to non-existent notes)
- Claims missing `passages:` field
- Confidence rating inconsistencies
- Broken hierarchy (atoms without parents)

Writes suggestions to `_suggestions.md`.
