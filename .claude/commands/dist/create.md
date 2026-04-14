Create a new brain from a directory of files.

What to create: $ARGUMENTS

**Examples:**

```
/dist:create brain from books/contracts/
/dist:create brain-legal from books/regulations/
/dist:create brain-philosophy from books/philosophy/
```

**What happens:**
1. Scan the directory for supported files (.pdf, .epub, .txt, .md)
2. Create brain directory at the specified name (or ask if not given)
3. For each file, run the full add-source pipeline (read `.claude/skills/distillary-add-source.md`)
4. Report progress: "Processing source 3/12: {filename} ({N} claims extracted)..."
5. After all sources, run cross-source analytics and concept-mapper
6. Write brain index
7. Add to `brains.yaml`

**Print completion:**

```
Brain "{name}" created.

  Sources: {N}
  Total claims: {N}
  Bridge concepts: {N}
  Output: {brain-path}/

Added to brains.yaml. Use /dist:research to query it.
```
