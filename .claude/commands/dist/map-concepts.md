Map concepts between two sources or two brains. Creates bridge entity notes.

What to map: $ARGUMENTS

**Examples:**

```
/dist:map-concepts ibn-qayyim and rich-dad
/dist:map-concepts all sources
/dist:map-concepts brain/ and brain-legal/
```

**What happens:**
1. Read `.claude/agents/concept-mapper.md` — run concept-mapper to find pairs
2. Read `.claude/agents/bridge-builder.md` — create bridge notes for top 10 pairs
3. Update original entity files with cross-references

**Print:**

```
Mapping complete.

  Same concept: {N} pairs
  Complementary: {N} pairs
  Opposing: {N} pairs
  Bridge notes created: {N}
  Output: brain/shared/concepts/
```
