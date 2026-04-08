# Distillary Brain — Agent Retrieval Demo

Any AI agent with web access can query a published Distillary brain. No API keys, no MCP server, no authentication. Just a URL and a skill.

## Get the skill

One fetch. Paste it into your agent. Done.

```
curl https://brain.distillary.xyz/static/skill.md
```

Or from GitHub:

```
curl https://raw.githubusercontent.com/distillary/distillary/main/.claude/skills/distillary-retrieval.md
```

Every published brain serves its own skill at `/static/skill.md`. The `agent.json` manifest also points to it:

```json
{ "brain": { "skill": "/static/skill.md" } }
```

An agent discovering a brain for the first time can fetch `agent.json`, see the skill URL, fetch the skill, and start querying — fully autonomous, zero human setup.

---

## Try it with your agent

Pick your tool. Paste the skill. Ask a question. The agent walks the brain on its own.

### Claude Code

Already built-in. Just say:

```
Query https://brain.distillary.xyz — what does this brain know about debt?
```

### Codex (OpenAI)

Add to your `AGENTS.md` or system instructions:

```
When asked about a Distillary brain, fetch {url}/static/agent.json first.
It tells you what's in the brain and how to navigate it.
Follow links by relevance. Backlinks on entity pages ARE the answers.
```

Then: `codex "Query https://brain.distillary.xyz — what is Barnum's view on luck?"`

### Gemini CLI

Add to your system prompt or context file:

```
You can query Distillary brains at any URL.
Start with GET {url}/static/agent.json for the manifest.
Walk pages: entity pages have backlinks = claims about that concept.
2 fetches answers most questions.
```

Then: `gemini "Using https://brain.distillary.xyz — how important is integrity in business?"`

### OpenCode / Aider / Cline

Add to `.opencode/agents.md`, `.aider.conf.yml`, or your system prompt:

```
# Distillary Brain Retrieval
Fetch {brain_url}/static/agent.json for navigation instructions.
CONCEPT questions → find entity → read backlinks (they ARE the answer).
SOURCE questions → thesis is in manifest → fetch root_note for pyramid.
Every page has: content + wikilinks (deeper) + backlinks (wider).
```

### Cursor / Windsurf / Continue

Add to `.cursorrules`, `.windsurfrules`, or `config.json` system prompt:

```
When querying a Distillary brain:
1. GET {url}/static/agent.json — returns sources, navigation, bridges
2. For "what is X?" → find entity page → backlinks = claims about X
3. For "summarize" → thesis in manifest → fetch root_note
4. 2 fetches, <2000 tokens per question
```

### Any agent with HTTP access

The universal skill to paste into any system prompt:

```markdown
# Distillary Brain Retrieval

You can query Distillary brains — published knowledge bases at a URL.

## How to use

1. Fetch {brain_url}/static/agent.json — returns what's in the brain,
   navigation instructions, and source metadata
2. Pick your strategy based on the question:
   - CONCEPT ("what is X?") → find entity → fetch page → read backlinks
   - SOURCE ("what does this argue?") → thesis in manifest → fetch root_note
   - COMPARISON ("do sources agree?") → fetch bridge concept or /shared/analytics/comparison
   - EVIDENCE ("prove it") → walk pyramid: root → cluster → structure → atom
   - EXPLORATORY ("what's related?") → any entity → follow backlinks + wikilinks
3. Follow 2-3 links for evidence. Most questions: 2 fetches, <2000 tokens.

Every page has: content + wikilinks (go deeper) + backlinks (go wider).
```

That's it. No SDK. No API key. No MCP server. The agent fetches `agent.json`, reads the navigation instructions, and walks pages by relevance.

---

## Demo: 10 questions answered from the live brain

**Brain URL:** https://brain.distillary.xyz
**Source:** The Art of Money Getting by P.T. Barnum (1880)
**Method:** Each question answered by fetching `agent.json` then walking pages.

---

## Q1: What books are in this brain?

**Strategy:** Read manifest (1 fetch)
**Fetched:** `/static/agent.json`

**Answer:** The brain contains one source: *The Art of Money Getting* by P.T. Barnum (1880). It's a book with 79 extracted claims and 23 entity pages. Barnum's central thesis is that lasting wealth emerges from the convergence of personal financial discipline, individual capacity and effort, competent business operations, and honest reputation.

---

## Q2: What are the main ideas in this brain?

**Strategy:** Fetch clusters page (2 fetches)
**Fetched:** `agent.json` → `/sources/barnum-art-of-money-getting/claims/clusters/`

