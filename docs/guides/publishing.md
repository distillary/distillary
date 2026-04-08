---
title: Publishing Your Brain
---

# Publishing your brain

Share your brain as a static website with graph view, search, and an agent-queryable API.

## Preview locally

In Claude Code, say:

> Preview my brain

Or manually:

```bash
git clone --depth=1 https://github.com/jackyzha0/quartz.git .brain-site
cd .brain-site && npm i
cp -r ../brain content/ && rm -rf content/.obsidian
npx quartz build --serve
# → http://localhost:8080
```

## Generate agent API

After Quartz builds, generate the JSON manifest so other agents can query your brain:

```python
from distillary.agent_index import generate_agent_index
generate_agent_index("brain", ".brain-site/public")
```

This creates `/agent.json` — a lightweight entry point that tells agents what's inside and how to navigate.

## Deploy to GitHub Pages

```bash
cd .brain-site
npx quartz sync --no-pull
```

Your brain is now live at `https://username.github.io/brain/`.

## What others see

### Humans

A website with:
- Full graph view (colored by source)
- Wikilink navigation (click any `[[concept]]`)
- Backlinks panel on every page
- Full-text search
- Tag pages for filtering

### Agents

A manifest at `/agent.json` with:
- Source list with theses
- Bridge concepts with descriptions and URLs
- Navigation instructions
- Bulk API endpoints (optional, for programmatic filtering)

## Community sharing

1. Tag your repo `distillary-brain` on GitHub
2. Add domain topic tags (`entrepreneurship`, `psychology`, etc.)
3. Post your GitHub Pages URL in the [Discord](https://discord.gg/rGwB4hPMCp)
4. Others can clone your brain into their Obsidian, or query it via agents
