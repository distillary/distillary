---
name: distillary-retrieval
description: Retrieve knowledge from any published Distillary brain. Self-contained skill — give this to any agent with web access and a brain URL. No setup needed. Triggers on "query brain", "retrieve from brain", "use fractal brain", "look up in published brain".
---

# Distillary Brain Retrieval

You are querying a Distillary brain — a published knowledge base at a URL. It contains distilled claims from books, videos, articles, organized as a navigable graph. Follow the instructions below to find answers efficiently.

## What you need

- A brain URL (e.g., `https://user.github.io/brain/`)
- A web fetch capability (WebFetch, curl, or any HTTP GET)

## Step 1: Read the manifest

```
GET {brain_url}/agent.json
```

This returns:
- `sources` — what's in the brain (books, videos, etc.) with thesis summaries
- `bridges` — concepts that connect multiple sources, with descriptions
- `how_to_navigate` — instructions for walking the brain

Read it. Then pick your strategy based on your question.

## Step 2: Choose your path

### Your question is about a CONCEPT ("what is X?", "what does the brain know about X?")

Find the matching bridge or entity from agent.json. Fetch its page:

```
GET {brain_url}/shared/concepts/{concept-slug}
```

The page has: description + backlinks grouped by source. Each backlink is a claim about that concept. **The backlinks ARE the answer.** Follow 2-3 for evidence.

### Your question is about a SOURCE ("what does this book argue?", "summarize this")

The thesis is already in agent.json. For more detail, fetch the root note:

```
GET {brain_url}{root_url from agent.json}
```

The root links to ~8 clusters. Each cluster links to ~5 structure notes. Each structure note links to ~5 atomic claims. Walk down by relevance.

### Your question is COMPARATIVE ("do they agree?", "how do sources differ?")

Fetch the comparison:

```
GET {brain_url}/shared/analytics/comparison
```

Or fetch a bridge concept — it shows both sources' perspectives on the same idea.

### Your question is EXPLORATORY ("what's related?", "explore this topic")

Start at any entity page. Read backlinks. Pick an interesting claim. That claim has wikilinks to other entities. Follow one. Read its backlinks. Repeat. Understanding builds through the web of connections.

## How pages work

Every page on a Distillary brain has:

- **Content** — the claim or entity description
- **Wikilinks** — `[[linked concepts]]` in the text, rendered as clickable links
- **Backlinks** — at the bottom, a list of every page that links TO this one

The wikilinks go deeper. The backlinks go wider. Together they form a navigable graph.

## URL patterns

```
/                                    — brain index (start here)
/agent.json                          — manifest for agents
/sources/{slug}/claims/atoms/{name}  — individual claim
/sources/{slug}/claims/structure/{n} — argument parent
/sources/{slug}/claims/clusters/{n}  — chapter-level group
/sources/{slug}/entities/concepts/{n}— entity (concept, person, etc.)
/shared/concepts/{name}              — bridge concept (cross-source)
/shared/analytics/comparison         — cross-source synthesis essay
/shared/analytics/entity-mapping     — which concepts map across sources
```

## Token budget

| Strategy | Fetches | ~Tokens |
|---|---|---|
| Thesis summary | 1 (agent.json) | 500 |
| Concept lookup | 2 (manifest + entity) | 1500 |
| Cross-source comparison | 2 (manifest + bridge) | 2000 |
| Deep evidence chain | 4 (manifest → root → cluster → atom) | 2500 |
| Exploration | 4-6 (follow backlink chains) | 3000-5000 |

Most questions: 2 fetches, under 2000 tokens.

## Example session

**Question: "What do these sources say about validating customer interest?"**

```
1. GET /agent.json
   → See bridge: "Real Signals" (aliases: Actionable Metrics, Commitment)
   → Description: "Reliable evidence of genuine interest"

2. GET /shared/concepts/real-signals
   → Lean Startup: quantitative signals with clear causation
   → Mom Test: qualitative signals where customers put skin in the game
   → 36 LS backlinks + 26 MT backlinks

3. Pick 2 interesting backlinks, GET each one
   → Specific claims with source_ref showing chapter/section

Done. Multi-source answer with citations in 4 fetches.
```

## Share this skill

Copy this entire skill into any agent's system prompt or skill library. The agent only needs:
1. A brain URL
2. HTTP GET capability

No API keys. No authentication. No MCP server. Just URLs and structured markdown pages.
