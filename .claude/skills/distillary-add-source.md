---
name: distillary-add-source
description: Add any knowledge source (book, video, podcast, article, paper) to the brain vault. Ingests, decomposes, auto-bridges. Triggers on "add book", "add video", "add article", "add podcast", "new source", "process this", "ingest".
---

# Distillary Add Source — Ingest anything into the brain

Add any knowledge source to `brain/sources/{slug}/` and connect it to everything already there.

## Source types and extraction

| Type | Input | Extraction |
|---|---|---|
| Book | EPUB/PDF/TXT | `extract_text("book.epub")` |
| YouTube | URL | `yt-dlp --write-auto-subs` → clean transcript |
| Podcast | Audio file | Whisper transcription |
| Article | URL | WebFetch or `curl` + BeautifulSoup |
| Paper | PDF | `extract_text("paper.pdf")` |
| Lecture | PDF/markdown | `extract_text()` or read directly |

## Pipeline (same for all source types)

### 1. Get text

For books/PDFs:
```python
from distillary.extraction.loader import extract_text, split_text
text = extract_text("path/to/source")
chunks = split_text(text, 20000)
```

For YouTube:
```bash
yt-dlp --write-auto-subs --sub-lang en --skip-download -o "tmp/transcript" "URL"
```

For articles:
Use WebFetch tool or curl + clean HTML.

### 2. Extract claims (parallel haiku agents)

Launch `extract` agents with:
- Source title, author/creator, year
- Source slug (e.g., `ries-lean-startup`, `yc-validate-ideas-2024`)
- Source type for `source_ref` context

### 3. Dedupe + entities (parallel haiku agents)

### 4. Group + pyramid (opus agents)

### 5. Link (haiku agents)

### 6. Assemble into brain

```python
from distillary.vault_ops import fix_vault, reinforce_links, build_entity_hubs
from distillary.doctor import doctor

fix_vault("tmp/{slug}", "brain/sources/{slug}")
reinforce_links("brain")
build_entity_hubs("brain")
doctor("brain")
```

### 7. Write source metadata

Create `brain/sources/{slug}/_source.md`:

```yaml
---
draft: true
title: "Source metadata"
source_title: "Source Title"
author: "Author Name"
type: book | video | podcast | article | paper
published: 2024
url: "https://..."
source_slug: author-short-title
ingested: 2026-04-08
extracted_by: claude-haiku-4.5
---

[One paragraph summary.]
```

### 8. Write source index page

Launch `source-index` agent (haiku) to write a compelling `_index.md`:

```
Agent(subagent_type="source-index", model="haiku",
  prompt="Write an index page for brain/sources/{slug}/. 
  Read _source.md, the root note, and cluster notes.")
```

### 9. Auto-bridge to existing sources

Launch `concept-mapper` (opus) → `bridge-builder` (haiku) to connect new source to existing brain content.

### 10. Update brain index

Launch `brain-index` agent (haiku) to write/update the brain's main `_index.md`:

```
Agent(subagent_type="brain-index", model="haiku",
  prompt="Update brain/_index.md. A new source was added: {title} by {author}.
  Read all source index pages and bridge concepts to write a compelling overview.")
```

## Slug format

| Type | Example |
|---|---|
| Book | `ries-lean-startup` |
| YouTube | `yc-validate-ideas-2024` |
| Podcast | `acquired-nvidia-2024` |
| Article | `paulgraham-do-things-2023` |
| Paper | `vaswani-attention-2017` |

## Incremental growth

Each new source makes every existing source more connected. Source #3 gets bridged to both #1 and #2. Concepts that appear across 3+ sources become the field's consensus — visible as high-centrality bridge nodes in the graph.
