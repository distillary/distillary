---
title: Quick Start
---

# Quick start

Process your first book into a brain vault in ~15 minutes.

## Prerequisites

- [Claude Code](https://claude.ai/code) — CLI, desktop, or web
- Python 3.11+ with `pip install pyyaml ebooklib beautifulsoup4`
- An EPUB, PDF, or TXT file of the book

## Steps

### 1. Clone the repo

```bash
git clone https://github.com/distillary/distillary.git
cd distillary
pip install pyyaml ebooklib beautifulsoup4
```

### 2. Add your book

Put your book file in `books/`:

```bash
cp ~/Downloads/my-book.epub books/
```

### 3. Open in Claude Code

Open the `distillary/` folder in Claude Code. Say:

> Add books/my-book.epub to my brain. Title: "My Book", Author: "Author Name", Published: 2024

Claude reads the `distillary-add-source` skill and runs the full pipeline:

- 16 parallel haiku agents extract claims (~2 min)
- Haiku agents deduplicate and extract entities (~2 min)
- Opus agents group claims into pyramid (~5 min)
- Haiku agents find connections (~2 min)
- Python assembles the vault (~1 min)
- Doctor fixes issues and writes suggestions

### 4. Open in Obsidian

Open `brain/` as a vault in Obsidian.

1. Enable **Bases** core plugin (Settings → Core plugins → Bases)
2. Enable CSS snippet (Settings → Appearance → CSS snippets → `distillary-tags`)
3. Open `_index.md` — your entry point

### 5. Explore

- Click the root thesis to read the book's argument
- Follow `[[wikilinks]]` to drill deeper
- Check entity pages for concept hubs with backlinks
- Open `.base` files for analytical database views
- Read `_suggestions.md` for ghost concepts to explore

### 6. Add a second book

Say:

> Add books/second-book.epub to my brain

The pipeline runs again. This time, after assembly, Claude also:
- Maps concepts between both books (concept-mapper agent)
- Creates bridge entities in `brain/shared/concepts/`
- Writes a comparison essay in `brain/shared/analytics/`

Your brain now has two sources connected by bridge concepts.

## What's next

- [Add your own annotations](annotating.md)
- [Publish your brain](publishing.md)
- [Understand the architecture](architecture.md)
