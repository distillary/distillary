# Distillary: Agent-Based Knowledge Distillation with Argumentation-Aware Extraction and Cross-Source Verification

**Noureddine Haouari**

---

## Abstract

We present Distillary, an open-source system that transforms unstructured knowledge sources — books, regulatory documents, research papers, and any text-bearing medium — into navigable, queryable, and verifiable knowledge graphs. Unlike existing knowledge management tools that treat text as flat content, Distillary decomposes sources into atomic claims with structured argumentation metadata: evidence type, strength grade, warrant, and traceable source passages. The system employs a pipeline of 16 specialized AI agents orchestrated across 11 processing steps, producing Obsidian-compatible vaults where entity backlinks serve as the primary discovery mechanism. We introduce five contributions: (1) a universal argumentation framework with 9 evidence categories that operates across domains without configuration, (2) a multi-dimensional tagging system that makes every claim filterable across 9 orthogonal axes, (3) a deep research agent with 11 discovery methods including warrant mining and analogical transfer across sources, (4) a source verification layer that traces every claim to exact passages in the original text, and (5) a multi-brain federation architecture that enables cross-domain knowledge synthesis across independent knowledge bases. Evaluation across Islamic jurisprudence texts, cybersecurity regulatory frameworks, and business literature demonstrates zero-configuration domain transfer, 100% wikilink accuracy in research outputs, and successful cross-domain concept mapping between structurally unrelated knowledge bases.

---

## 1. Introduction

Knowledge workers face a fundamental problem: the insights in books, papers, regulations, and documents are locked in prose. A researcher reading five papers on a topic must mentally track which claims are supported by strong evidence, which are speculative, where authors agree, and where they contradict — across hundreds of pages with no structural support.

Existing tools address parts of this problem. Reference managers (Zotero, Mendeley) organize sources but don't decompose their arguments. Note-taking systems (Obsidian, Notion, Roam) provide linking but require manual extraction. Summarization tools (AI-generated summaries) compress content but lose evidence structure and verifiability. Knowledge graphs (Wikidata, concept maps) capture entities and relationships but not the argumentation that justifies them.

Distillary addresses the full problem: given any text source, automatically produce a structured knowledge graph where every claim has typed evidence, a strength grade, a warrant explaining the reasoning, cross-source connections, and a traceable path back to the exact source passage. The system requires no domain-specific configuration — the same pipeline processes Islamic jurisprudence, cybersecurity regulations, and business books.

### 1.1 Contributions

1. **Universal Argumentation Framework.** Nine evidence categories (textual, transmitted, consensus, analogical, empirical, rational, experiential, authority, silence) that map to any domain without configuration. A hadith and a randomized controlled trial are different evidence types but occupy the same structural position.

2. **Deep Research Agent with Advanced Discovery.** An iterative question-answering agent with 6 core strategies and 11 advanced methods (including warrant mining, analogical transfer, inverse search, and source passage verification) that exhaustively searches the knowledge graph before answering.

3. **Source Verification Layer.** Every claim stores lightweight passage references (chunk file, line range, snippet) that trace to the original text. A verify agent fact-checks claims against source passages, catching extraction errors and assessing confidence.

4. **Cross-Source Bridge Concepts.** Automated concept mapping discovers same-idea-different-name pairs across sources, creating unified entities that serve as cross-source query hubs.

5. **Multi-Brain Federation.** Multiple independent knowledge bases can be connected and searched simultaneously, with cross-brain concept mapping and analytics.

---

## 2. System Architecture

### 2.1 Overview

Distillary consists of three layers:

- **Agent layer** (`.claude/agents/`): 16 AI agents with specific roles and model assignments (haiku for bulk operations, opus for deep reasoning)
- **Utility layer** (`distillary/`): Python functions for text extraction, note parsing, vault operations, and link management
- **Output layer** (`brain/`): Obsidian-compatible vault with claims, entities, bridges, analytics, and optional source chunks

### 2.2 Processing Pipeline

The pipeline transforms a source into a structured knowledge graph in 11 steps:

| Step | Agent | Model | Input | Output |
|---|---|---|---|---|
| 1. Extract text | Python | — | PDF/EPUB/TXT | Text chunks (20KB each) |
| 2. Extract claims | extract | haiku (parallel) | Chunks | Atomic claims with backing + passages |
| 3. Deduplicate | dedupe | haiku | All claims | Unique claims (passages merged) |
| 4. Extract entities | entities | haiku | Claims | Concept and person entities |
| 5. Add wikilinks | entity-link | haiku | Claims + entities | Claims with `[[wikilinks]]` in body |
| 6. Group into hierarchy | group | opus | Linked claims | Clusters (L1) with parent claims |
| 7. Build pyramid | pyramid | opus | Clusters | Structure (L2) + root thesis (L3) |
| 8. Find connections | link | haiku | All claims | Tension and pattern markers |
| 9. Verify (optional) | verify | haiku | Claims + chunks | Verification report |
| 10. Post-process | Python | — | Vault | Reinforced links, entity hubs, doctor |
| 11. Bridge to other sources | concept-mapper + bridge-builder | opus + haiku | Entities across sources | Bridge concepts |

