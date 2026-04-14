Fact-check claims against source text.

What to verify: $ARGUMENTS

**Examples:**

```
/dist:verify brain/sources/kiyosaki-rich-dad/
/dist:verify all
/dist:verify "Debt is enslavement"
```

**What happens:**
Read `.claude/agents/verify.md` FIRST. For each claim with a `passages:` field:
1. Open the referenced chunk file
2. Find the passage at the referenced lines
3. Check: does the passage support the proposition?

**Print:**

```
Verification report:

  Verified: {N} ({%})
  Partially verified: {N} ({%})
  Unverified: {N} ({%})
  Missing passages: {N}
```
