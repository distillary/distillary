Re-extract a source with current agent prompts.

Source to redo: $ARGUMENTS

**Examples:**

```
/dist:redo brain/sources/shafii-resala/
/dist:redo Rich Dad Poor Dad
```

**What happens:**
Read `.claude/skills/distillary-redo.md` FIRST.
1. Confirms before deleting (old claims cannot be recovered)
2. Deletes old claims and entities
3. Keeps chunks (source text preserved)
4. Re-runs the full pipeline with current agent prompts
5. Re-runs concept-mapper if other sources exist

**Print:** before/after claim counts and what changed.
