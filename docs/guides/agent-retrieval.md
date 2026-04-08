---
title: Agent Retrieval Skill
---

# Agent retrieval skill

A self-contained skill for querying any published Distillary brain. Copy this into any agent's context — it only needs a brain URL and HTTP GET.

## The skill

Copy the contents of [`.claude/skills/distillary-retrieval.md`](../../.claude/skills/distillary-retrieval.md) into your agent's system prompt or skill library.

## How it works

1. Agent fetches `{brain_url}/agent.json` — lightweight manifest with sources, bridges, and navigation instructions
2. Based on the question type, the agent picks a strategy:
   - **Concept lookup** → fetch a bridge entity page → backlinks ARE the answer
   - **Source summary** → thesis is already in the manifest
   - **Comparison** → fetch the comparison essay or a bridge page
   - **Deep evidence** → walk the pyramid: root → cluster → structure → atom
   - **Exploration** → follow backlink chains through the concept graph
3. Each fetch returns one page with content + links to go deeper
4. Most questions answered in 2-4 fetches, under 2500 tokens

## Example

Agent receives question: "What does this brain say about validating demand?"

```
GET /agent.json
→ Bridge: "Demand Test" — testing whether customers want what you're building

GET /shared/concepts/demand-test
→ Lean Startup: ship an MVP and measure real behavior
→ Mom Test: check for commitment that costs something (time, money, reputation)
→ Both agree: compliments don't count as validation
```

Done. 2 fetches. Multi-source answer.

## Integration

Works with any agent that can make HTTP requests:
- Claude Code (WebFetch tool)
- ChatGPT (web browsing)
- Custom agents (curl/fetch)

No API keys. No authentication. No MCP server. Just URLs and structured markdown pages.
