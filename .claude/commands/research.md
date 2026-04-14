Deep research a question using the brain.

Read the research agent instructions from `.claude/agents/research.md` FIRST, then follow them precisely.

Question: $ARGUMENTS

**Examples:**

```
/dist:research what is the relationship between fear and wealth?
/dist:research how do the sources disagree about debt?
/dist:research ما العلاقة بين التقوى والنجاح المالي؟
/dist:research what is the strongest evidence for financial literacy?
```

**Behavior:**
- If no brain path in the question, read `brains.yaml` and search all local brains
- For published brains, use WebFetch to query their agent.json
- Write answer to `brain/personal/research/{slugified-question}.md`

**After completion, print:**

```
Research complete.

  Answer: brain/personal/research/{filename}.md
  Confidence: {HIGH/MEDIUM/LOW}
  Claims read: {N}
  Sources: {list}
```
