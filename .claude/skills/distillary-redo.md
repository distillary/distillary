---
name: distillary-redo
description: Re-extract a source that had quality issues. Deletes old claims, re-runs the extraction pipeline. Triggers on "redo", "re-extract", "redo extraction", "fix source", "reprocess".
---

# Distillary Redo — Re-extract a source

Re-run the extraction pipeline on an existing source. Use when extraction produced garbage (bad OCR, wrong language, missing claims) or when you want to re-extract with updated agent prompts (e.g., upgrading from v3 to v4).

## How to use

```
User: "redo extraction for brain/sources/shafii-resala/"
```

## Steps

### 1. Confirm with user

Tell the user what will happen:

> **Re-extracting {source title}.** This will:
> - Delete all existing claims (atoms, clusters, structure, root)
> - Delete all entities
> - Keep chunks (if present) — they're the source text
> - Keep `_source.md` — metadata preserved
> - Re-run the full pipeline from extraction
>
> Proceed? (The old claims cannot be recovered.)

### 2. Clean old output

```python
# Delete claims and entities, keep chunks and _source.md
import shutil
from pathlib import Path

source_dir = Path("brain/sources/{slug}")
for subdir in ["claims/atoms", "claims/clusters", "claims/structure", "entities/concepts", "entities/people"]:
    d = source_dir / subdir
    if d.exists():
        shutil.rmtree(d)
        d.mkdir(parents=True)

# Delete root claim
for f in (source_dir / "claims").glob("*.md"):
    f.unlink()

# Keep: chunks/, _source.md, _index.md (will be overwritten)
```

### 3. Re-run pipeline

Read the chunks from `brain/sources/{slug}/chunks/` (or re-extract from the original file if chunks don't exist).

Then run the standard pipeline:
1. Extract claims (from chunks) — use current agent prompt version
2. Dedupe + entities
3. Entity-link → linked_claims.md
4. Group + pyramid (from linked)
5. Source index
6. Post-process (reinforce + hubs + doctor)
7. Re-run concept-mapper if other sources exist

### 4. Report

```
Re-extraction complete for "{source title}".

Before: {old count} claims
After: {new count} claims, {N} entities, {M} clusters

Changes: [what's different — more claims? better backing? new entities?]
Output: brain/sources/{slug}/
```
