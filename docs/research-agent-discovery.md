# Agent Discovery: Making a Published Brain as Usable as a CLI

## The core analogy

A CLI tool works for agents because of three properties:

1. **Single-entry discovery.** `tool --help` returns everything the tool can do. One fetch, full picture.
2. **Predictable grammar.** `tool <noun> <verb> --flag` means an agent can construct valid commands without examples.
3. **Machine-readable output.** `--format json` means the agent can parse results without scraping HTML.

An MCP server breaks all three. Discovery requires protocol negotiation (JSON-RPC handshake, capability listing). Grammar is schema-driven but schema must be fetched per-tool. Output is structured but wrapped in protocol framing. The setup cost before first useful action is 3-5 round trips.

A published brain (Quartz static site) currently sits between these extremes. It has human-friendly pages. It has a `sitemap.xml` and a `static/contentIndex.json` (Quartz generates both). But neither is designed for an agent that wants to answer a specific question against the brain's knowledge.

The goal: make the published brain closer to CLI than to MCP. One fetch to understand the brain. Predictable URLs to drill into anything. Machine-readable responses at every level.

---

## What Quartz already gives us

Quartz generates three machine-readable artifacts:

| Artifact | Path | What's in it |
|---|---|---|
| Site map | `/sitemap.xml` | Every page URL + last-modified date |
| RSS feed | `/index.xml` | Last N pages with descriptions |
| Content index | `/static/contentIndex.json` | Every page: slug, title, tags, links, full text |

`contentIndex.json` is the most useful. It contains the full text of every note. But it has problems for agent use:

- **It's a single monolithic blob.** For a brain with 400+ notes, this is hundreds of KB. An agent that wants one claim downloads everything.
- **No semantic structure.** Tags and links are flat arrays. There's no distinction between "this is a claim atom" and "this is an entity" and "this is an analytics page" -- you'd have to parse tags to figure that out.
- **No query capability.** You can't ask "give me all claims tagged `priority/core`" without downloading the whole index and filtering client-side.

---

## Proposed design: the brain manifest

### 1. The help page: `/agent.json`

This is the equivalent of `--help`. One file. An agent fetches this first and knows everything about the brain's structure, contents, and URL patterns.

