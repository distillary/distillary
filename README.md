# Distillary

**Turn any knowledge source into a navigable, shareable brain.**

[Demo Brain](https://brain.distillary.xyz) | [Docs](https://distillary.xyz) | [Discord](https://discord.gg/rGwB4hPMCp)

---

## Quick start

### Try an existing brain (30 seconds)

Browse a published brain right now:

1. Go to the [Demo Brain](https://brain.distillary.xyz)
2. Click any source's root thesis to read the argument
3. Follow `[[wikilinks]]` to drill deeper
4. Check entity pages — their backlinks answer "what does this brain know about X?"

Or query it from your agent — fetch `/agent.json` and follow the navigation instructions.

### Create your own brain (15 minutes)

```bash
curl -fsSL https://raw.githubusercontent.com/distillary/distillary/main/install.sh | bash
cd ~/distillary && claude
```

Then say:

> Add ~/Downloads/my-book.epub to my brain

That's it. Three commands. Claude runs 14 agents in parallel and builds your brain in ~15 minutes. Open `brain/` in [Obsidian](https://obsidian.md) to explore.

### Add a second source

> Add books/another-book.epub to my brain

Claude auto-bridges the new source to everything already in your brain — finds same concepts under different names, writes a comparison essay, creates unified entity pages.

### Publish

> Publish my brain

Your brain becomes a static website with graph view, search, backlinks, and an agent API at `/agent.json`.

---

## What Distillary does

You give it a source (book, video, article). It gives you:

- **A pyramid of claims** — root thesis → chapter clusters → argument groups → atomic evidence, each traceable to a chapter via `source_ref`
- **Entity hubs** — every person, concept, and company gets a page where backlinks from every source show what your brain knows about it
- **Bridge concepts** — when two sources call the same idea by different names, a bridge entity unifies them with both perspectives
- **Your annotations** — your reactions, questions, and insights are part of the graph

All in one `brain/` vault that works in Obsidian and publishes as a website.

---

## How it works

```
Source (book, video, article)
  → 16 parallel haiku agents extract atomic claims (~2 min)
  → Deduplicate + extract entities (~2 min)
  → Opus agents build argumentative pyramid (~5 min)
  → Find tensions, patterns, evidence (~2 min)
  → Doctor fixes issues + suggests explorations (~1 min)
  → Bridge to existing sources in brain
```

14 agents total. Haiku for fast parallel work. Opus for reasoning. Everything defined in `.claude/agents/` and orchestrated by `.claude/skills/`.

---

## For AI agents

Published brains have an `agent.json` manifest. Any agent can query them:

```
GET /agent.json → see sources, bridges, navigation instructions
GET /shared/concepts/real-signals → both perspectives + 62 backlinks
= 2 requests. Multi-source answer with citations.
```

Entity backlinks are the search engine. No MCP server, no auth, no setup. See the [retrieval skill](docs/guides/agent-retrieval.md).

---

## Community

Tag repos `distillary-brain` on GitHub. Join the [Discord](https://discord.gg/rGwB4hPMCp). Share brains, request distillations, compare sources.

---

## Project structure

```
.claude/           14 agents + 10 skills (the brain)
distillary/        Python utilities agents call
brain/             Your knowledge vault (the output)
docs/              Documentation
```

[Full docs →](docs/) | [Architecture →](docs/guides/architecture.md) | [README in docs →](docs/)

---

## License

MIT

---

*Built with Claude agents. Published with [Quartz](https://quartz.jzhao.xyz/). The brains are the value, not the tool.*
