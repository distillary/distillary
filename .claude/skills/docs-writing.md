---
name: docs-writing
description: Write clear, professional documentation using Quartz components. Guides how to structure pages, when to use diagrams vs text vs callouts, and how to organize doc sites. Triggers on "write docs", "improve docs", "documentation", "write guide", "write page".
---

# Writing Good Documentation

## The principle: text first, components support

Documentation is prose. The reader should understand everything from the text alone. Diagrams, callouts, and tables are supporting evidence — not replacements for explanation.

**Bad**: a Mermaid diagram with no explanation.
**Good**: a paragraph explaining the flow, followed by a diagram that makes it visual.

**Bad**: a callout containing the main explanation.
**Good**: the explanation in regular text, with a callout highlighting one key takeaway.

## Page structure

Every page follows this pattern:

```
# Title

One paragraph explaining what this page covers and why it matters.

---

## Section 1

Explain the concept in 2-3 paragraphs of regular text. Use concrete
examples. Write as if the reader has never seen this before.

After the explanation, optionally add a diagram that visualizes what
you just described:

[mermaid diagram]

> [!tip] Key takeaway
> One sentence summarizing the most important point from this section.

## Section 2

Continue with text-first explanation...
```

## When to use each component

### Regular text (the default)

Use for: everything. All explanations, arguments, steps, and context.

Every section should start and end with regular text. If a section is only a diagram or only a table, add text explaining what the reader is looking at and why it matters.

### Tables

Use for: structured comparisons, reference data, feature lists.

Always introduce a table with a sentence explaining what it shows:

```markdown
The pipeline has 6 steps, each handled by different agent types:

| Step | Agent | Time |
|---|---|---|
| Extract | 16 haiku (parallel) | ~2 min |
| Group | opus | ~5 min |
```

Do NOT use tables for prose. If a cell needs more than 10 words, it should be a paragraph instead.

### Mermaid diagrams

Use for: flows, hierarchies, decision trees, architecture.

Always explain the diagram in text BEFORE showing it. The reader should already understand the concept — the diagram just makes it visual.

```markdown
Sources flow through a pipeline of parallel agents. Text gets split
into chunks, haiku agents extract claims simultaneously, then opus
agents group them into an argumentative hierarchy.

[mermaid diagram here]
```

Do NOT add custom `style` directives to Mermaid — Quartz applies its own theme that works in light and dark mode.

Keep diagrams simple — 5-10 nodes max. If you need more, split into multiple diagrams.

### Callouts

Use for: key takeaways, warnings, tips, and notable asides. A callout is a highlighted paragraph — not a label or a one-word tag.

**Good callout** (substantive, adds value):
```markdown
> [!tip] Start with bridge concepts for the fastest answers
> When an agent needs to answer a cross-source question, fetching a
> bridge concept page gives both perspectives and all backlinks in
> a single request. This is faster than walking the pyramid for
> each source separately.
```

**Bad callout** (too short, adds nothing):
```markdown
> [!tip] This is fast
```

Callout types and when to use them:

| Type | Use when |
|---|---|
| `[!info]` | Providing context the reader needs to understand what follows |
| `[!tip]` | Recommending a best practice or shortcut |
| `[!warning]` | Something that could go wrong if the reader isn't careful |
| `[!example]` | A concrete scenario showing how something works in practice |
| `[!success]` | Confirming a result or outcome the reader should expect |
| `[!abstract]` | Summarizing a key insight or TLDR for a section |
| `[!note]` | Additional context that's useful but not critical |
| `[!quote]` | A direct quote or important statement |

Do NOT use more than 2-3 callouts per page. If everything is highlighted, nothing is.

### Code blocks

Use for: commands, configuration, file contents, API examples.

Always add a sentence before the code explaining what it does:

```markdown
Install the dependencies:

\`\`\`bash
pip install pyyaml ebooklib beautifulsoup4
\`\`\`
```

### Internal links — ALWAYS use wikilinks

**Never use markdown links** `[text](path/file.md)` for internal pages. They break when folders are renamed or reorganized.

**Always use wikilinks:**

```markdown
[[quick-start|Quick start guide]]    — links to quick-start.md wherever it lives
[[tag-taxonomy|Tag taxonomy]]        — Quartz resolves by filename, ignoring folders
[[publishing]]                       — display text defaults to page title
```

Quartz resolves wikilinks by filename across the entire site. No folder paths needed. Backlinks show up automatically.

Use markdown links `[text](url)` only for external URLs.

## Page types and their structure

### Landing page (index)

```
# Project Name

One-sentence tagline.

Two-paragraph explanation of what this does and who it's for.

---

## Key concept 1 (with diagram)

Text explanation → diagram → callout with takeaway

## Key concept 2

Text explanation → table → callout

## Getting started links

Bulleted list of guide links with one-sentence descriptions.

---

> [!note] Acknowledgments
```

### Guide page

```
# How to [do thing]

One paragraph: what you'll learn, prerequisites.

## Step 1: [verb]

Explain what to do and why. Show code if needed.

## Step 2: [verb]

Explain → optionally add diagram → callout with key insight.

## What's next

Links to related guides.
```

### Reference page

```
# [Component] Reference

Brief description of what this is.

## Overview table

| Feature | Description |
|---|---|

## Detailed sections

### Feature A

Text explanation with examples.

### Feature B

Text explanation with examples.
```

## Common mistakes

1. **Markdown links for internal pages** — use `[[page|text]]` wikilinks, never `[text](path.md)`
2. **Diagram without explanation** — always write the text first
3. **Callout as the main content** — callouts highlight, they don't explain
4. **One-word callouts** — write a full paragraph inside callouts
4. **Too many callouts** — max 2-3 per page
5. **Table cells with paragraphs** — use text instead if cells get long
6. **Custom Mermaid colors** — let Quartz handle theming
7. **No introduction** — every page needs a first paragraph explaining what it covers
8. **Links without context** — write "See [Publishing](publishing.md) to deploy your brain" not just "[Publishing](publishing.md)"