```json
{
  "brain": {
    "name": "Distillary Knowledge Brain",
    "version": "1.0.0",
    "description": "Distilled knowledge from books, articles, and other sources. Claims are atomic propositions extracted from sources, organized in a hierarchy (atoms → clusters → structure → thesis). Entities are named concepts, people, companies, and places referenced by claims.",
    "generated": "2026-04-07T12:00:00Z",
    "generator": "distillary v0.4.0"
  },

  "sources": [
    {
      "slug": "lean-startup",
      "title": "The Lean Startup",
      "author": "Eric Ries",
      "type": "book",
      "published": 2011,
      "claim_count": 302,
      "entity_count": 72,
      "thesis": "The Lean Startup method engineers sustainable businesses by replacing planning with iterative validated learning under uncertainty"
    },
    {
      "slug": "mom-test",
      "title": "The Mom Test",
      "author": "Rob Fitzpatrick",
      "type": "book",
      "published": 2013,
      "claim_count": 118,
      "entity_count": 81,
      "thesis": "Customer conversations that produce trustworthy learning require methodology that overrides human social defaults at every stage"
    }
  ],

  "cross_source": {
    "bridge_concepts": 11,
    "shared_claim_pairs": 24,
    "analytics": ["comparison", "entity-mapping", "graph-analytics", "statistical-profiles", "set-operations"]
  },

  "taxonomy": {
    "claim_layers": {
      "0": {"name": "atom", "description": "Single falsifiable proposition from the source text"},
      "1": {"name": "cluster", "description": "Group of related atoms that form a coherent argument"},
      "2": {"name": "structure", "description": "High-level organizational claim that frames a section"},
      "3": {"name": "thesis", "description": "Top-level claim that captures the source's central argument"}
    },
    "entity_types": ["concept", "person", "company", "place", "work"],
    "tag_dimensions": {
      "priority": ["core", "key", "support", "aside"],
      "certainty": ["established", "endorsed", "argued", "speculative"],
      "stance": ["endorsed", "neutral", "criticized"],
      "domain": "open vocabulary (methodology, strategy, measurement, ...)",
      "role": "open vocabulary (argument, definition, methodology, example, ...)"
    }
  },

  "urls": {
    "pattern": "All URLs are relative to the site root. Slugs are kebab-case.",
    "templates": {
      "source_index":      "/sources/{source_slug}/",
      "claim_atom":        "/sources/{source_slug}/claims/atoms/{claim_slug}",
      "claim_cluster":     "/sources/{source_slug}/claims/clusters/{claim_slug}",
      "claim_structure":   "/sources/{source_slug}/claims/structure/{claim_slug}",
      "entity":            "/sources/{source_slug}/entities/{entity_type}/{entity_slug}",
      "bridge_concept":    "/shared/concepts/{concept_slug}",
      "analytics":         "/shared/analytics/{report_slug}",
      "agent_index":       "/api/sources/{source_slug}/claims.json",
      "agent_entities":    "/api/sources/{source_slug}/entities.json",
      "agent_search":      "/api/search.json?q={query}"
    }
  },

  "api": {
    "description": "Static JSON files generated at build time. No server required.",
    "endpoints": [
      {"path": "/agent.json", "description": "This file. Brain manifest and discovery."},
      {"path": "/api/sources/{slug}/claims.json", "description": "All claims for a source with frontmatter, proposition, layer, tags, and parent/child links."},
      {"path": "/api/sources/{slug}/entities.json", "description": "All entities for a source with type, description, and back-references."},
      {"path": "/api/sources/{slug}/claims/core.json", "description": "Only priority/core claims. Smallest useful subset."},
      {"path": "/api/shared/bridge-concepts.json", "description": "Cross-source concept mappings."},
      {"path": "/api/shared/analytics.json", "description": "Pre-computed analytics: graph centrality, statistical profiles, set operations."},
      {"path": "/api/graph.json", "description": "Full link graph as adjacency list. Nodes have type and source labels."},
      {"path": "/api/search.json", "description": "Pre-built inverted index for full-text search over propositions."}
    ]
  }
}
```

Why this works like `--help`:

- An agent reads one URL and knows: what sources exist, how many claims/entities each has, the complete tag taxonomy, every URL pattern, every API endpoint.
- The `urls.templates` section is the grammar. An agent can construct any URL without crawling.
- The `api.endpoints` section tells the agent what machine-readable data is available and what each file contains.

### 2. The lightweight indexes: `/api/sources/{slug}/claims.json`

This is the equivalent of `tool list --format json`. An agent fetches this to get a structured overview of all claims without reading every page.

```json
{
  "source": "lean-startup",
  "claim_count": 302,
  "claims": [
    {
      "slug": "3d-printing-enables-small-batch-hardware",
      "title": "3D printing enables small batch hardware",
      "proposition": "3D printing and rapid prototyping enable small batch hardware at low cost",
      "layer": 0,
      "tags": {
        "priority": "key",
        "certainty": "established",
        "stance": "endorsed",
        "domain": "technology",
        "role": "argument"
      },
      "parent": "small-batch-principles-extend-beyond-software-through-converging-technologies",
      "children": [],
      "entities": ["obstacle"],
      "url": "/sources/lean-startup/claims/atoms/3d-printing-enables-small-batch-hardware"
    }
  ]
}
```

What makes this agent-friendly:

- **Filterable without fetching content.** An agent looking for `priority: core` claims can filter this list. An agent looking for claims about `domain: measurement` can filter. No need to download 302 separate pages.
- **Hierarchical navigation.** `parent` and `children` fields let an agent walk the claim tree (thesis → structure → cluster → atom) without separate requests.
- **Entity cross-references.** The `entities` array lets an agent find which entities a claim references, enabling graph traversal.

### 3. The core subset: `/api/sources/{slug}/claims/core.json`

Same format as above, but filtered to only `priority: core` claims. This is the "TL;DR" of the source. Typically 30-40 claims instead of 300. An agent that wants a quick understanding of the source reads this.

### 4. The search index: `/api/search.json`

A pre-built inverted index over propositions. Generated at build time, no server needed.

