---
title: Quick Start
---

# Quick start

Process your first source into a brain vault in ~15 minutes.

## Prerequisites

- [Claude Code](https://claude.ai/code) — CLI, desktop, or web
- Python 3.11+ with `pip install pyyaml ebooklib beautifulsoup4 langchain-community`
- An EPUB, PDF, or TXT file

## Steps

### 1. Clone the repo

```bash
git clone https://github.com/distillary/distillary.git
cd distillary
pip install pyyaml ebooklib beautifulsoup4 langchain-community
```

### 2. Add your source

Put your file in `books/`:

```bash
cp ~/Downloads/my-book.epub books/
```

### 3. Open in Claude Code

Open the project folder in Claude Code. Say:

> Add books/my-book.epub to my brain. Title: "My Book", Author: "Author Name", Published: 2024

The pipeline runs:

- Split text into chunks, save permanently if chosen (~30 sec)
- 16 parallel haiku agents extract claims with backing + passages (~2 min)
- Haiku agents deduplicate and extract entities (~2 min)
- Haiku agent adds wikilinks to claim bodies (~1 min)
- Opus agents group claims into pyramid (~5 min)
- Haiku agents find connections (~2 min)
- Optional: verify agent spot-checks claims against source chunks (~1 min)
- Python assembles the vault, fixes links, runs doctor

### 4. Open in Obsidian

Open `brain/` as a vault in Obsidian.

1. Enable **Bases** core plugin (Settings → Core plugins → Bases)
2. Enable CSS snippet (Settings → Appearance → CSS snippets → `distillary-tags`)
3. Open `_index.md` — your entry point

### 5. Explore

- Click the root thesis to read the source's argument
- Follow `[[wikilinks]]` to drill deeper
- Check entity pages — their `Referenced by` sections are your search engine
- Open `.base` files for analytical database views
- Read `_suggestions.md` for ghost concepts to explore
- Check `backing:` fields on claims to see evidence type and strength
- Check `passages:` to read the exact source text in the chunk files

### 6. Add a second source

Say:

> Add books/second-book.epub to my brain

The pipeline runs again. After assembly, Claude also:
- Maps concepts between both sources (concept-mapper agent)
- Creates bridge entities in `brain/shared/concepts/`
- Runs analytics comparing both sources
- Updates the brain index

Your brain now has two sources connected by bridge concepts.

### 7. Ask a question

Say:

> Research: what do both sources say about integrity?

The deep research agent:
- Searches both sources
- Follows backlink chains
- Checks evidence quality (backing type + strength)
- Optionally verifies claims against source chunks
- Writes a structured answer with citations and confidence rating

### 8. Connect more brains

Copy the example config:

```bash
cp brains.example.yaml brains.yaml
```

Edit `brains.yaml` to add local or published brains. The research agent will search across all of them. See [Managing multiple brains](multi-brain.md).

## What's next

- [How it works](how-it-works.md) — the full pipeline and note format
- [Argumentation layer](argumentation-layer.md) — how evidence is captured
- [Deep research agent](deep-research.md) — advanced question-answering
- [Source verification](source-verification.md) — fact-checking claims against source text
- [Publishing](publishing.md) — share your brain as a website
- [Architecture](architecture.md) — agents, skills, utilities
