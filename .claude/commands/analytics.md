Run cross-source analytics — statistical profiles, entity overlap, evidence comparison.

What to analyze: $ARGUMENTS

**Examples:**

```
/dist:analytics
/dist:analytics ibn-qayyim vs rich-dad
/dist:analytics all brains
```

**What happens:**
Read `.claude/agents/analytics.md` FIRST. Generates reports in `brain/shared/analytics/`:
- Statistical profiles (claim counts, certainty, backing types per source)
- Entity overlap (shared concepts, hub identification)
- Set operations (unique territory per source)
- Graph analytics (connectivity, centrality)

If two sources specified: focused two-source comparison.
If no argument: all sources in the default brain.
If "all brains": reads `brains.yaml` and compares across brains.