```json
{
  "index_type": "inverted",
  "token_count": 1847,
  "document_count": 420,
  "entries": {
    "validated": [
      {"slug": "validated-learning-is-the-true-measure-of-startup-progress", "source": "lean-startup", "tf": 3},
      {"slug": "validated-learning-grounded-in-empirical-data", "source": "lean-startup", "tf": 2}
    ],
    "pivot": [
      {"slug": "a-pivot-is-a-structured-hypothesis-change", "source": "lean-startup", "tf": 4},
      {"slug": "early-pivoting-preserves-resources", "source": "lean-startup", "tf": 2}
    ]
  }
}
```

This lets an agent do keyword search without downloading full text. For a brain with hundreds of notes, this saves bandwidth and latency.

### 5. The graph: `/api/graph.json`

The knowledge graph as a static adjacency list.

```json
{
  "nodes": [
    {
      "id": "lean-startup/claims/atoms/3d-printing-enables-small-batch-hardware",
      "type": "claim",
      "layer": 0,
      "source": "lean-startup",
      "title": "3D printing enables small batch hardware"
    },
    {
      "id": "lean-startup/entities/concepts/actionable-metrics",
      "type": "entity",
      "entity_type": "concept",
      "source": "lean-startup",
      "title": "Actionable Metrics"
    },
    {
      "id": "shared/concepts/validated-learning",
      "type": "bridge",
      "source": null,
      "title": "Validated Learning"
    }
  ],
  "edges": [
    {"from": "lean-startup/claims/atoms/3d-printing-enables-small-batch-hardware", "to": "lean-startup/entities/concepts/obstacle", "relation": "references"},
    {"from": "lean-startup/claims/atoms/3d-printing-enables-small-batch-hardware", "to": "lean-startup/claims/clusters/small-batch-principles", "relation": "child_of"}
  ]
}
```

An agent can traverse relationships, find clusters, discover which entities are most connected, all from a single static file.

---

## URL scheme

The predictable URL convention, analogous to CLI's `command subcommand --flag` pattern:

```
/{section}/{source_slug}/{content_type}/{sub_type}/{item_slug}
```

Concrete paths:

```
/                                          → Human landing page
/agent.json                                → Machine manifest (the --help)

/sources/lean-startup/                     → Source overview page
/sources/lean-startup/claims/atoms/        → All atom claims (folder listing)
/sources/lean-startup/claims/clusters/     → All cluster claims
/sources/lean-startup/claims/structure/    → All structural claims
/sources/lean-startup/entities/concepts/   → All concept entities
/sources/lean-startup/entities/people/     → All person entities
/sources/lean-startup/entities/companies/  → All company entities

/shared/concepts/validated-learning        → Bridge concept page
/shared/analytics/graph-analytics          → Analytics report

/api/sources/lean-startup/claims.json      → Machine-readable claim index
/api/sources/lean-startup/entities.json    → Machine-readable entity index
/api/sources/lean-startup/claims/core.json → Core claims only
/api/shared/bridge-concepts.json           → Cross-source bridges
/api/shared/analytics.json                 → All analytics data
/api/graph.json                            → Full knowledge graph
/api/search.json                           → Search index
```

The pattern is discoverable: if you know the source slug and content type, you can construct any URL. No crawling required.

---

## How this differs from an MCP server

| Dimension | Published Brain (static) | MCP Server |
|---|---|---|
| **Setup** | `fetch /agent.json` | Discover URL, negotiate protocol, authenticate, list tools |
| **First useful action** | 1 HTTP GET | 3-5 round trips minimum |
| **Infrastructure** | Static file hosting (GitHub Pages, Cloudflare Pages, any CDN) | Running server process, runtime, dependencies |
| **Query flexibility** | Pre-computed indexes; limited to what was built | Arbitrary queries; server can filter/compute on demand |
| **Cost** | Zero (static hosting is free) | Server compute costs; uptime maintenance |
| **Latency** | CDN-cached; sub-100ms globally | Server processing time; cold starts |
| **Auth** | None needed (public knowledge) | OAuth/API keys typical |
| **Update model** | Rebuild static files on content change | Real-time |
| **Failure mode** | CDN is down (rare) | Server crash, dependency failure, auth expiry |
| **Agent complexity** | HTTP GET + JSON parse | MCP client library, protocol handling, error recovery |

