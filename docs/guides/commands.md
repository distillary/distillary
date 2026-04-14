---
title: Command Reference
---

# Command Reference

All commands use `/dist:command-name`. Each reads its agent definition file — consistent behavior every time.

---

## Adding Content

| Command | What it does |
|---|---|
| `/dist:add` | Add a book, PDF, article, video, or URL to the brain |
| `/dist:create` | Create a new brain from a directory of files |

```
/dist:add books/rich-dad-poor-dad.pdf
/dist:add books/my-book.epub
/dist:add https://youtube.com/watch?v=abc123
/dist:add https://paulgraham.com/ds.html

/dist:create brain-legal from books/contracts/
/dist:create brain-philosophy from books/philosophy/
```

The `add` command auto-detects the type: file path → extract text, YouTube URL → download transcript, web URL → fetch article. Reports progress at every step.

---

## Asking Questions

| Command | What it does |
|---|---|
| `/dist:research` | Deep research with evidence grading (~3-5 min) |
| `/dist:lookup` | Quick entity lookup via backlinks (~30 sec) |

```
/dist:research what is the relationship between fear and wealth?
/dist:research ما العلاقة بين التقوى والنجاح المالي؟
/dist:research how do the sources disagree about debt?

/dist:lookup integrity
/dist:lookup القياس
/dist:lookup Passive Income
```

`research` searches all brains, follows backlink chains, grades evidence, writes a full answer to file. `lookup` is the fast path — finds the entity, reads backlinks, prints a summary.

---

## Analysis

| Command | What it does |
|---|---|
| `/dist:map-concepts` | Find same-concept pairs, create bridge notes |
| `/dist:compare` | Write synthesis essay (agreement, tensions, meta-thesis) |
| `/dist:analytics` | Statistical profiles, entity overlap, graph metrics |

```
/dist:map-concepts ibn-qayyim and rich-dad
/dist:map-concepts brain/ and brain-legal/

/dist:compare barnum and kiyosaki
/dist:compare brain/ and brain-security/

/dist:analytics
/dist:analytics ibn-qayyim vs rich-dad
/dist:analytics all brains
```

---

## Quality

| Command | What it does |
|---|---|
| `/dist:verify` | Fact-check claims against source chunks |
| `/dist:doctor` | Find orphans, ghost links, missing passages |
| `/dist:redo` | Re-extract a source with current prompts |

```
/dist:verify brain/sources/kiyosaki-rich-dad/
/dist:verify all

/dist:doctor
/dist:doctor brain-legal/

/dist:redo brain/sources/shafii-resala/
/dist:redo Rich Dad Poor Dad
```

---

## Brain Management

| Command | What it does |
|---|---|
| `/dist:brains` | List, add, clone, or remove connected brains |
| `/dist:sources` | List all sources with stats table |
| `/dist:status` | Quick health overview (~10 sec) |
| `/dist:combine` | Merge two brains or move sources |

```
/dist:brains list
/dist:brains add /path/to/brain-philosophy/
/dist:brains add https://someone.github.io/their-brain/
/dist:brains clone https://someone.github.io/their-brain/
/dist:brains remove Philosophy

/dist:sources
/dist:sources brain-legal/

/dist:status

/dist:combine brain/ and brain-legal/ into brain-combined/
```

---

## Personal

| Command | What it does |
|---|---|
| `/dist:explore` | Suggest what to investigate next |
| `/dist:annotate` | Write a personal reaction to a claim |

```
/dist:explore
/dist:explore financial literacy

/dist:annotate the integrity argument
/dist:annotate I disagree with Rich Dad's view on debt
```

---

## Output

| Command | What it does |
|---|---|
| `/dist:base` | Create Obsidian analytical database view |
| `/dist:publish` | Deploy brain to web with agent.json |

```
/dist:base claims by domain
/dist:base entities with most backlinks
/dist:base evidence strength distribution

/dist:publish
/dist:publish preview
```

---

## Quick Reference

| What you want | Command |
|---|---|
| Add a book/PDF | `/dist:add books/X.pdf` |
| Add a video | `/dist:add https://youtube.com/...` |
| Add an article | `/dist:add https://example.com/article` |
| Create new brain | `/dist:create brain-name from books/dir/` |
| Deep research | `/dist:research [question]` |
| Quick lookup | `/dist:lookup [concept]` |
| Map concepts | `/dist:map-concepts [A] and [B]` |
| Compare sources | `/dist:compare [A] and [B]` |
| Run analytics | `/dist:analytics` |
| Fact-check | `/dist:verify [source]` |
| Fix issues | `/dist:doctor` |
| Re-extract | `/dist:redo [source]` |
| List brains | `/dist:brains list` |
| Add external brain | `/dist:brains add [path or URL]` |
| Clone brain | `/dist:brains clone [URL]` |
| List sources | `/dist:sources` |
| Brain status | `/dist:status` |
| Merge brains | `/dist:combine [A] and [B]` |
| Get suggestions | `/dist:explore` |
| Write annotation | `/dist:annotate [topic]` |
| Create Base view | `/dist:base [what]` |
| Publish | `/dist:publish` |