**Answer:** Barnum organizes his argument into four pillars:

1. **Financial discipline and capital integrity** — Income must exceed expenditure. Avoid debt. Earn your own capital rather than inheriting it, because the discipline of earning is itself the education needed to preserve wealth.
2. **Personal capacity, vocational fit, and relentless effort** — Health and sobriety provide the foundation. Choose work that matches your aptitude. Then concentrate all effort on that one thing rather than scattering attention.
3. **Honest dealing, genuine advertising, and charitable reputation** — Persistent advertising of genuine goods compounds awareness. Politeness and charity convert transactions into lasting patronage. Integrity opens the credit of an entire community.
4. **Sound business operations** — Maintain personal oversight of critical functions. Hire and retain skilled employees. Keep financial matters confidential to preserve competitive advantage.

---

## Q3: What does Barnum say about debt?

**Strategy:** Concept lookup (2 fetches)
**Fetched:** `agent.json` → `/sources/.../entities/concepts/Debt`

**Answer:** Barnum characterizes debt as enslavement that robs people of dignity and entrepreneurial freedom. His key arguments:

- **Creditors have perfect memories** — hoping they'll forget is futile
- **Compound interest works against the borrower** — the same force that builds wealth for savers actively destroys it for debtors
- **Easy credit corrupts youth** — young people who grow accustomed to borrowing develop lasting patterns of indebtedness
- **Debt cascades** — one purchase on credit triggers further expenses that expand lifestyle permanently

He positions debt avoidance as one of three foundations of financial discipline, alongside maintaining income over expenditure and earning your own capital.

---

## Q4: Does luck play a role in success?

**Strategy:** Concept lookup (2 fetches)
**Fetched:** `agent.json` → `/sources/.../entities/concepts/Luck`

**Answer:** No. Barnum flatly rejects luck as an explanation for success or failure. His argument:

- "Identical causes produce identical effects" — when someone adopts correct methods, luck cannot prevent success
- Failures stem from discoverable causes, not accident
- Finding gold repeatedly in the street is impossible — outcomes follow from proper methods
- Luck serves as an excuse for those avoiding examination of actual causation

Instead, Barnum attributes success to sustained focused effort and perseverance. He argues that wealth without earned understanding actually corrupts character — so even apparent "good luck" (like inheritance) can be destructive.

---

## Q5: How important is integrity in business?

**Strategy:** Concept lookup (2 fetches)
**Fetched:** `agent.json` → `/sources/.../entities/concepts/Integrity`

**Answer:** Integrity is what Barnum calls "the indispensable foundation of lasting prosperity." His reasoning:

- **Dishonesty is always discovered** — and once discovered, it "closes nearly every path to success forever"
- **Honesty opens community credit** — people known for strict honesty receive better access to resources because their promises are trusted
- **Integrity is more valuable than wealth itself** — it enables people to enjoy success peacefully
- **Fraudulent goods lose customers permanently** — while genuine goods with honest advertising compound customer awareness over time

Barnum treats integrity not as a moral luxury but as a commercial engine. It's the fourth pillar of his wealth system, and without it, the other three pillars eventually collapse.

---

## Q6: What is Barnum's advice on choosing a career?

**Strategy:** Concept lookup (2 fetches)
**Fetched:** `agent.json` → `/sources/.../entities/concepts/Vocation`

**Answer:** Barnum's career advice centers on aptitude-vocation alignment:

- **People have innate aptitudes** — natural diversity in talents means different people suit different vocations
- **Misalignment creates lifelong hardship** — forcing someone into an unsuitable profession means they work "up hill" and constantly seek escape
- **Two conditions for success:** (1) select work aligned with your natural capabilities, (2) maintain focused, sustained effort in that single field
- **Constant business changing keeps one poor** — scattered effort across multiple ventures wastes talent
- **Excellence in one's field cannot fail to succeed** — deep mastery of a well-chosen vocation reliably produces wealth

He illustrates this with the contrast between a natural mechanic who thrives versus someone without mechanical aptitude forced into watchmaking.

---

## Q7: What role does health play in wealth creation?

**Strategy:** Concept lookup (2 fetches)
**Fetched:** `agent.json` → `/sources/.../entities/concepts/Health`

**Answer:** Health is the prerequisite that enables everything else. Barnum argues:

