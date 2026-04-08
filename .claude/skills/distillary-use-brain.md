---
name: distillary-use-brain
description: Navigate a published Distillary brain to answer questions. Choose the right strategy based on your question type. Triggers on "look up in brain", "check brain", "what does the brain say about", "explore brain", "learn about".
---

# Using a Published Brain

A Distillary brain is a static website with a structured knowledge graph. Different questions need different navigation strategies. Pick the right one.

## Step 0: Always start here

```
WebFetch(url="https://site/brain/agent.json",
         prompt="What sources and bridge concepts are available?")
```

This gives you: source list with theses, bridge concepts with descriptions, and navigation instructions. ~500 tokens. From here, choose your strategy.

## Strategy 1: Walk the pyramid (top-down)

**Use when**: "What does this source argue?", "Summarize the book", "What are the main themes?", "Give me the big picture"

The question is about structure or the overall argument. Walk down the pyramid.

```
agent.json → thesis is already there (0 extra fetches for the summary)
  ↓ need more detail?
root_url → read ~8 cluster links (1 fetch)
  ↓ which cluster matters?
cluster page → read ~5 structure links (1 fetch)
  ↓ need the evidence?
structure page → read ~5 atom links (1 fetch)
```

**Tokens**: 500-2000 depending on depth.
**Best for**: overview questions, "what does X argue about Y", getting oriented.

## Strategy 2: Entity lookup (concept-first)

**Use when**: "What does the brain know about [concept]?", "Define [term]", "How is [idea] used across sources?"

The question is about a specific concept. Jump straight to its entity page.

```
agent.json → find entity name in bridges list or guess the slug
  ↓
entity page → description + backlinks grouped by source (1 fetch)
  ↓ backlinks ARE the answer
follow 2-3 backlinks → read specific claims with evidence (2-3 fetches)
```

**Tokens**: 1500-2500.
**Best for**: concept questions, "what is X", "how is X used", definition lookups.

## Strategy 3: Bridge hop (cross-source)

**Use when**: "Do the sources agree on X?", "How do these books differ on Y?", "What's the relationship between [concept A] and [concept B]?"

The question is about connections between sources. Use bridge concepts.

```
agent.json → find the bridge concept matching the topic
  ↓
bridge page → both perspectives + backlinks from each source (1 fetch)
  ↓ the page already answers "how do they differ"
optionally follow 1-2 backlinks from each source for evidence
```

**Tokens**: 1000-2000.
**Best for**: comparison questions, cross-source synthesis, "do they agree".

## Strategy 4: Backlink chain (discovery)

**Use when**: "What's related to [topic]?", "Explore [area]", "What should I learn about [field]?", "Surprise me"

The question is about exploration, not a specific answer. Follow the link graph.

```
start at any entity or bridge concept
  ↓
read its backlinks → pick the most interesting claim
  ↓
that claim has [[wikilinks]] to other entities → follow one
  ↓
read that entity's backlinks → discover new connections
  ↓
repeat 3-5 times → you've mapped a neighborhood of ideas
```

**Tokens**: 3000-5000 (more fetches, but each is small).
**Best for**: learning, exploration, finding unexpected connections.

## Strategy 5: Comparison essay (pre-built)

**Use when**: "How do all the sources in this brain relate?", "Give me the full cross-source analysis"

Someone already wrote the synthesis. Just fetch it.

```
WebFetch(url="https://site/brain/shared/analytics/comparison",
         prompt="What are the shared ground, tensions, and complementarity?")
```

**Tokens**: ~2000 (one page).
**Best for**: the meta-question, when you want the full picture without exploring yourself.

## Strategy 6: Bulk filter (programmatic)

**Use when**: "List all speculative claims", "How many methodology claims are there?", "What's the tag distribution?"

The question requires filtering across many claims. Use the JSON API.

```
WebFetch(url="https://site/brain/api/sources/{slug}/claims.json",
         prompt="Filter to claims with certainty/speculative")
```

**Tokens**: high (~5000+). Use only when walking pages can't answer the question.
**Best for**: statistical questions, filtering by tags, counting.

## Quick reference: question → strategy

| Question pattern | Strategy | Fetches |
|---|---|---|
| "What does [source] argue?" | Walk pyramid | 1-2 |
| "Summarize [source]" | Walk pyramid | 1 |
| "What is [concept]?" | Entity lookup | 2-3 |
| "How is [concept] used?" | Entity lookup → backlinks | 2-4 |
| "Do sources agree on [topic]?" | Bridge hop | 2 |
| "How do [A] and [B] differ?" | Bridge hop | 2-3 |
| "What's related to [topic]?" | Backlink chain | 3-5 |
| "Explore [field]" | Backlink chain | 4-6 |
| "Full cross-source analysis" | Comparison essay | 1 |
| "List all [tag] claims" | Bulk filter | 1 (heavy) |
| "How many claims about X?" | Bulk filter | 1 (heavy) |

## The key insight

The brain has two navigation structures:

1. **The pyramid** (root → clusters → structure → atoms) — follows the argument hierarchy, good for "what does this source argue about X?"

2. **The link graph** (entities → backlinks → claims → entities) — follows the concept web, good for "what does the brain know about X?"

Both exist in the same vault. The agent chooses which to walk based on the question. Most questions are answered in 2-4 fetches regardless of strategy. The brain has 400+ claims but you never need to see more than 10-15 per question.