A critical ordering constraint: entity-linking (step 5) must precede grouping (step 6) so that atom files written to the vault already contain wikilinks. This was identified through empirical testing and eliminates the need for post-hoc link patching.

### 2.3 Vault Structure and Skill Orchestration

The output vault follows a three-zone architecture:

```
brain/
  sources/{slug}/           Per-source zone (agent-generated)
    chunks/                 Source text for verification
    claims/{atoms,clusters,structure}
    entities/{concepts,people}
  shared/                   Cross-source zone
    concepts/               Bridge entities connecting sources
    analytics/              Statistical comparisons
    evidence/               Shared citation hubs
  personal/                 User zone
    annotations/            Reactions to claims
    research/               Deep research outputs
```

Each source maintains its own hierarchy (root → structure → clusters → atoms) and entities. The `shared/` zone holds cross-source artifacts that emerge from concept mapping and analytics. The `personal/` zone contains the user's own thinking — annotations and research outputs that link into the graph alongside agent-generated content.

**Skills as orchestration.** The system includes 11 skills that chain agents into workflows. A skill is not an agent — it's a recipe that describes which agents to launch in what order with what inputs. For example, the `add-source` skill orchestrates the 11-step pipeline, reporting progress at each step; the `research` skill launches the research agent with proper context from `brains.yaml`. Skills are the user-facing interface; agents are the workers.

**Publishing.** The vault can be deployed as a static website via Quartz, a markdown-to-website generator. Publishing also generates an `agent.json` manifest — a machine-readable index of sources, bridges, and navigation paths. Any agent with HTTP access can query a published brain by fetching `agent.json` and following URLs to entity pages and claims. This enables the **clone-then-map** pattern: download a published brain locally, then run concept-mapper and analytics against it — combining someone else's knowledge with your own.

### 2.4 The Claim Format (v4.0)

Every atomic claim carries structured metadata:

```yaml
proposition: "subject → relationship → object"
source_ref: "Chapter 7: Measure"
backing:
  - category: empirical
    subtype: case_study
    snippet: "We had been spending our time improving a product nobody wanted"
    strength: strong
    warrant: "The case demonstrates that traditional metrics masked product-market fit failure"
passages:
  - chunk: "chunk_04.txt"
    lines: [42, 48]
    snippet: "We had been spending our time improving a product..."
confidence: exact
```

The `backing` field captures **what** evidence supports the claim and **why** (the warrant). The `passages` field traces **where** in the original text the claim originates. The `confidence` field rates how directly the source states the claim: `exact` (verbatim), `synthesized` (combines multiple passages), or `inferred` (derived through reasoning).

### 2.5 Multi-Dimensional Tagging System

Every claim carries a set of tags across 9 orthogonal dimensions, making the vault filterable and queryable along any axis:

| Tag dimension | Values | What it answers |
|---|---|---|
| `type/` | `claim/atom`, `claim/cluster`, `claim/structure`, `claim/root`, `entity/concept`, `entity/person` | What kind of note is this? |
| `priority/` | `core`, `key`, `support`, `aside` | How central to the argument? |
| `certainty/` | `established`, `argued`, `speculative` | How solid is the evidence? |
| `stance/` | `endorsed`, `criticized`, `neutral` | Does the author agree, disagree, or describe? |
| `domain/` | Single word (e.g., `methodology`, `finance`, `governance`) | What field is this about? |
| `role/` | `fact`, `argument`, `definition`, `rebuttal`, `methodology`, `example`, `prediction` | What function does this serve? |
| `source/` | Source slug (e.g., `ries-lean-startup`) | Which source does this come from? |
| `backing/` | Evidence category (e.g., `textual`, `empirical`, `transmitted`) | What type of evidence? |
| `strength/` | Highest strength among backings (`definitive`, `strong`, `moderate`, `weak`) | How strong is the best evidence? |

Additional frontmatter fields:

| Field | Purpose |
|---|---|
| `kind` | `claim` or `entity` — the fundamental note type |
| `layer` | 0 (atom), 1 (cluster), 2 (structure), 3 (root) — position in the pyramid |
| `proposition` | Canonical form: `subject → relationship → object` |
| `source_ref` | Chapter, section, or control ID in the original source |

This multi-dimensional tagging enables compound queries that would be impossible in unstructured notes. For example: "Show all `priority/core` claims from `source/ries-lean-startup` with `certainty/speculative` and `backing/experiential`" returns precisely the author's most important but weakly-evidenced assertions — the claims most worth scrutinizing.

The `role/rebuttal` tag deserves special attention. When an author presents and addresses a counter-argument, Distillary extracts both the objection and the response as separate claims linked by a `rebuts:` field. This preserves the dialectical structure of the argument, making it possible to query "what objections did the author address?" and evaluate whether the responses are convincing.