- **Without sound health, a person lacks the ambition, incentive, and force needed to make money** — it's foundational, not optional
- **Intoxication prevents sound judgment** — alcohol directly undermines the mental clarity needed for business decisions
- **Tobacco undermines both health and finances** — Barnum himself smoked 10-15 cigars daily before quitting, and speaks from experience
- **People in poor health could improve by understanding natural laws** — health is largely within one's control

Health and sobriety form the base of his "personal capacity" pillar. Without physical and mental foundations, vocational alignment and perseverance are meaningless — you can't concentrate effort if your body and mind are compromised.

---

## Q8: How should you advertise a business?

**Strategy:** Concept lookup (2 fetches)
**Fetched:** `agent.json` → `/sources/.../entities/concepts/Advertising`

**Answer:** Barnum's advertising philosophy is surprisingly systematic for 1880:

- **Persistent newspaper advertising** builds awareness even for excellent products that "bring no return because no one knows about them"
- **Seven exposures before purchase** — he cites a French writer's framework: (1) notice without awareness, (2) read without absorption, (3) read with attention, (4) check prices, (5) discuss with family, (6) become purchase-ready, (7) buy
- **Repetition creates purchasing intention** — consistent exposure compounds into customer action
- **Only advertise genuine goods** — fraudulent goods with advertising accelerate failure rather than prevent it
- **Advertising + integrity compound together** — genuine advertising is one of three components (alongside customer relationships and charitable giving) that build lasting commercial trust

The critical requirement: the product must be real. Advertising amplifies what already exists — quality or fraud.

---

## Q9: Who is P.T. Barnum and why should we listen to him?

**Strategy:** Entity lookup (2 fetches)
**Fetched:** `agent.json` → `/sources/.../entities/people/P.T.-Barnum`

**Answer:** P.T. Barnum (1810-1891) was the author of *The Art of Money Getting* (1880). Known primarily as a showman and entrepreneur, he writes from personal experience rather than academic theory.

His credibility comes from:
- **Firsthand success** — he built and lost fortunes, giving him perspective on both sides
- **Pattern recognition** — he observed countless people succeed and fail, and his writing synthesizes those patterns
- **Willingness to share personal examples** — he discusses his own habits, including smoking 10-15 cigars daily before quitting 14 years prior
- **Practical anecdotes** — he references a London penny showman who relocated to America and accumulated $60,000

What makes his advice relevant 146 years later is how he treats wealth-building as interconnected systems rather than isolated tips. The four pillars (discipline, capacity, operations, reputation) depend on each other — this systemic thinking holds regardless of era.

---

## Q10: What is the root thesis of the entire brain?

**Strategy:** Fetch root note (2 fetches)
**Fetched:** `agent.json` → root_note URL

**Answer:** "Wealth is built by disciplined character operating through sound business practices, not by luck or shortcuts."

This root thesis sits atop a four-pillar pyramid:

1. **Financial discipline** → income over expenditure, avoid debt, earn your own capital
2. **Personal capacity** → health, vocational fit, concentrated perseverance
3. **Sound operations** → owner oversight, skilled employees, strategic secrecy
4. **Honest reputation** → genuine advertising, customer kindness, charitable giving, integrity

The critical insight: **each pillar depends on the others.** Discipline without effort produces nothing. Effort without operational excellence wastes resources. Operations without integrity eventually collapse. And shortcuts — debt, inherited wealth, scattered focus, speculation, fraud — undermine the foundational system they attempt to bypass.

This is why Barnum's framework persists: it's not a list of tips but a system where every choice compounds.

---

## Summary

| # | Question | Strategy | Fetches | Tokens (est.) |
|---|---|---|---|---|
| 1 | What books are in this brain? | Manifest | 1 | ~500 |
| 2 | What are the main ideas? | Clusters | 2 | ~1500 |
| 3 | What about debt? | Concept lookup | 2 | ~1500 |
| 4 | Does luck matter? | Concept lookup | 2 | ~1500 |
| 5 | How important is integrity? | Concept lookup | 2 | ~1500 |
| 6 | Career advice? | Concept lookup | 2 | ~1500 |
| 7 | Role of health? | Concept lookup | 2 | ~1500 |
| 8 | How to advertise? | Concept lookup | 2 | ~1500 |
| 9 | Who is Barnum? | Entity lookup | 2 | ~1500 |
| 10 | Root thesis? | Root note | 2 | ~1500 |

**Average: 1.9 fetches per question, ~1400 tokens per answer.**

All answers sourced from the live brain at https://brain.distillary.xyz using the distillary-retrieval skill. No local files were used — only the published agent API.
