---
title: Deep Research Agent — Answering Hard Questions from the Brain
---

# Deep Research Agent

The research agent answers questions by iteratively searching the brain — going back and forth, following links, checking evidence, cross-referencing sources — until it finds a comprehensive, well-evidenced answer.

## When to Use

- Complex questions that span multiple sources
- Questions where evidence quality matters ("what's the daleel?")
- Questions where sources might disagree
- Questions that require synthesis (combining insights no single source states)
- Any question where a simple Grep search isn't enough

## How It Works

The agent works in passes. Each pass deepens understanding. It doesn't stop after one search.

```
Question
  │
  ├── Pass 1: Scope → break into sub-questions, pick strategies
  ├── Pass 2: Search → Grep key terms, read claims, check backings
  ├── Pass 3: Backlinks → entity pages → Referenced by → follow chains
  ├── Pass 4: Pyramid → walk root → structure → cluster → atom for context
  ├── Pass 5: Cross-source → bridges, analytics, compare evidence types
  ├── Pass 6: Advanced methods → if still not confident
  ├── Pass 7: Evaluate → rank evidence, assess confidence
  └── Pass 8+: Iterate → until confident or brain exhausted
```

## 6 Core Strategies

The agent picks strategies based on question type. For complex questions, it combines multiple.

### Strategy 1 — Concept Lookup

**For:** "What is X?", "What does the brain know about X?"

Find entity page for X → read its `## Referenced by` section. Each backlink is a claim about X from every source. The backlinks ARE the answer.

```
Entity: القياس
  └── Referenced by:
      ├── Validated learning measures real progress (ries-lean-startup)
      ├── Cohort analysis reveals true retention (ries-lean-startup)
      └── ...
```

### Strategy 2 — Pyramid Walk

**For:** "What does source Y argue about Z?"

Walk top-down through one source's hierarchy:

```
Root (layer 3): "الرسالة أول تأسيس منهجي لعلم أصول الفقه"
  └── Structure (layer 2): "البناء النظري لأصول الفقه ومصادر التشريع"
      └── Cluster (layer 1): "القياس أصل من أصول الاستدلال الشرعي"
          └── Atom (layer 0): specific claim with backing + warrant
```

Each level adds context. The root tells you the thesis. The atom tells you the specific evidence.

### Strategy 3 — Evidence Chain

**For:** "Prove it", "What's the daleel?", "ما الدليل؟"

Read atom claims → check their `backing:` fields:

```yaml
backing:
  - category: textual/ayah — "ومن يشاقق الرسول..." (definitive)
    warrant: "الآية تحذر من مخالفة سبيل المؤمنين"
  - category: transmitted/hadith — "لا تجتمع أمتي..." (strong)
    warrant: "عصمة الأمة تثبت حجية إجماعها"
```

Follow `depends_on` for chained evidence (hadith that specifies a general ayah).

### Strategy 4 — Cross-Source Comparison

**For:** "Do they agree?", "How do sources differ?"

Read bridge concepts in `shared/concepts/` — they show how different sources approach the same idea. Their `Referenced by` sections span ALL sources.

### Strategy 5 — Backlink Chain Exploration

**For:** "What's related?", "Explore this topic"

Navigate the graph through backlinks:

```
entity → backlinks → claims → wikilinks → more entities → more backlinks
```

Each hop reveals more context. The agent does at least 3 hops.

### Strategy 6 — Gap Detection

**For:** "What's missing?", "What don't we know?"

Grep key terms across all sources. Few results = brain has a gap. Check `shared/analytics/set-operations.md` for what each source uniquely covers.

## 10 Advanced Discovery Methods

When core strategies don't yield a full answer, the agent uses advanced methods. **These are what make it handle hard questions.**

### Method A — Inverse Search

Can't find what X IS? Search for what X is NOT. Claims that contrast with X, oppose X, or target X as a rebuttal reveal X's boundaries through negative space.

**Example:** Can't find "what is justice?" → search claims about injustice, oppression, corrupt judges → infer the positive definition from what the brain opposes.

### Method B — Warrant Mining

Search `warrant:` fields across unrelated claims. If the same reasoning pattern appears in multiple places, you've found a hidden meta-principle the brain holds but never states explicitly.

**Example:** The agent discovered "measure what matters, not what's easy" — a principle that appears across multiple sources' warrants. Source A argues for validated learning over vanity metrics. Source B argues for real customer commitment over compliments. No single source states the meta-principle, but all build on it.

