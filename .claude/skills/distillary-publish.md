---
name: distillary-publish
description: Publish the brain as a website with agent-friendly API. Triggers on "publish brain", "publish vault", "share brain", "deploy", "make website", "preview".
---

# Distillary Publish — Share your brain

## Preview locally

```python
from distillary.publish import preview
preview("brain/")
# → http://localhost:8080 with graph view, search, backlinks
```

Or manually:
```bash
# Clone Quartz + apply Distillary branding
git clone --depth=1 https://github.com/jackyzha0/quartz.git .brain-site
cd .brain-site && npm i
cp ../quartz-config/quartz.config.ts .
cp ../quartz-config/quartz.layout.ts .
cp ../quartz-config/Footer.tsx quartz/components/Footer.tsx

# Copy brain + build
cp -r ../brain content/ && rm -rf content/.obsidian
npx quartz build --serve
```

## Generate agent-friendly API

After Quartz builds, generate JSON indexes so other agents can query the brain:

```python
from distillary.agent_index import generate_agent_index
generate_agent_index("brain", ".brain-site/public")
```

This creates:
- `/agent.json` — manifest (like `--help` for agents)
- `/api/sources/{slug}/claims.json` — all claims, filterable
- `/api/sources/{slug}/claims/core.json` — core claims only (TL;DR)
- `/api/sources/{slug}/entities.json` — all entities
- `/api/shared/bridge-concepts.json` — cross-source bridges
- `/api/graph.json` — full link graph

## Deploy to GitHub Pages

```bash
cd .brain-site
npx quartz sync --no-pull
# → live at https://username.github.io/brain/
```

Or use `distillary publish brain/` which does all of the above.

## How other agents use your published brain

They fetch `/agent.json` to discover what's available, then query specific JSON endpoints. No MCP server, no auth. See the `distillary-use-brain` skill for details.

```
Agent fetches: https://you.github.io/brain/agent.json
  → sees 2 sources, 420 claims, 152 entities
Agent fetches: https://you.github.io/brain/api/sources/ries-lean-startup/claims/core.json
  → gets the 118 core claims from The Lean Startup
```

## Prepare for git sharing

```python
from distillary.sharing import init_vault
init_vault("brain/", title="My Knowledge Brain", author="Your Name")
# Creates README.md + .gitignore
```

Convention: repos tagged `distillary-brain` on GitHub. Topic tags for domains.
