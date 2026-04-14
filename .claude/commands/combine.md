Merge two brains or move sources between brains.

What to combine: $ARGUMENTS

**Examples:**

```
/dist:combine brain/ and brain-legal/ into brain-combined/
/dist:combine brain-security/sources/ecc-2024 into brain/
```

Read `.claude/skills/distillary-combine.md` FIRST.

**What happens:**
1. Copy source directories (claims, entities, chunks)
2. Run concept-mapper between combined sources
3. Run bridge-builder for new pairs
4. Regenerate analytics
5. Update brain index and `brains.yaml`

**Print:** what was combined, new source count, new bridge count.
