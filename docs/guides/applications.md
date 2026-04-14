---
title: Applications — What You Can Build With a Brain
---

# Applications

Distillary turns sources into a queryable, verifiable knowledge graph. The same pipeline and tools serve radically different purposes depending on what sources you add and what questions you ask.

## Academic Research

### Literature review with evidence grading

Add 10-20 research papers on a topic. Each paper's claims are extracted with backing (empirical/RCT, meta-analysis, cohort study) and strength (definitive/strong/moderate/weak). The brain reveals:

- Which claims are supported by multiple independent studies (convergent evidence)
- Which claims rest on a single weak study (fragile)
- Where studies contradict each other (the research agent flags tensions)
- Which sub-topics have no coverage (gaps)

**Research question:** "What does the evidence actually say about X?"

The deep research agent walks the brain, follows backlink chains across all papers, aggregates evidence strength, and reports: "7 studies support this with strong evidence, 2 contradict with moderate evidence, and no study addresses the mechanism."

### Paper review with source verification

Add one paper. Extract with chunks stored. Every claim traces to the exact passage in the paper. The research agent can then:

- Check if the abstract's claims match what the methods section actually says
- Verify that cited statistics appear in the results
- Flag where the discussion overstates what the data shows
- Identify claims marked `confidence: inferred` — derived by reasoning, not directly stated

**Output:** A structured review with quotes from the paper for every point.

### Comparing two competing theories

Add the seminal paper for Theory A and the seminal paper for Theory B. The concept-mapper finds where they use different terms for the same phenomenon. Bridge concepts reveal:

- Where they agree (same claim, different vocabulary)
- Where they genuinely contradict (same phenomenon, opposite conclusions)
- Where they're complementary (different scope, compatible insights)
- The hidden assumptions each makes that the other doesn't

**Example:** Add Kahneman's "Thinking Fast and Slow" + Gigerenzer's "Gut Feelings." The brain shows where heuristics are bugs (Kahneman) vs. features (Gigerenzer), and where the disagreement is about scope, not substance.

### Thesis writing

Build a brain from your literature. Write your annotations as `personal/annotations/` — your reactions, questions, connections the papers don't make. The research agent can then answer questions using YOUR thinking combined with the literature's evidence, properly cited.

---

## Legal Analysis

### Comparing legal frameworks across jurisdictions

Add regulatory documents from two jurisdictions. Example: EU GDPR + California CCPA, or NIST CSF + ISO 27001, or SOX + UK Companies Act. The concept-mapper finds equivalent requirements under different names. Analytics show:

- Which controls exist in both frameworks
- Which are unique to one jurisdiction
- Where requirements conflict (one allows what the other prohibits)
- How enforcement mechanisms differ

**Research question:** "If I comply with GDPR, what additional controls do I need for CCPA?"

The brain answers with specific article/section IDs from both frameworks, backed by exact regulatory text quotes.

### Contract analysis

Add a set of contracts or legal agreements. Extract clauses as claims. Each clause gets `backing: textual/statutory` with the exact article reference. The research agent can then:

- Find all clauses related to liability across multiple contracts
- Compare termination provisions between contracts
- Identify missing standard clauses
- Trace which clauses derive from which statutory requirements

### Regulatory compliance mapping

Add all applicable regulations for your industry. The brain maps every requirement and shows which controls overlap across frameworks. Example: map NIST CSF → ISO 27001 → SOC 2 → GDPR Article 32, showing how one base requirement (access control) specializes differently for cloud, healthcare, financial services, and privacy.

**Output:** A compliance matrix with exact control IDs, applicable deployment models, and enforcement mechanisms — backed by quoted regulatory text.

### Legal precedent research

Add court opinions on a legal question. Each opinion's holdings become claims with `backing: consensus/binding_precedent` or `authority/persuasive_precedent`. The brain shows:

- The evolution of the doctrine over time
- Which holdings have been distinguished or overruled
- Where circuit splits exist
- The strongest and weakest authority for each side

---

## Islamic Studies

### Cross-book fiqh research

Add multiple usul al-fiqh texts. The brain extracts each scholar's positions with `backing: textual/ayah`, `transmitted/hadith`, `consensus/ijma`, `analogical/qiyas`. The research agent can:

