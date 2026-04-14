---
name: distillary-brains
description: Manage connected brains. Add, remove, list available brains. Triggers on "add brain", "connect brain", "list brains", "remove brain", "show brains".
---

# Distillary Brains — Connect Multiple Knowledge Vaults

Manage the collection of brains available for research, comparison, and cross-brain queries.

## Configuration

All brains are listed in `brains.yaml` at the project root.

## Commands

### List brains

Read `brains.yaml` and show all connected brains with their status:

```
Name              | Type      | Path                           | Sources | Status
Islamic Knowledge | local     | brain/                         | 3       | available
Security          | local     | brain-security/                | 8       | available
Philosophy        | published | https://user.github.io/brain/  | -       | reachable/unreachable
```

For local brains: count sources in `{path}/sources/` and verify the path exists.
For published brains: check if `{path}/agent.json` is reachable via WebFetch.

### Add a local brain

```
User: "add brain at /path/to/brain-philosophy"
```

1. Verify the path exists and contains `sources/`
2. Read `_index.md` for description (if present)
3. Count sources
4. Add entry to `brains.yaml`:

```yaml
  - name: "[ask user or derive from _index.md]"
    path: "/path/to/brain-philosophy/"
    type: local
    description: "[from _index.md or ask user]"
```

### Add a published brain

```
User: "add brain at https://someone.github.io/their-brain/"
```

1. Fetch `{url}/agent.json` via WebFetch
2. Read the manifest: sources, bridges, description
3. Add entry to `brains.yaml`:

```yaml
  - name: "[from agent.json]"
    path: "https://someone.github.io/their-brain/"
    type: published
    description: "[from agent.json]"
```

### Clone a published brain locally

```
User: "clone brain from https://someone.github.io/their-brain/"
```

1. Fetch `agent.json` for the manifest
2. Create a local directory: `brain-{name}/`
3. Fetch key pages: `_index.md`, all source indexes, bridge concepts, analytics
4. Save locally
5. Add to `brains.yaml` as type: local

This gives you a local copy for offline research. Note: published brains don't include chunks (copyrighted source text stays with the publisher).

### Remove a brain

```
User: "remove brain Philosophy"
```

1. Find the entry in `brains.yaml` by name
2. Remove it
3. Do NOT delete the brain directory — just disconnect it

## How agents use brains.yaml

### Research agent

When no specific brain path is given, the research agent reads `brains.yaml` and searches all local brains. It prefixes findings with the brain name:

```
**[Islamic Knowledge]** The concept of التقوى appears in 5 claims...
**[Security Frameworks]** Access control requirements span 4 frameworks...
```

For published brains, it uses the retrieval skill (WebFetch + agent.json) to query them.

### Cross-brain research

The most powerful feature: asking a question that spans multiple brains.

```
"How does the concept of accountability appear across Islamic ethics and cybersecurity regulation?"
```

The research agent searches both brains, finds bridge-worthy connections, and synthesizes. The Islamic brain has claims about accountability before God (المحاسبة); the security brain has claims about audit trails and compliance enforcement. The research agent finds the structural parallel.

### Concept mapping across brains

The concept-mapper and analytics agents work on **local brains only** (they need file access). The agents themselves don't change — you just give them paths from multiple brains.

```
"Map concepts between brain/ and brain-security/"
```

What happens:
1. Read `brains.yaml` → get paths for both brains
2. Launch concept-mapper with: "Read entities from `brain/sources/*/entities/` AND `brain-security/sources/*/entities/`"
3. The mapper runs normally — it reads from two directories instead of one
4. Output goes to a shared cross-brain directory

Same for analytics:
```
"Run analytics across all brains"
```
The analytics agent reads claims from all local brains' `sources/` directories and produces cross-brain reports.

### Published brains: clone first, then map

Published brains (type: `published`) are **query-only** — the research agent can search them via WebFetch, but concept-mapper and analytics cannot. They need file-level access.

To run concept-mapper or analytics on a published brain:

```
Step 1: "clone brain from https://someone.github.io/their-brain/"
   → downloads entity pages, claim indexes, bridges, analytics into brain-{name}/
   → adds to brains.yaml as type: local

Step 2: "Map concepts between brain/ and brain-{name}/"
   → now works because both are local
```

The clone won't have chunks (copyrighted source text stays with the publisher), but it has everything the concept-mapper and analytics agents need: claims, entities, and bridge concepts.

| Agent | Local brain | Published brain | Cloned brain |
|---|---|---|---|
| Research | Full search | WebFetch query | Full search |
| Concept-mapper | Full mapping | Cannot (no file access) | Full mapping |
| Analytics | Full analysis | Cannot (no file access) | Full analysis |
| Verify | Full (if chunks) | Cannot | Cannot (no chunks) |