The key tradeoff: the static approach loses query flexibility (you can't ask "find all claims where certainty is speculative AND domain is measurement" unless that exact filter was pre-computed). But for a knowledge brain, the set of useful queries is small and predictable. Pre-computing them is cheap.

The MCP server becomes worth it when:
- The brain has 10,000+ notes and full indexes become too large to download
- You need real-time computation (e.g., running new analytics on the fly)
- You need write access (adding annotations, updating claims)
- You need authentication (private brain, paid access)

For a published knowledge brain with hundreds of notes, static wins on every dimension that matters: simplicity, cost, reliability, speed.

---

## The agent interaction pattern

Here is what an agent session looks like with this design:

```
Agent: I need to understand what this brain knows about customer validation.

Step 1: GET /agent.json
        → Learns: 2 sources, 420 total claims, URL patterns, available APIs

Step 2: GET /api/search.json (or fetch + ctrl-F for "validation" in claims.json)
        → Finds: 12 claims across both sources mention validation

Step 3: GET /api/sources/lean-startup/claims/core.json
        → Reads the 35 core claims, finds the validation cluster

Step 4: GET /sources/lean-startup/claims/clusters/the-build-measure-learn-feedback-loop-replaces-linear-planning
        → Reads the full cluster with all children and entity references

Step 5: GET /api/shared/bridge-concepts.json
        → Finds that "Validated Learning" bridges both sources, maps to different concepts in each

Total: 5 HTTP GETs. No authentication. No protocol negotiation. No server to maintain.
```

Compare to MCP:

```
Step 1: Initialize MCP connection (WebSocket or stdio)
Step 2: Send initialize request, receive capabilities
Step 3: Send tools/list, receive available tools
Step 4: Understand tool schemas, construct search call
Step 5: Send tools/call with search parameters
Step 6: Parse response, construct follow-up call
Step 7: Send tools/call for related claims
...
```

More round trips, more protocol overhead, more things that can break.

---

## The minimum viable agent interface

If you implement nothing else, implement these two files:

### 1. `/agent.json` — the manifest

Contains: source list, claim/entity counts, URL templates, taxonomy description. This is the `--help`.

### 2. `/api/sources/{slug}/claims.json` — the claim index

Contains: every claim with slug, proposition, layer, tags, parent, children, entity refs. This is `tool list --format json`.

With just these two files, an agent can:
- Discover what the brain contains
- Filter claims by any tag dimension
- Navigate the claim hierarchy
- Construct URLs to fetch full content of any claim
- Cross-reference entities

Everything else (search index, graph, core subsets, bridge concepts) is optimization. The manifest + claim indexes are the minimum viable agent interface.

---

## Implementation

This requires a Quartz plugin or a build-time script that:

1. Reads the vault content (already available during Quartz build)
2. Parses frontmatter from every note
3. Generates the JSON files and writes them to the output directory

The existing `ContentIndex` emitter plugin in Quartz (`quartz/plugins/emitters/contentIndex.tsx`) already iterates over all content and extracts frontmatter, tags, and links. A new `AgentIndex` emitter would follow the same pattern but output the structured JSON files described above instead of the monolithic `contentIndex.json`.

Alternatively, this can be a post-build step in the `fractal` Python tool: after `distillary publish` copies the vault to Quartz's content directory and runs the build, it generates the agent JSON files from the vault's markdown directly and drops them into the Quartz output directory. This avoids modifying Quartz internals.

The second approach is simpler and keeps the agent interface under fractal's control rather than coupling it to Quartz's plugin system.

---

## What this means for the fractal project

The brain already has the right structure for this. The vault layout maps directly to the URL scheme:

```
brain/sources/lean-startup/claims/atoms/    → /sources/lean-startup/claims/atoms/
brain/sources/lean-startup/entities/concepts → /sources/lean-startup/entities/concepts/
brain/shared/concepts/                       → /shared/concepts/
brain/shared/analytics/                      → /shared/analytics/
```

The frontmatter already contains the fields needed for the claim indexes (tags, kind, layer, proposition). The `_source.md` files already contain source metadata (title, author, claim count). The analytics files already contain the cross-source data.

The work is: parse what's already there, serialize it as structured JSON, and serve it alongside the static site. No new data modeling. No new extraction. Just a new output format for what already exists.