- Trace a ruling across multiple scholars to see where they agree and diverge
- Find the daleel (evidence) for any position — with the exact hadith or verse quoted
- Identify which positions are backed by definitive evidence vs. weak evidence
- Discover where scholars use the same hadith to reach different conclusions (warrant divergence)

**Example:** "What is the evidence for the obligation of congregational prayer?" — the brain returns positions from multiple scholars, each with specific ahadith and Quranic verses, strength-graded, with warrants explaining the reasoning chain.

### Tafsir comparison

Add multiple tafsir (Quran commentary) works. Each commentator's interpretation of a verse becomes a claim with `backing: authority/athar` (companion sayings) or `rational/linguistic` (Arabic analysis). Bridge concepts reveal:

- Where commentators agree on meaning
- Where they offer genuinely different interpretations
- Which interpretations are backed by companion narrations vs. linguistic analysis
- How interpretation evolved across centuries

### Building a personal Islamic library

Add the books you're studying. Write annotations in `personal/annotations/`. The explore agent suggests:

- Concepts you keep encountering but haven't annotated (ghost links)
- Contradictions between sources you haven't addressed
- Topics that multiple sources discuss but you haven't explored
- Questions that emerge from the intersection of your sources

---

## Business and Strategy

### Competitive analysis

Add competitor whitepapers, annual reports, and strategy documents. The brain extracts their stated strategies, claimed differentiators, and market positioning as claims. The research agent reveals:

- Where competitors make the same claim (commoditized positioning)
- Where genuine differentiation exists
- Which claims are backed by data vs. assertion
- Gaps in the market that no competitor addresses

### Due diligence

Add all documents for an acquisition target: financials, contracts, regulatory filings, technical architecture docs. The brain creates a queryable knowledge base where any question ("what are their data sovereignty obligations?") returns specific answers with document references.

### Book synthesis

Add 5 business books on the same topic (e.g., innovation methodology). The brain finds the common principles that all authors agree on and the genuine disagreements. The concept-mapper discovers that Christensen's "disruptive innovation" and Ries's "pivot" and Blank's "customer development" are three vocabularies for overlapping but distinct ideas.

**Output:** A synthesis essay that no single book provides — the meta-argument across all five sources.

---

## Technical Documentation

### Architecture decision records

Add RFCs, design docs, and architecture reviews. Each decision becomes a claim with `backing: rational/design_rationale`. The brain shows:

