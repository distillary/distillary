---
name: distillary-decompose
description: Process a book into the brain vault using parallel Claude agents. Triggers on "process book", "decompose book", "fractal decompose", "turn book into vault", "extract claims from book". NOTE - for adding a book to an existing brain, prefer the fractal-add-book skill instead.
---

# Distillary Decompose — Book → Brain Pipeline

Process a book (EPUB/PDF/TXT) into `brain/books/{slug}/` using parallel haiku/opus agents. Output goes into the brain vault, not a standalone vault.

## Step-by-step

### 1. Extract text and split into chunks

```python
from distillary.extraction.loader import extract_text, split_text
import glob

book = glob.glob("books/*.epub")[0]  # or user-provided path
text = extract_text(book)
chunks = split_text(text, 20000)

# Save chunks
for i, chunk in enumerate(chunks):
    with open(f"tmp/chunks/chunk_{i:02d}.txt", "w") as f:
        f.write(chunk)
```

### 2. Extract claims — parallel haiku agents

Launch one `extract` agent per 2 chunks. All run in parallel.

```
Agent(subagent_type="extract", model="haiku", run_in_background=True,
  prompt="Read chunks tmp/chunks/chunk_00.txt and chunk_01.txt from [BOOK TITLE] by [AUTHOR] ([YEAR]).
  Source slug: [slug]. Write notes to tmp/results/extract_00_01.md")
```

Repeat for all chunk pairs. Wait for all to complete.

### 3. Merge + dedupe — parallel haiku agents

```bash
cat tmp/results/extract_*.md > tmp/all_claims.md
```

Split into batches of ~100 notes. Launch `dedupe` agents in parallel:

```
Agent(subagent_type="dedupe", model="haiku", run_in_background=True,
  prompt="Read tmp/dedupe_batch_0.md. Write to tmp/results/dedupe_0.md")
```

### 4. Extract entities — haiku agent

```
Agent(subagent_type="entities", model="haiku", run_in_background=True,
  prompt="Read tmp/all_claims.md. Write to tmp/results/entities.md")
```

Can run in parallel with dedupe.

### 5. Group into pyramid — parallel opus agents

Split deduped claims into batches of ~70. Launch `group` agents:

```
Agent(subagent_type="group", model="opus", run_in_background=True,
  prompt="Read tmp/group_batch_0.md. Write to tmp/results/group_0.md")
```

### 6. Build pyramid to root — opus agent

Extract layer-1 parents from grouped results. Launch `pyramid` agent:

```
Agent(subagent_type="pyramid", model="opus", run_in_background=True,
  prompt="Read tmp/layer1_parents.md. Write to tmp/results/pyramid.md")
```

### 7. Link + entity-link — parallel haiku agents

```
Agent(subagent_type="link", model="haiku", run_in_background=True, ...)
Agent(subagent_type="entity-link", model="haiku", run_in_background=True, ...)
```

### 8. Assemble vault

```python
from distillary.vault_ops import fix_vault, reinforce_links, validate, write_index, build_entity_hubs, restore_bodies
from distillary.doctor import doctor

fix_vault("tmp", "vault-output")
restore_bodies("vault-output", "tmp")
reinforce_links("vault-output")
build_entity_hubs("vault-output")
write_index("vault-output", "Book Title", "Author", 2024)
doctor("vault-output")
validate("vault-output")
```

## Key parameters

- Source slug: lowercase, hyphenated (e.g., `ries-lean-startup`)
- Published year: when the book was published
- Chunk size: 20000 chars
- Batch sizes: ~100 for dedupe, ~70 for grouping
- Always provide book title, author, year to extraction agents

## Performance

- ~15 min for a 500-page book using 16 parallel haiku + 6 opus agents
- ~200-800 claims depending on book density
- ~30-50 entities per book
