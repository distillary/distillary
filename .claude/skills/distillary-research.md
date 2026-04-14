---
name: distillary-research
description: Deep research a question using the brain. Iteratively searches claims, follows links, checks evidence, cross-references sources. Triggers on "research", "deep search", "investigate", "what does the brain say about", "ابحث", "ما رأي".
---

# Distillary Research — Deep question answering from the brain

Answer any question by iteratively searching the brain vault until confident.

## How to use

Launch the `research` agent (opus) with:
- The question
- The brain path (`brain/`)
- An output file for the answer

```
Agent(subagent_type="research", model="opus",
  prompt="Question: {user's question}
  Brain path: /path/to/brain/
  Write your answer to: brain/personal/research/{slugified-question}.md")
```

## What it does

The agent works in passes:
1. **Scope** — breaks the question into sub-questions
2. **Search** — finds relevant claims using key terms
3. **Evaluate** — checks backing quality (evidence type + strength + warrant)
4. **Deepen** — follows wikilinks to related claims, checks other sources
5. **Cross-reference** — compares across sources, identifies agreement/conflict
6. **Report** — structured answer with evidence citations, confidence level, and gaps

## Output format

The answer goes to `brain/personal/research/` with:
- Direct answer
- Evidence citations with backing details
- Cross-source agreement/conflict
- Confidence level (HIGH/MEDIUM/LOW)
- Gaps — what the brain doesn't know

## After completion

**Always tell the user:**

```
Research complete.

Answer written to: brain/personal/research/{filename}.md
Confidence: {HIGH/MEDIUM/LOW}
Claims read: {N}
Sources consulted: {list}

Open the file to read the full answer with evidence citations.
```

## When to use

- Complex questions that span multiple sources
- Questions where evidence quality matters ("what's the daleel?")
- Questions where sources might disagree
- Any question where a simple search isn't enough