- Which decisions were justified and which were assumed
- Where decisions conflict with each other
- The chain of dependencies between architectural choices
- Which decisions have been superseded (the brain's abrogation concept handles this naturally)

### Security audit

Add security frameworks + your organization's policy documents. The brain maps every framework requirement to your existing policies, identifies gaps, and generates a compliance report with exact references to both the requirement and your policy.

### API and protocol comparison

Add specifications for competing protocols or APIs. The brain extracts capabilities, requirements, and constraints. Bridge concepts reveal functional equivalences across different naming conventions.

---

## Contemplative Reading (Tadabbur)

### Reading a single book deeply

Most people read a book and forget 90% in a month. Distillary forces a different mode: every idea becomes an atomic claim, every claim has evidence, every concept connects to every other concept. You don't just read — you decompose.

After processing a book, the brain shows you:
- The argument structure you missed on first read (the pyramid makes implicit logic explicit)
- Which claims the author actually argues vs. assumes without evidence (backing field reveals this)
- Which ideas are core vs. peripheral (priority tagging)
- What the author considers certain vs. speculative (certainty tagging)

**This is التدبر made structural.** You see not just what the author said, but how they built their argument, what evidence they relied on, and where the reasoning is strong or weak.

### Connecting ideas across books

Read two books on different topics. The concept-mapper discovers connections neither author intended. This is where the brain becomes more than the sum of its parts.

**Example:** Add a book on cognitive psychology + a book on urban design. The brain discovers both discuss "decision fatigue" — the psychologist studies it in individuals, the urbanist in city navigation systems. Neither cites the other. The bridge concept connects them. You now see the idea from two angles no single reader would naturally combine.

This scales: 5 books produce not 5 separate summaries but a web of interconnected ideas where each book illuminates the others.

### Tracking your evolving understanding

Write annotations as you read: reactions, disagreements, questions, connections to your life. These go to `personal/annotations/` and become part of the graph. Over months of reading:

- The explore agent notices which concepts you keep returning to
- Ghost links show ideas you reference but haven't formally explored
- Your annotation history reveals how your thinking evolved
- You can ask the research agent: "how has my view on X changed across my annotations?"

Your reading becomes a conversation with the text, not passive consumption.

### Reading for contradictions

Add two authors who disagree. The brain doesn't hide the disagreement — it structures it. Tension markers (`⚡ Tension with`) explicitly link contradictory claims. The research agent presents both sides with evidence quality:

- Author A says X, backed by 3 empirical studies (strong)
- Author B says not-X, backed by logical argument + 1 case study (moderate)
- The evidence favors A, but B raises a valid edge case

You don't just know they disagree — you know **why**, **on what evidence**, and **who has the stronger case**.

### Slow reading with source passages

With chunks stored, you can read the brain and jump to the exact original passage whenever you want. This enables a reading mode where:

1. Read the brain's pyramid (5 minutes) — get the full argument structure
2. Drill into a claim that interests you
3. Read its `passages` snippet — see the exact words the author used
4. Open the chunk file for the full surrounding context
5. Write an annotation reacting to the original text
6. The annotation links back to the claim, which links to the entity, which connects to other sources

You're reading the book through its structure, not through its page order. This is how scholars read — jumping between argument, evidence, and context — but the brain does the indexing for you.

### Building a personal canon

Over years, add every important book you read. The brain accumulates. Bridges multiply. Patterns emerge that only appear across dozens of sources:

- The same principle shows up in philosophy, economics, and religion under different names
- An author you read in 2024 contradicts something you accepted from a 2022 book
- A concept from a novel connects to a research paper connects to a religious text

Your brain becomes a map of your intellectual life — not a list of books read, but a living graph of ideas and how they relate.

---

## Critical Thinking

### Evaluating argument quality

Every claim in the brain has a `backing` field that exposes HOW the author argues. This makes invisible reasoning visible:

- A claim backed by `transmitted/hadith_sahih` (strength: definitive) is structurally different from one backed by `rational/analogy` (strength: moderate)
- A claim backed by `empirical/meta_analysis` carries more weight than `experiential/anecdote`
- A claim with NO backing field is a bare assertion — the author stated it without evidence

The brain forces you to ask: "why should I believe this?" for every claim. Not because you're skeptical of everything, but because you can now SEE the evidence structure that was previously hidden in prose.

### Detecting logical gaps

The pyramid reveals what's missing. When you walk from root (thesis) → structure → cluster → atoms, gaps become visible:

- A cluster with 2 atoms is underargued — the author asserted a major point with thin evidence
- An atom with `confidence: inferred` means the extract agent derived the claim — the source never states it directly
- A claim with strong backing that contradicts its parent cluster reveals an internal inconsistency the author didn't resolve

### Separating fact from opinion

The `certainty` and `stance` tags do this mechanically:

- `certainty/established` + `stance/endorsed` = the author presents this as settled fact
- `certainty/argued` + `stance/endorsed` = the author advocates for this but acknowledges debate
- `certainty/speculative` = the author is guessing
- `stance/neutral` = the author presents without endorsing — descriptive, not prescriptive

Read a source filtered by `certainty/speculative` and you see everything the author treats as uncertain. Read by `stance/criticized` and you see everything they reject. The tags make the author's intellectual posture explicit.

### Identifying hidden assumptions

The warrant field in `backing` exposes the reasoning chain the author relies on:

```
Claim: "Debt is enslavement"
Backing: experiential/personal_observation
Warrant: "Creditors have perfect memories and debtors lose dignity"
```

The warrant reveals the assumption: that creditor behavior is universal and that dignity loss is inevitable. You can now question the warrant independently of the claim. Maybe creditors negotiate. Maybe some debt is empowering. The brain made the hidden assumption visible so you can evaluate it.

### Cross-source reality check

When two independent sources make the same claim with different evidence, confidence increases. When they contradict, you have work to do. The brain structures this automatically:

- Bridge concepts show agreement: both sources use different words for the same idea
- Tension markers show disagreement: both address the same topic but reach opposite conclusions
- Evidence quality comparison shows who argues better: one source backs the claim with definitive evidence, the other with speculation

This is systematic triangulation — checking claims against multiple independent sources, graded by evidence quality.

### Questioning the expert

Add a source by a recognized authority. The brain doesn't care about the author's reputation — it grades every claim on its evidence. You might discover that:

- The expert's most famous claim rests on a single anecdote (`backing: experiential`, strength: weak)
- Their strongest evidence supports a point they treat as minor
- 40% of their claims have no identifiable evidence (pure assertion)
- Their counter-argument handling is thin (few rebuttal claims extracted)

The brain treats every author the same way: decompose, grade evidence, expose structure. Authority is not evidence.

### Building your own argument

After reading critically, you have the raw materials to construct your own position:

1. Identify claims you agree with across sources (convergent evidence)
2. Identify where you disagree and why (your annotations capture this)
3. Check the evidence for your position vs. the counter-position
4. The research agent can assemble your argument: "based on these 12 claims from 4 sources, backed by these evidence types, here is the case for X — with these 3 acknowledged weaknesses"

You're not just consuming arguments — you're building your own from verified parts.

---

## Education and Learning

### Study guide from textbook

Add a textbook. The brain creates a navigable hierarchy from chapter thesis to individual facts. The research agent answers exam-style questions with specific textbook references. If chunks are stored, the exact passages are quotable.

### Course synthesis

Add lecture notes, textbook chapters, and supplementary readings for a course. The brain connects ideas across all materials that the course syllabus treats separately. Entity backlinks show every mention of a concept across all course materials.

### Teaching with structured arguments

If you teach, add your course materials + the key texts students read. The brain reveals where your lectures align with the textbook and where they diverge. Students can query the brain: "what does the textbook say about X vs. what the professor emphasized?" — and get a structured answer showing both perspectives.

### Language learning with parallel texts

Add a text in two languages (e.g., Arabic original + English translation). Extract claims from both. The concept-mapper bridges equivalent passages. The brain becomes a parallel concordance where you can see the original and translation side by side at the claim level.

---

## Journalism and Investigation

### Source verification for reporting

Add multiple sources on a story (interview transcripts, documents, public records). The brain extracts claims from each source. The research agent identifies:

- Where sources corroborate each other (convergent testimony)
- Where sources contradict (flag for investigation)
- Which claims are only supported by a single source
- What claims are backed by documents vs. only by testimony

With chunks stored, every fact in the story traces to a specific source passage.

### Long-form investigation

Build a brain over months of investigation. As you add new documents and interview transcripts, the brain grows. Bridge concepts automatically connect new evidence to existing findings. The research agent can answer "what do we know about X?" at any point with full citations.

---

## Personal Knowledge Management

### Reading journal with cross-references

Add every book you read. Your annotations in `personal/annotations/` become part of the graph. Over time, the brain reveals patterns in your thinking — which authors influenced you most, which concepts keep recurring, where your views have evolved.

### Decision journal

Add documents related to a major decision (research, expert opinions, pro/con analyses). The brain structures the arguments for and against. The research agent can present the strongest case for each side with evidence quality ratings.

### Building expertise in a new field

Add the 5 foundational texts in a field you're learning. Start with the brain's cross-source synthesis to get the big picture. Then dive into individual claims when you need depth. Your annotations track your evolving understanding. The explore agent suggests what to read next based on your gaps.

---

## What Makes These Work

Every application above uses the same infrastructure:

| Capability | What it enables |
|---|---|
| **Atomic claims** | Any assertion is queryable independently |
| **Backing with warrant** | Know not just WHAT is claimed but WHY and HOW STRONG |
| **Passages** | Trace any claim to exact source text (when chunks stored) |
| **Cross-source bridges** | Same idea, different vocabulary → unified |
| **Deep research agent** | Complex questions answered with evidence grading |
| **Analytics** | Quantitative comparison across sources |
| **9 universal categories** | Same framework works for hadith, RCT, statute, anecdote |
| **Verify agent** | Automated fact-checking against source text |
| **Personal annotations** | Your thinking is part of the graph |

The brain doesn't care what domain it's in. It cares about claims, evidence, and connections. Add sources → ask questions → get answers with citations.