### Method C — Evidence Archaeology

Trace a single piece of evidence (a hadith, a verse) across every claim that cites it. Different authors use the same evidence for different conclusions. The divergence reveals what each source values.

### Method D — Cluster Intersection

Find claims at the intersection of two thematic clusters. These bridge themes and often contain the most nuanced arguments.

**Example:** Source A's "customer validation" cluster intersects Source B's "cognitive bias" cluster at the concept of confirmation bias. Entrepreneurs need to avoid it when testing hypotheses; psychologists study it as a universal judgment error. Same mechanism, different domains.

### Method E — Analogical Transfer

If Source A answers a similar question in Domain A, the bridge concept between A and B may carry the answer across domains.

**Example:** Source A's principle of "failing fast" transfers to Source B's domain of investment — the investor needs the boldness to make bets with the discipline to cut losses early. A bridge concept carries the principle across domains.

### Method F — Strength Aggregation

One weak piece of evidence + another moderate + a third strong = collectively stronger than any alone. The agent maps all evidence into a table and reads the aggregate pattern.

### Method G — Rebuttal Reconstruction

Search for `role/rebuttal` claims. The objections an author anticipated reveal edge cases, boundary conditions, and what they considered and rejected. The rejected alternatives are part of the answer.

### Method H — Hierarchical Layering

Read ALL layers (0-3) for the same topic. The root says one thing abstractly; the atom says it concretely with evidence. The gap between them reveals the reasoning chain.

**Example:** At root level, Source A says "build-measure-learn is the engine of startups." At atom level, it says "run the cheapest experiment that tests your riskiest assumption." The root gives you the principle; the atom gives you the specific action. Reading both layers reveals the reasoning chain from philosophy to practice.

### Method I — Entity Co-occurrence

If two entities frequently appear in the same claims (overlapping backlink lists), they're deeply connected even without a bridge concept. The overlapping claims ARE the implicit bridge.

### Method J — Source Signature Analysis

Each source has a characteristic argumentation style (check `shared/analytics/statistical-profiles.md`). A source that argues through empirical evidence gives a different kind of answer than one arguing through rational methods. The signature tells you how much to trust its claims on a given topic.

### Method K — Source Passage Verification

When citing a claim as evidence, check its `passages:` field. Read the referenced chunk file at the specified lines. Confirm the passage actually supports the claim. If the passage is weaker than the claim suggests, downgrade confidence. This prevents building answers on poorly extracted claims.

## Output Format

The research agent writes a structured answer:

```
## Question
## Sub-questions (each marked answered/unanswered)
## Answer (standalone 5-15 sentence paragraph)
## Evidence (each point with claim, backing, warrant, context)
## Cross-source analysis (agreement/conflict)
## Evidence quality assessment (table)
## Confidence: HIGH / MEDIUM / LOW (with reasoning)
## Gaps (what's missing, what source would fill it)
## Advanced discoveries (insights from Methods A-J)
## Research path (strategies used, hops followed, dead ends hit)
```

## Minimum Requirements

Before writing an answer, the agent must:
- Read at least 15 claims
- Follow at least 3 backlink chains
- Walk at least 1 pyramid (root → atom)
- Check at least 2 sources
- Use at least 1 advanced method for MEDIUM/LOW confidence questions

## Real Test Results

**Question tested:** "كيف يتعامل المسلم مع الشك في صحة اجتهاده؟ وهل يأثم المجتهد إذا أخطأ؟ وما العلاقة بين الاجتهاد الفقهي وصلاح القلب؟"

**Results:**
- 37 units read (22 atoms + 4 clusters + 3 structures + 2 roots + 6 bridges)
- 4 backlink chains followed
- 2 full pyramids walked
- 3 sources cross-referenced
- 4 advanced methods used (warrant mining, cluster intersection, analogical transfer, hierarchical layering)
- Confidence: HIGH
- Key discovery: hidden meta-principle "الحالة الداخلية تحدد النتيجة الخارجية" found through warrant mining — not stated by any single source but emergent from cross-source analysis

## How to Invoke

```
Agent(model="opus",
  prompt="Read the research agent instructions from .claude/agents/research.md first.
  Question: {your question}
  Brain path: brain/
  Write answer to: brain/personal/research/{slug}.md")
```

Or say: "research", "investigate", "ابحث", "ما رأي الدماغ في..."
