---
title: Managing Multiple Brains
---

# Multiple Brains

Each brain is a self-contained knowledge vault focused on a domain. You can connect multiple brains so the research agent searches across all of them.

## Configuration

All connected brains are listed in `brains.yaml` at the project root:

```yaml
brains:
  - name: "Islamic Knowledge"
    path: "brain/"
    type: local
    description: "Jurisprudence methodology, spiritual ethics, practical wisdom"

  - name: "Security Frameworks"
    path: "brain-security/"
    type: local
    description: "Cybersecurity controls, compliance, procurement law"

  - name: "Philosophy"
    path: "https://someone.github.io/philosophy-brain/"
    type: published
    description: "Ethics, epistemology, logic"
```

## Adding a brain

### Local brain (on your disk)

Say: **"add brain at /path/to/brain-name"**

The system:
1. Verifies the path exists with a `sources/` directory
2. Reads `_index.md` for a description
3. Counts the sources
4. Adds it to `brains.yaml`

### Published brain (someone else's, via URL)

Say: **"add brain at https://someone.github.io/their-brain/"**

The system:
1. Fetches `{url}/agent.json` to read the manifest
2. Gets the brain's name, sources, and bridge concepts
3. Adds it to `brains.yaml`

Published brains are read-only — you query them but don't modify them.

### Clone a published brain locally

Say: **"clone brain from https://someone.github.io/their-brain/"**

The system fetches key pages (index, source indexes, bridges, analytics) and saves them locally. This gives you offline access for research. Note: chunks are not included (the publisher may have copyrighted source material).

## How research uses multiple brains

When you ask a question without specifying a brain:

```
"Research: what is the relationship between accountability and governance?"
```

The research agent:
1. Reads `brains.yaml` — finds 2 local brains
2. Searches both: Islamic brain has claims about محاسبة (accountability before God), Security brain has claims about audit trails and compliance enforcement
3. Prefixes findings with brain name:

```
**[Islamic Knowledge]** Accountability (المحاسبة) is a spiritual principle...
**[Security Frameworks]** Audit logging with 12-month retention (ECC 2-12-3)...
```

4. Synthesizes across brains — finds structural parallels
5. Reports which brain contributed what

### Specifying a single brain

```
"Research in brain-security/: what are the MFA requirements?"
```

The agent searches only that brain.

## Cross-brain concept mapping and analytics

The concept-mapper and analytics agents need file-level access — they read entity files and claim frontmatter directly. This means they work on **local brains only**.

### Mapping two local brains

```
"Map concepts between brain/ and brain-security/"
```

The concept-mapper reads entities from both brains' `sources/*/entities/` directories and finds cross-domain connections. The agents don't change — they just receive paths from two brains instead of one.

### Running analytics across brains

```
"Run analytics across all local brains"
```

The analytics agent reads claims from all local brains and produces cross-brain reports: which brains share concepts, how argument styles differ, where knowledge overlaps.

### What about published brains?

Published brains are **query-only** — the research agent can search them via WebFetch, but concept-mapper and analytics cannot run on them directly.

**The solution: clone first, then map.**

```
Step 1: "clone brain from https://someone.github.io/their-brain/"
   → downloads claims, entities, bridges, analytics into brain-{name}/
   → adds to brains.yaml as type: local

Step 2: "Map concepts between brain/ and brain-{name}/"
   → works because both are now local files
```

The clone won't have chunks (copyrighted source text stays with the publisher), but it has everything the concept-mapper and analytics agents need.

### Agent capabilities by brain type

| Agent | Local brain | Published brain | Cloned brain |
|---|---|---|---|
| **Research** | Full search (Grep + Read) | WebFetch query (agent.json → pages) | Full search |
| **Concept-mapper** | Full mapping | Cannot (no file access) | Full mapping |
| **Analytics** | Full analysis | Cannot (no file access) | Full analysis |
| **Bridge-builder** | Full bridging | Cannot | Full bridging |
| **Verify** | Full (if chunks present) | Cannot | Cannot (no chunks) |

**Rule of thumb:** If you just want to ask questions → add as published. If you want to deeply analyze and connect → clone it first.

## Brain types

| Type | How it works | Research | Map & Analyze | Verify |
|---|---|---|---|---|
| **local** | Files on disk | Full | Full | Yes (if chunks) |
| **published** | URL + agent.json | WebFetch query | Clone first | No |
| **cloned** | Downloaded from published | Full | Full | No (no chunks) |

## Sharing your brain

To make your brain available to others:

1. Publish with Quartz: `"publish my brain"`
2. This generates a static site + `agent.json` manifest
3. Share the URL — anyone can add it to their `brains.yaml`
4. They can query it via research agent, or clone it to run concept-mapper/analytics

Published brains don't include `chunks/` — your copyrighted source material stays private. The claims, entities, bridges, and analytics are what gets shared.

## Use cases for multiple brains

- **Personal + professional:** One brain for books you read, another for work-related regulatory documents
- **Team knowledge:** Each team member publishes their brain, everyone clones each other's for cross-brain mapping
- **Domain separation:** Keep Islamic studies, computer science, and business in separate brains that can still cross-reference
- **Before/after:** Clone someone's brain, add your own sources, run concept-mapper to see what your additions connect to
- **Collaborative research:** Two researchers each build a brain on related topics, clone each other's, run analytics to find where their knowledge overlaps and diverges
