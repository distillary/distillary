---
title: Command Reference
---

# Command Reference

Everything you can say to Distillary, organized by what you're trying to do.

---

## Adding Sources

### Add a book, article, or document

```
"Add books/my-book.epub to my brain"
"Add books/my-book.pdf to my brain. Title: The Republic, Author: Plato, Published: -380"
"New source from books/research-paper.pdf"
"Process this: books/lecture-notes.txt"
```

The system asks about chunk storage, then runs the full pipeline. Reports progress at every step.

### Add a YouTube video

```
"Add video https://youtube.com/watch?v=..."
```

Downloads transcript, then processes like any other source.

### Add a batch of documents

```
"Add all PDFs in books/contracts/ to a new brain called brain-legal"
```

Processes all files in the directory as separate sources in one brain.

---

## Asking Questions

### Simple research

```
"Research: what does the brain say about integrity?"
"What do my sources say about risk management?"
"ابحث: ما رأي الكتب في التقوى؟"
```

### Deep research with evidence

```
"Investigate: how do the sources disagree about free will?"
"Deep search: what is the strongest evidence for X?"
"Research with quotes: what exactly do the regulations say about encryption?"
```

### Cross-brain research

```
"Research across all brains: what is accountability?"
"Research in brain-legal/: what are the termination clauses?"
```

When no brain is specified, all brains in `brains.yaml` are searched.

---

## Managing Brains

### List connected brains

```
"List brains"
"Show brains"
```

Shows all brains from `brains.yaml` with status and source counts.

### Add a local brain

```
"Add brain at /path/to/brain-philosophy/"
"Connect brain at ../other-project/brain/"
```

### Add a published brain

```
"Add brain at https://someone.github.io/their-brain/"
```

### Clone a published brain for deep analysis

```
"Clone brain from https://someone.github.io/their-brain/"
```

Downloads locally so concept-mapper and analytics can run on it.

### Remove a brain

```
"Remove brain Philosophy"
```

Disconnects from `brains.yaml`. Does not delete files.

---

## Cross-Source Analysis

### Map concepts between sources

```
"Map concepts between the two books"
"Find bridges between all sources"
```

Runs automatically when adding a second source. Can also be triggered manually.

### Map concepts between brains

```
"Map concepts between brain/ and brain-legal/"
```

Finds structural parallels across completely different knowledge domains.

### Run analytics

```
"Run analytics"
"Compare all sources"
"Run analytics across all brains"
```

Generates: statistical profiles, entity overlap, set operations, graph analytics.

---

## Fact-Checking and Verification

### Verify claims against source text

```
"Verify claims in brain/sources/ries-lean-startup/"
"Fact-check the claims from Thinking Fast and Slow"
```

The verify agent reads claims, opens the referenced chunk files, and checks if passages match.

### Research with source quotes

```
"Research with quotes: what exactly does the author say about validation?"
```

The research agent uses Method K — reads chunk files and includes verbatim quotes in the answer.

---

## Fixing and Maintaining

### Run the doctor

```
"Fix my brain"
"Check for issues"
"Run doctor"
```

Finds orphan notes, ghost links, broken hierarchies, missing passages. Writes suggestions.

### Re-extract a source

```
"Redo extraction for brain/sources/ries-lean-startup/"
"Re-extract Thinking Fast and Slow with the updated prompt"
"Reprocess brain/sources/kahneman-thinking/"
```

Deletes old claims, keeps chunks, re-runs the full pipeline with the current agent prompts.

---

## Publishing and Sharing

### Publish your brain

```
"Publish my brain"
"Share my brain"
```

Builds a Quartz static site + generates `agent.json` for other agents to query.

### Preview before publishing

```
"Preview my brain"
```

Starts a local Quartz dev server.

---

## Obsidian Features

### Create analytical database views

```
"Create a base for claims by domain"
"Create base showing entities with most backlinks"
"Obsidian base for evidence strength distribution"
```

Creates `.base` files that Obsidian renders as interactive database views.

### Render diagrams and callouts

```
"Add a Mermaid diagram showing the claim hierarchy"
"Add a callout highlighting this key finding"
```

Uses Quartz-compatible rendering: callouts, Mermaid, wikilinks, code, LaTeX, embeds.

---

## Writing and Annotation

### Add your own notes

```
"Help me annotate this claim"
"I want to write a note about my reaction to the integrity argument"
```

Creates properly formatted notes in `brain/personal/annotations/` linked to specific claims.

### Explore what to read next

```
"What should I explore next?"
"Suggest investigations"
```

The explore agent reads your annotations, ghost links, and bridge gaps to suggest what to investigate.

---

## Presentations and Reports

### Generate from research

```
"Make a presentation about our compliance posture"
"Create slides from the research on innovation methodology"
```

*Note: currently requires iteration. A `distillary-present` skill is planned for one-command output.*

### Convert to PDF

```
"Convert docs/guides/applications.md to PDF"
"Make PDF from the research output"
```

---

## Quick Reference Card

| What you want | What to say |
|---|---|
| Add a source | "Add books/X.epub to my brain" |
| Ask a question | "Research: [question]" |
| Ask with quotes | "Research with quotes: [question]" |
| List brains | "List brains" |
| Add external brain | "Add brain at [path or URL]" |
| Clone published brain | "Clone brain from [URL]" |
| Cross-brain research | "Research across all brains: [question]" |
| Map concepts | "Map concepts between [source A] and [source B]" |
| Run analytics | "Run analytics" |
| Verify claims | "Verify claims in [source path]" |
| Fix issues | "Fix my brain" |
| Re-extract | "Redo extraction for [source path]" |
| Publish | "Publish my brain" |
| Create Obsidian Base | "Create a base for [what]" |
| Annotate | "Help me annotate [claim]" |
| Explore suggestions | "What should I explore next?" |