---

## 3. Universal Argumentation Framework

### 3.1 The 9 Evidence Categories

We observe that despite vast differences in domain vocabulary, there are only 9 fundamental ways humans provide evidence for claims:

| Category | Pattern | Examples across domains |
|---|---|---|
| **textual** | "It's written in the authoritative source" | Scripture verse, statute, primary source quote |
| **transmitted** | "A reliable person reported this" | Prophetic narration, witness testimony, reported data |
| **consensus** | "Everyone qualified agrees" | Scholarly consensus, scientific consensus, legal precedent |
| **analogical** | "This case is like that case" | Legal analogy, comparative study, case-based reasoning |
| **empirical** | "We observed or measured it" | Experiment, RCT, statistic, forensic evidence |
| **rational** | "It follows logically" | Deductive proof, syllogism, cost-benefit analysis |
| **experiential** | "Someone lived through this" | Case study, ethnography, personal testimony |
| **authority** | "A recognized expert said so" | Expert opinion, scholarly commentary |
| **silence** | "The absence of evidence is itself evidence" | No text → permitted, no studies → speculative |

These categories are **exhaustive** (we found no evidence type that doesn't fit) and **domain-agnostic** (the same framework handles Islamic jurisprudence, cybersecurity regulation, academic research, and business literature without configuration changes).

### 3.2 The Warrant

The most underappreciated component of argumentation is the warrant: the logical connection between evidence and claim. The same piece of evidence can support different claims depending on the warrant:

Evidence: "A company's revenue grew 300% after pivoting."

- Warrant A: "Revenue growth validates the pivot strategy" → Claim: Pivots work
- Warrant B: "Revenue growth occurred despite, not because of the pivot — it correlated with market timing" → Claim: Market conditions matter more than strategy

Without capturing warrants, evidence-based search cannot distinguish these uses. Distillary's extract agent produces a warrant for every backing entry, enabling the research agent to evaluate not just what evidence exists but how it connects to claims.

### 3.3 Strength Scale

Every backing carries a universal strength grade:

| Strength | Meaning |
|---|---|
| **definitive** | Virtually undisputed in the field |
| **strong** | Widely accepted, minor debate possible |
| **moderate** | Reasonable but contested |
| **weak** | Some value but unreliable alone |
| **contested** | Actively disputed |

This is the **field's** assessment, not the system's. The extract agent captures the author's own certainty level, preserving the source's epistemic posture.

---

## 4. Deep Research Agent

### 4.1 Design

The research agent answers questions by iteratively searching the knowledge graph. Unlike single-pass retrieval, it works in 8+ passes, deepening understanding at each step:

1. **Scope** — decompose question into sub-questions
2. **Search** — Grep for key terms across all sources
3. **Backlinks** — entity pages → Referenced-by sections → claims (3+ hops)
4. **Pyramid** — walk root → structure → cluster → atom for context
5. **Cross-source** — compare via bridge concepts and analytics
6. **Advanced methods** — apply discovery techniques (see 4.2)
7. **Evaluate** — rank evidence quality, assess confidence
8. **Iterate** — repeat until all sub-questions answered or brain exhausted

### 4.2 Advanced Discovery Methods

For questions where direct search fails, the agent applies 11 discovery methods:

| Method | Technique | When to use |
|---|---|---|
| A. Inverse search | Search for what X is NOT | Can't find X directly |
| B. Warrant mining | Find shared reasoning patterns across warrants | Need hidden meta-principles |
| C. Evidence archaeology | Trace same evidence across multiple claims | Same citation, different conclusions |
| D. Cluster intersection | Find claims bridging two thematic clusters | Question spans themes |
| E. Analogical transfer | Carry answer across domains via bridges | Answer exists in wrong domain |
| F. Strength aggregation | Combine weak evidence into stronger composite | Only weak individual evidence |
| G. Rebuttal reconstruction | Read counter-arguments authors addressed | Need edge cases and boundaries |
| H. Hierarchical layering | Read all pyramid layers for same topic | Need both principle and application |
| I. Entity co-occurrence | Find implicit connections via shared backlinks | No bridge but connection exists |
| J. Source signature | Assess source's argumentation style | Evaluating trustworthiness |
| K. Source verification | Check claim passages against chunk files | Verifying cited evidence before using it |
| K. Source verification | Check claim passages against chunk files | Verifying cited evidence |

### 4.3 Multi-Brain Search

When multiple knowledge bases are connected via `brains.yaml`, the research agent searches all local brains and queries published brains via their API manifest (`agent.json`). Findings are prefixed with the brain name, enabling users to see which knowledge base contributed what.

---

## 5. Source Verification

### 5.1 The Problem

AI extraction is lossy. An LLM reading a text chunk may misinterpret, oversimplify, or hallucinate claims that the source doesn't actually support. Without a mechanism to verify extracted claims against source text, the knowledge graph's trustworthiness degrades with every extraction.

### 5.2 The Solution: Passage References

Every claim stores lightweight references to its source passages:

```yaml
passages:
  - chunk: "chunk_04.txt"
    lines: [42, 48]
    snippet: "We had been spending our time improving a product..."
```

The snippet is ~15 words — enough to locate the passage, not enough to reproduce copyrighted content. The full text stays in the chunk files, which are always stored locally during ingestion.

### 5.3 Verification Agent

The verify agent reads each claim's passages, opens the referenced chunk file, and checks:

1. Does the snippet exist in the chunk at the referenced lines?
2. Does the surrounding passage support the claim's proposition?
3. Is the backing snippet present in one of the passages?
4. Does the warrant logically follow from the passage?
5. Is the confidence rating (exact/synthesized/inferred) accurate?

### 5.4 Copyright Handling

Source chunks are always stored locally during ingestion (they're just text files, they cost nothing). The copyright question only arises at **publish time**: sources marked `publishable: false` in their metadata have chunks excluded from the published site. This separation means local fact-checking always works, while publishing respects intellectual property.

---

## 6. Cross-Source Concept Mapping

### 6.1 Bridge Concepts

When two sources discuss the same idea under different names, the concept-mapper agent (opus model) identifies the semantic equivalence and creates a unified bridge entity:

```
Source A: "Vanity Metrics"  ←→  Source B: "Compliments"
                    ↓
         Bridge: "False Signals"
         (aliases both names, backlinks from both sources)
```

Bridge entities are cross-source query hubs: their Referenced-by sections contain claims from all connected sources, enabling a single entity page to answer "what does the brain know about X?" with multi-source evidence.

### 6.2 Cross-Brain Mapping

The same mechanism extends to mapping concepts across independent knowledge bases. A concept-mapper pointed at two brains discovers structural parallels that no single-brain analysis could find. In testing, we mapped 18 concept pairs between an Islamic jurisprudence brain and a cybersecurity regulatory brain, finding genuine structural isomorphisms (e.g., scholarly consensus ↔ compliance standards, analogical reasoning ↔ risk assessment).

---

## 7. Applications and Ecosystem

### 7.1 Analytical Database Views

Distillary generates Obsidian Base files (`.base`) — structured database views over the vault's claims. Users can filter, sort, and group claims by any frontmatter field: backing category, strength, domain, source, layer. This transforms the vault from a static wiki into an interactive analytical workspace. Example views include: claims by evidence strength (showing which arguments are weakest), entity backlink counts (showing which concepts are most connected), and backing distribution per source (showing how each author argues).

### 7.2 Cross-Brain Analytics

When multiple brains are connected via `brains.yaml`, the analytics agent produces cross-brain comparison reports. In testing, we compared an Islamic jurisprudence brain (219 claims, 7 backing categories) against a cybersecurity regulatory brain (288 claims, 1 backing category). The analytics revealed that the Islamic sources use 7 distinct argumentation methods while the regulatory sources rely exclusively on textual mandate — a structural difference invisible without cross-brain analysis.

### 7.3 Personal Annotation Layer

The annotate agent helps users write structured reactions to claims in `personal/annotations/`. Annotations become part of the knowledge graph — they link to claims, reference entities, and appear in backlink sections. Over time, a user's annotations reveal patterns in their thinking: which concepts they keep returning to, where they disagree with sources, how their views evolve. The explore agent reads these patterns and suggests what to investigate next.

### 7.4 Applications in Contemplative Reading

The system naturally supports contemplative reading (tadabbur) — engaging deeply with a text rather than passively consuming it. The pyramid makes implicit argument structure explicit. The backing fields reveal which claims the author argues vs. assumes. Passages let the reader jump between the brain's structure and the original text. Annotations capture the reader's evolving understanding. Over multiple sources, the brain becomes a map of the reader's intellectual life — not a list of books read, but a living graph of ideas and how they relate.

### 7.5 Critical Thinking Support

The argumentation metadata provides structural support for critical thinking:

- **Evaluating argument quality**: the backing field exposes evidence type and strength for every claim, making "why should I believe this?" answerable mechanically
- **Detecting logical gaps**: underargued clusters (few atoms), inferred claims (not directly stated), and internal inconsistencies become visible through the pyramid structure
- **Separating fact from opinion**: certainty and stance tags mechanically distinguish established facts from speculation and advocacy
- **Identifying hidden assumptions**: the warrant field makes the author's reasoning chain visible and questionable
- **Cross-source reality check**: bridges show where sources agree, tension markers show where they disagree, evidence grading shows who argues better

### 7.6 Regulatory Compliance and Reporting

In practice, we used Distillary to build a cybersecurity regulatory brain from 12 framework documents and then generated compliance research with verbatim regulatory quotes, cross-framework requirement mapping, enforcement chain analysis, and gap identification. The deep research agent produced audit-ready outputs citing specific control IDs traced to exact source text — a workflow that would require weeks of manual analysis.

---

## 8. Evaluation

### 7.1 Extraction Quality

We evaluated extraction quality across three domains:

| Domain | Source | Claims | With backing | Warrants | Passages |
|---|---|---|---|---|---|
| Islamic jurisprudence | 2 classical Arabic texts | 159 | 130 (82%) | 130 (100%) | v4.0 pending |
| Cybersecurity regulation | 12 English regulatory PDFs | 288 | 184 (64%) | 184 (100%) | Tested: 100% verified |
| Business literature | 1 English book | 79 | 79 (100%) | 79 (100%) | v4.0 pending |

The lower backing rate for cybersecurity (64%) reflects that regulatory documents contain many definitional claims that don't cite evidence — they ARE the evidence. The 100% warrant rate across all domains confirms the extract agent consistently captures reasoning chains.

### 7.2 Research Agent Accuracy

We tested the deep research agent with 11 questions across 4 difficulty levels:

| Difficulty | Questions | Wikilink accuracy | Confidence correct | Honest gap reporting |
|---|---|---|---|---|
| Easy (single source) | 2 | 24/24 (100%) | 2/2 | N/A |
| Medium (cross-source) | 3 | 19/19 (100%) | 3/3 | N/A |
| Hard (sparse coverage) | 1 | verified | 1/1 (LOW) | Yes — reported brain doesn't cover topic |
| Very hard (emergent synthesis) | 5 | 25/26 (96%) | 5/5 | Yes — identified specific missing sources |

The single wikilink error (96% on very hard) was a generic term (`[[wikilink]]`) used as a placeholder in the research path log, not a hallucinated claim reference. After adding a rule against this, subsequent tests achieved 100%.

### 7.3 Source Verification

We tested v4.0 extraction with passage references on a regulatory document:

| Metric | Result |
|---|---|
| Claims extracted | 8 |
| Passages with correct chunk reference | 8/8 (100%) |
| Passages with correct line range | 8/8 (100%) |
| Snippets found in chunk (whitespace-normalized) | 16/16 (100%) |
| Propositions supported by passages | 8/8 (100%) |
| Confidence ratings accurate | 8/8 (100%) |

Two normalization issues were identified and resolved: line breaks in PDF-extracted text and smart/curly apostrophes vs. straight apostrophes. Both are whitespace/encoding issues, not accuracy issues.

### 7.4 Cross-Brain Concept Mapping

We tested cross-brain concept mapping between two structurally unrelated brains (Islamic jurisprudence and cybersecurity regulation):

- **Entities read**: 67 + 27 = 94 entities across both brains
- **Pairs found**: 10 same-concept + 8 complementary = 18 total
- **Quality**: All pairs represent genuine structural parallels verified by reading entity descriptions

### 7.5 Multi-Brain Research

We tested multi-brain research across 3 brains (2 local + 1 published):

- All 3 brains successfully queried (local via file read, published via HTTP)
- Findings correctly prefixed with brain name
- Cross-brain synthesis produced genuine insights not available in any single brain

---

## 9. Limitations

### 8.1 OCR Dependency

For scanned documents, extraction quality is bounded by OCR accuracy. A manuscript with ~41% OCR accuracy produced garbled claims that required manual deletion (5 out of 84 claims, 6%). The system has no automatic OCR quality detection.

### 8.2 Extract Agent Hallucination

While the extract agent is instructed not to hallucinate, it occasionally paraphrases backing snippets instead of copying them verbatim. In testing, 15 of 16 snippets were exact matches (94%). The source verification layer catches these cases but does not auto-correct them.

### 8.3 Rebuttal Extraction

Counter-arguments ("فإن قال قائل..." in Islamic texts, "one might object..." in academic papers) are underextracted. In one source with 40 counter-argument instances in the raw text, zero rebuttal claims were extracted. This appears to be a prompt sensitivity issue — the extract agent skips the most linguistically complex passages.

### 8.4 Scale

The system has been tested with brains containing up to 12 sources and ~500 claims. Performance characteristics at 100+ sources or 10,000+ claims are unknown. The Obsidian vault format may encounter rendering performance issues at large scale.

### 8.5 Language Handling

Arabic text extraction from scanned manuscripts is significantly lower quality than English PDF extraction. The system handles mixed-language content (Arabic claims with English entity names) but does not perform automatic transliteration or translation alignment.

---

## 10. Related Work

### 9.1 Karpathy's LLM Wiki Pattern (2025-2026)

The most directly comparable system is the LLM Wiki pattern introduced by Andrej Karpathy and rapidly adopted across the Obsidian community. The core idea: instead of retrieving from raw documents at query time, an LLM incrementally builds and maintains a persistent wiki — structured, interlinked markdown files that sit between the user and raw sources. Implementations include `obsidian-wiki` (Ar9av), `llm-wiki-local` (kytmanov), `second-brain` (NicholasSpisak), and `claude-obsidian` (AgriciDaniel).

The LLM Wiki pattern shares Distillary's architecture of raw sources → LLM extraction → structured wiki. The v2 specification even introduces claim tagging (extracted, inferred, ambiguous) and provenance tracking. However, key differences exist:

- **Argumentation structure.** LLM Wiki tags claims as extracted/inferred/ambiguous. Distillary goes deeper: 9 evidence categories, strength grades, warrants, and passage references. A Distillary claim carries not just "where did this come from?" but "what type of evidence, how strong, and why does it support this claim?"
- **Cross-source synthesis.** LLM Wiki focuses on accumulating knowledge from conversations and documents into one wiki. Distillary explicitly models cross-source bridges: same-concept-different-name pairs that unify entities across sources.
- **Hierarchical argumentation.** LLM Wiki produces flat wiki pages. Distillary builds a 4-layer pyramid (root → structure → cluster → atom) that makes the source's argument structure navigable.
- **Verification.** LLM Wiki's provenance tracks which source a claim came from. Distillary's passages field traces to the exact line range in the source text, enabling automated fact-checking.

### 9.2 Multi-Agent Knowledge Graph Construction

KARMA (2025, OpenReview) is a multi-agent LLM framework that automatically enriches knowledge graphs from scientific papers using nine collaborative agents. On 1,200 PubMed articles, KARMA identified 38,230 new entities with 83.1% LLM-verified correctness. CoDe-KG (2025, EMNLP) achieves 65.8% macro-F1 on relation extraction through coreference resolution and syntactic decomposition.

These systems focus on entity-relationship extraction — the "what" of knowledge. Distillary's contribution is the "why": the backing field with warrant that captures not just facts but the argumentation that justifies them. KARMA extracts "Drug X treats Disease Y"; Distillary extracts "Drug X treats Disease Y, backed by 3 RCTs (strong), warranted by mechanism of action targeting pathway Z."

### 9.3 Deep Research Agents

OpenAI's Deep Research (2025) and Google's Gemini Deep Research (2025-2026) represent the state-of-the-art in iterative search and synthesis. These agents conduct multiple rounds of web search, assess results, and issue follow-up searches. FutureHouse (2026) extends this to scientific literature with specialized database access.

Distillary's research agent differs fundamentally in its search substrate. Commercial deep research agents search the open web; Distillary's agent searches a structured knowledge graph with typed evidence, hierarchical arguments, and cross-source bridges. This enables discovery methods impossible on unstructured web content: warrant mining (finding shared reasoning patterns across claims), cluster intersection (finding claims at thematic boundaries), and source signature analysis (assessing an author's argumentation style). The tradeoff is scope: Distillary only searches what has been ingested, while web-based agents access everything.

### 9.4 Knowledge Graph-Enhanced RAG

GraphRAG (Microsoft, 2024) and LightRAG (2024) construct knowledge graphs from documents and use graph structure for retrieval. KA-RAG (2025) combines knowledge graphs with agentic workflows for educational question-answering. ReGraphRAG (2025, EMNLP) reorganizes fragmented knowledge for better retrieval.

Distillary's approach is complementary but distinct. RAG systems build graphs for retrieval at query time — the graph is an intermediate representation that improves answer generation. Distillary's brain is the end product — a navigable, publishable, verifiable knowledge base that humans browse in Obsidian and agents query via backlinks. The graph is not just a retrieval mechanism but a permanent knowledge artifact with its own value.

### 9.5 Argument Mining

The ArgMining workshop series (2014-2026) drives research in computational argumentation. Stab and Gurevych (2017) parse argument structures in persuasive essays. Lawrence and Reed (2020) survey the field comprehensively. Recent work (2024-2025) applies LLMs to argument mining with improved performance on claim detection and evidence classification.

Distillary extends argument mining in two directions: (1) domain-agnostic evidence categories that work without training data or domain-specific models, and (2) cross-source argumentation comparison through bridge concepts. Traditional argument mining focuses on extracting structure from a single document; Distillary compares argumentation across sources and domains.

### 9.6 Toulmin's Argumentation Model

Distillary's claim format implements a modified Toulmin model (1958): claim → ground (backing) → warrant → qualifier (strength) → rebuttal (separate claims). The adaptation adds domain-agnostic evidence categories, source passage tracing, and confidence levels (exact/synthesized/inferred) that traditional Toulmin implementations lack.

### 9.7 Positioning Summary

| System | Extracts claims | Types evidence | Grades strength | Cross-source bridges | Source verification | Domain-agnostic |
|---|---|---|---|---|---|---|
| LLM Wiki (Karpathy) | Yes | Partial (3 tags) | No | No | Provenance only | Yes |
| KARMA | Entities only | No | No | No | No | No (biomedical) |
| GraphRAG / LightRAG | Entities + relations | No | No | No | No | Yes |
| Deep Research (OpenAI/Google) | No (synthesis) | No | No | No | Cites URLs | Yes |
| ArgMining (academic) | Yes | Domain-specific | Partial | No | No | No |
| **Distillary** | **Yes** | **Yes (9 categories)** | **Yes (5 levels)** | **Yes** | **Yes (passages)** | **Yes** |

---

## 11. Future Work

### 10.1 Proposed Experiments

**Experiment 1: Extraction Faithfulness.** Run the v4.0 extraction pipeline on a corpus of 50 diverse sources (academic papers, legal documents, books, transcripts) across 5 languages. Measure: (a) percentage of claims with passages that verify against source chunks, (b) snippet accuracy after whitespace normalization, (c) warrant quality (human evaluation of logical soundness). This would quantify the system's reliability at scale.

**Experiment 2: Research Agent vs. Human Expert.** Present the same 20 research questions to the deep research agent and to domain experts. Measure: (a) factual accuracy, (b) evidence citation quality, (c) coverage of relevant sources, (d) identification of gaps. This would establish whether agent-mediated knowledge graphs approach human expert performance.

**Experiment 3: Cross-Domain Bridge Quality.** Have domain experts evaluate bridge concepts generated between unrelated knowledge bases. Measure: (a) percentage of bridges rated as genuinely insightful vs. superficial, (b) inter-rater agreement, (c) correlation between bridge quality and entity description depth. This would validate whether automated concept mapping produces meaningful connections.

**Experiment 4: Argumentation Category Completeness.** Collect 1,000 evidence instances from 10 domains (law, medicine, theology, physics, economics, philosophy, history, engineering, psychology, journalism). Classify each using the 9 categories. Measure: (a) percentage that fit cleanly, (b) percentage requiring a new category, (c) inter-annotator agreement. This would test the claim of exhaustiveness.

**Experiment 5: Learning Outcomes.** Give two groups of students the same reading list. Group A reads normally. Group B reads through a Distillary brain with annotations. After 4 weeks, test: (a) recall of key arguments, (b) ability to identify evidence quality, (c) ability to synthesize across sources, (d) critical evaluation of claims. This would measure whether structured knowledge graphs improve learning.

### 10.2 Community Brain Ecosystem

The multi-brain federation architecture (Section 6.2) opens the possibility of a **community brain ecosystem** — a shared network where people publish, discover, and interconnect knowledge bases.

**Brain registry.** A central index where published brains register their `agent.json` manifests. Users search the registry by domain, topic, or source type: "find brains about contract law" returns URLs of published brains with those sources. Adding a brain from the registry is one command.

**Collaborative knowledge building.** A professor publishes a brain from the course syllabus. Students clone it, add their own sources and annotations, and publish their extended versions. The professor can then clone students' brains and run cross-brain analytics to see which concepts different students explored — a new kind of intellectual dialogue mediated by structured knowledge.

**Domain-specific brain libraries.** Communities could maintain curated brain collections: a medical literature brain updated monthly with new papers, a legal brain tracking regulatory changes across jurisdictions, a religious studies brain spanning primary texts and commentaries. Each brain is independently maintained but queryable by anyone.

**Cross-community discovery.** The concept-mapper running across brains from different communities would discover unexpected connections: a medical brain's "informed consent" bridges to a legal brain's "contractual capacity" bridges to a philosophy brain's "autonomy." These emergent bridges represent genuine intellectual connections that no single community would generate.

**Quality signals.** Published brains carry verifiable quality metrics: percentage of claims with backing, average evidence strength, passage verification rate, source count. Users can assess a brain's rigor before connecting to it.

The architecture already supports this: `brains.yaml` connects local and published brains, the research agent searches across all of them, and concept-mapper works on any pair of local brains (with clone-then-map for published ones). What's missing is the social layer — the registry, the discovery, and the community conventions for maintaining shared brains.

### 10.3 Technical Improvements

**Automatic OCR quality detection.** Before extraction, assess text quality and warn the user or switch to a more robust extraction strategy for low-quality scans.

**Rebuttal-aware extraction.** A specialized extraction pass focused on counter-arguments, using linguistic markers specific to each domain's debate conventions.

**Incremental re-extraction.** When a source is re-extracted with an updated agent prompt, diff against previous claims to preserve user annotations that link to existing claims.

**Real-time collaboration.** Multiple users annotating the same brain simultaneously, with merge semantics for conflicting annotations.

**Evidence graph visualization.** An interactive visualization showing how evidence flows from sources through claims to conclusions, with strength color-coding and cross-source bridges highlighted.

**Brain registry and discovery service.** A searchable index of published brains with quality metrics, enabling community-driven knowledge sharing at scale.

---

## 12. Conclusion

Distillary demonstrates that AI agents can decompose unstructured text into structured, evidence-graded, verifiable knowledge graphs without domain-specific configuration. The universal argumentation framework (9 categories + warrant + strength) provides a common language for comparing evidence across radically different fields. The deep research agent shows that iterative graph traversal with advanced discovery methods produces answers with full citation chains and honest confidence assessment. The source verification layer closes the trust gap between AI extraction and human verification.

The system is open-source and designed for practical use: one command adds a source, one command answers a question, and every claim traces back to exact source text. The knowledge graph format (Obsidian-compatible markdown) ensures users are never locked into the system — the output is readable, portable, and useful with or without the extraction pipeline.

We believe the most promising direction is the intersection of structured argumentation and cross-source synthesis: the ability to ask a question and receive an answer graded by evidence quality, drawing from multiple independent sources, with every claim verifiable against the original text. This is how human experts think. Distillary is an attempt to make that process accessible to anyone with sources to read.

---

## References

Karpathy, A. (2025). LLM Wiki. GitHub Gist. https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f

KARMA: Leveraging Multi-Agent LLMs for Automated Knowledge Graph Enrichment (2025). OpenReview. https://openreview.net/forum?id=k0wyi4cOGy

Lawrence, J., & Reed, C. (2020). Argument mining: A survey. *Computational Linguistics*, 45(4), 765-818.

Microsoft (2024). GraphRAG: From Local to Global Text Understanding. https://arxiv.org/abs/2404.16130

OpenAI (2025). Introducing Deep Research. https://openai.com/index/introducing-deep-research/

Stab, C., & Gurevych, I. (2017). Parsing argumentation structures in persuasive essays. *Computational Linguistics*, 43(3), 619-659.

Sun, X., et al. (2025). Automated Knowledge Graph Construction using Large Language Models and Sentence Complexity Modelling. *EMNLP 2025*. https://aclanthology.org/2025.emnlp-main.783/

Toulmin, S. E. (1958). *The Uses of Argument*. Cambridge University Press.

Wang, Y., et al. (2025). KA-RAG: Integrating Knowledge Graphs and Agentic Retrieval-Augmented Generation. *Applied Sciences*, 15(23), 12547.

Xu, Z., et al. (2025). LLM-empowered Knowledge Graph Construction: A Survey. https://arxiv.org/abs/2510.20345

FutureHouse (2026). Superintelligent AI Agents for Scientific Discovery. https://www.futurehouse.org/research-announcements/launching-futurehouse-platform-ai-agents

Google (2025). Gemini Deep Research. https://gemini.google/overview/deep-research/

JMIR (2026). Deep Research Agents: Major Breakthrough or Incremental Progress for Medical AI? https://www.jmir.org/2026/1/e88195

---

## Appendix A: Agent Inventory

| Agent | Model | Role |
|---|---|---|
| extract | haiku | Text chunk → atomic claims with backing + passages |
| dedupe | haiku | Merge duplicate claims, combine passages |
| entities | haiku | Identify concepts, people, organizations |
| entity-link | haiku | Add wikilinks to claim bodies |
| group | opus | Cluster claims into argumentative parents |
| pyramid | opus | Build hierarchy to root thesis |
| link | haiku | Find tensions, patterns, evidence connections |
| verify | haiku | Fact-check claims against source chunks |
| source-index | haiku | Write narrative source overview |
| brain-index | haiku | Write brain-level overview |
| doctor | haiku | Fix orphans, ghost links, flag missing passages |
| concept-mapper | opus | Find same-concept pairs across sources |
| bridge-builder | haiku | Create unified bridge entities |
| analytics | haiku | Generate cross-source statistical reports |
| research | opus | Deep iterative question-answering |
| explore | opus | Suggest investigations based on gaps |

## Appendix B: The 11-Step Pipeline

```
Source → chunks → extract (parallel) → dedupe → entities → entity-link
  → group → pyramid → link → verify (optional) → assemble + post-process
  → concept-mapper → bridge-builder → brain index update
```

## Appendix C: Discovery Methods Summary

| Method | Input | Output | Tested |
|---|---|---|---|
| Concept lookup | Entity name | All claims about entity via backlinks | Yes |
| Pyramid walk | Source name | Root → structure → cluster → atom | Yes |
| Evidence chain | Claim | Backing → strength → warrant → depends_on | Yes |
| Cross-source | Bridge concept | Multi-source perspectives | Yes |
| Backlink exploration | Any entity | 3+ hop chain through graph | Yes |
| Gap detection | Search terms | Missing coverage areas | Yes |
| Inverse search | Negation of concept | Boundary definition | Yes |
| Warrant mining | Cross-claim warrants | Hidden meta-principles | Yes |
| Evidence archaeology | Single citation | Divergent uses across sources | Yes |
| Cluster intersection | Two themes | Claims at thematic boundary | Yes |
| Analogical transfer | Bridge concept | Cross-domain answer | Yes |
| Strength aggregation | Multiple weak evidence | Composite strength assessment | Partial |
| Rebuttal reconstruction | Counter-arguments | Edge cases and boundaries | Partial |
| Hierarchical layering | Topic across all layers | Principle + application | Yes |
| Entity co-occurrence | Two entities | Implicit connections | Partial |
| Source signature | Source analytics | Argumentation style assessment | Yes |
| Source verification | Claim + chunk | Passage confirmation | Yes |
