"""Generate agent-friendly manifest for a published brain.

The manifest (agent.json) is a lightweight entry point — it tells agents
what's in the brain and how to navigate it. Agents then walk the HTML
pages link by link, just like humans.

Optional detailed JSON indexes are available for agents that need
programmatic access to filter/search claims without walking pages.

Files generated:
  /agent.json                           — manifest: sources, structure, entry points
  /api/sources/{slug}/claims.json       — (optional) all claims for programmatic filtering
  /api/sources/{slug}/entities.json     — (optional) all entities
  /api/shared/bridge-concepts.json      — (optional) cross-source bridges
  /api/graph.json                       — (optional) full link graph
"""

from __future__ import annotations

import json
import logging
import os
import re
from pathlib import Path

import yaml

log = logging.getLogger(__name__)

_WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")


def generate_agent_index(brain_dir: str | Path, output_dir: str | Path) -> dict:
    """Generate all JSON index files for a brain vault.

    Args:
        brain_dir: path to the brain vault
        output_dir: where to write JSON files (typically the Quartz public/ dir)

    Returns stats dict.
    """
    brain = Path(brain_dir)
    out = Path(output_dir)
    stats = {"files_written": 0}

    # Load all notes
    notes = _load_all_notes(brain)

    # Identify sources
    sources = _find_sources(brain, notes)

    # Generate per-source indexes
    source_stats = {}  # slug → {claim_count, entity_count}
    folder_slugs = {}  # source_slug → folder name
    for slug, source_info in sources.items():
        folder_slug = slug
        for d in (brain / "sources").iterdir():
            if d.is_dir() and (slug in d.name or d.name in slug):
                folder_slug = d.name
                break
        folder_slugs[slug] = folder_slug

        source_notes = {}
        for s, n in notes.items():
            tags_str = " ".join(str(t) for t in n.get("tags", []))
            path = n.get("_path", "")
            if (slug in tags_str
                or n.get("source_slug") == slug
                or f"sources/{folder_slug}/" in path):
                source_notes[s] = n

        claims = [_claim_entry(s, n) for s, n in source_notes.items()
                  if n.get("kind") == "claim"]
        entities = [_entity_entry(s, n) for s, n in source_notes.items()
                    if n.get("kind") == "entity"]

        # All claims
        _write_json(out / "api" / "sources" / slug / "claims.json", {
            "source": slug, "claim_count": len(claims), "claims": claims,
        })
        stats["files_written"] += 1

        # Core claims only
        core = [c for c in claims if c["tags"].get("priority") == "core"]
        _write_json(out / "api" / "sources" / slug / "claims" / "core.json", {
            "source": slug, "claim_count": len(core), "claims": core,
        })
        stats["files_written"] += 1

        # Entities
        _write_json(out / "api" / "sources" / slug / "entities.json", {
            "source": slug, "entity_count": len(entities), "entities": entities,
        })
        stats["files_written"] += 1

        source_stats[slug] = {"claim_count": len(claims), "entity_count": len(entities)}

    # Bridge concepts — the strategic navigation shortcuts
    bridges = []
    for stem, n in notes.items():
        tags = n.get("tags", [])
        if any("cross-vault" in str(t) for t in tags):
            # Get first line of body as description
            desc = n.get("body_preview", "").split("\n")[0].strip()
            if desc.startswith("**") or not desc:
                desc = ""
            bridges.append({
                "slug": _slugify(stem),
                "name": stem,
                "aliases": [str(a) for a in n.get("aliases", []) if a],
                "description": desc,
                "url": f"/shared/concepts/{_slugify(stem)}",
            })
    _write_json(out / "api" / "shared" / "bridge-concepts.json", {
        "count": len(bridges), "bridges": bridges,
    })
    stats["files_written"] += 1

    # Graph (adjacency list)
    graph = {"nodes": [], "edges": []}
    for stem, n in notes.items():
        graph["nodes"].append({
            "id": stem,
            "kind": n.get("kind", ""),
            "layer": n.get("layer", -1),
            "source": _get_source_slug(n),
        })
        for link in n.get("links", []):
            graph["edges"].append({"source": stem, "target": link})
    _write_json(out / "api" / "graph.json", graph)
    stats["files_written"] += 1

    # Manifest (agent.json) — lightweight navigational entry point
    # Agents should walk pages link-by-link, not dump all data
    manifest = {
        "brain": {
            "description": "A Distillary knowledge brain. Navigate it like a website: "
                          "start at the index, follow links by relevance to your goal. "
                          "Each page has content + links to go deeper. "
                          "2-4 page fetches answers most questions.",
            "skill": "/static/skill.txt",
        },
        "how_to_navigate": {
            "start": "/",
            "fastest": "Start with bridge concepts below — each one is a cross-source hub "
                       "with both perspectives + all related claims in one page. "
                       "Follow backlinks from there to drill into specifics.",
            "by_source": [
                "The thesis is already in this manifest (see sources[].thesis)",
                "For main ideas: fetch sources[].main_ideas — lists all chapter-level clusters",
                "Each cluster links to ~5 structure notes — follow the one matching your topic",
                "Structure notes link to ~5 atomic claims with source references",
            ],
            "by_concept": [
                "Pick a bridge concept from the list below",
                "Fetch its page — see both sources' perspectives + all backlinks",
                "Follow backlinks to specific claims in either source",
            ],
            "comparison": "Fetch /shared/analytics/comparison for the full cross-source synthesis",
        },
        "sources": [
            {
                "slug": slug,
                "title": info.get("source_title", info.get("title", slug)),
                "author": info.get("author", ""),
                "type": info.get("type", "unknown"),
                "published": info.get("published", 0),
                "claims": source_stats.get(slug, {}).get("claim_count", 0),
                "entities": source_stats.get(slug, {}).get("entity_count", 0),
                "thesis": _get_root_thesis(notes, slug, folder_slugs.get(slug, slug)),
                "main_ideas": _get_root_url(notes, folder_slugs.get(slug, slug)),
                "root_note": _get_root_direct_url(notes, folder_slugs.get(slug, slug)),
            }
            for slug, info in sources.items()
        ],
        "bridges": bridges,
        "bulk_api": {
            "note": "Only use these if you need to filter/search programmatically. "
                    "For most questions, walking pages is faster and uses less context.",
            "endpoints": [
                f"/api/sources/{slug}/claims.json" for slug in sources
            ] + [
                "/api/shared/bridge-concepts.json",
                "/api/graph.json",
            ],
        },
    }
    _write_json(out / "agent.json", manifest)
    stats["files_written"] += 1

    log.info("generate_agent_index: %d files written to %s", stats["files_written"], out)
    return stats


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _load_all_notes(brain: Path) -> dict[str, dict]:
    """Load all .md files into {stem: {meta fields + links}}."""
    notes = {}
    for md in brain.rglob("*.md"):
        if ".obsidian" in str(md):
            continue
        text = md.read_text(encoding="utf-8", errors="replace")
        lines = text.split("\n")
        first = second = -1
        for i, line in enumerate(lines):
            if line.strip() == "---":
                if first == -1:
                    first = i
                else:
                    second = i
                    break
            elif line.strip() and first == -1 and i > 2:
                break
        meta = {}
        body = text
        if first != -1 and second != -1:
            try:
                m = yaml.safe_load("\n".join(lines[first + 1:second]))
                if isinstance(m, dict):
                    meta = m
            except:
                pass
            body = "\n".join(lines[second + 1:])

        meta["links"] = _WIKILINK_RE.findall(text)
        meta["body_preview"] = body.strip()[:200]
        meta["_path"] = str(md.relative_to(brain))
        notes[md.stem] = meta
    return notes


def _find_sources(brain: Path, notes: dict) -> dict[str, dict]:
    """Find source metadata from _source.md files.

    Falls back to folder name as slug if source_slug field is missing.
    """
    sources = {}
    for md in brain.rglob("_source.md"):
        text = md.read_text(encoding="utf-8")
        lines = text.split("\n")
        first = second = -1
        for i, line in enumerate(lines):
            if line.strip() == "---":
                if first == -1:
                    first = i
                else:
                    second = i
                    break
        if first != -1 and second != -1:
            try:
                meta = yaml.safe_load("\n".join(lines[first + 1:second]))
                if isinstance(meta, dict):
                    # Use source_slug if present, otherwise infer from folder name
                    slug = meta.get("source_slug") or md.parent.name
                    sources[slug] = meta
            except:
                pass
    return sources


def _claim_entry(stem: str, meta: dict) -> dict:
    return {
        "slug": _slugify(stem),
        "title": stem,
        "proposition": meta.get("proposition", ""),
        "layer": meta.get("layer", 0),
        "source_ref": meta.get("source_ref", ""),
        "tags": _extract_tag_dims(meta.get("tags", [])),
        "parent": _first_parent(meta.get("body_preview", "")),
        "entities": [l for l in meta.get("links", [])],
    }


def _entity_entry(stem: str, meta: dict) -> dict:
    return {
        "slug": _slugify(stem),
        "title": stem,
        "entity_type": meta.get("entity_type", "concept"),
        "aliases": meta.get("aliases", []),
        "description": meta.get("body_preview", "")[:200],
    }


def _extract_tag_dims(tags: list) -> dict:
    dims = {}
    for t in tags:
        t = str(t)
        for dim in ["priority", "certainty", "stance", "domain", "role"]:
            if t.startswith(f"{dim}/"):
                dims[dim] = t.split("/", 1)[1]
    return dims


def _first_parent(body: str) -> str:
    m = re.search(r"Parent:\s*\[\[([^\]]+)\]\]", body)
    return m.group(1) if m else ""


def _get_source_slug(meta: dict) -> str:
    for t in meta.get("tags", []):
        t = str(t)
        if t.startswith("source/") and t != "source/cross-vault":
            return t.split("/", 1)[1]
    return meta.get("source_slug", "")


def _slugify(title: str) -> str:
    s = title.lower().strip()
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"[\s]+", "-", s)
    return s[:100]


def _get_root_thesis(notes: dict, source_slug: str, folder_slug: str) -> str:
    """Get the root note's proposition for a source."""
    for stem, n in notes.items():
        if n.get("layer") == 3 and folder_slug in n.get("_path", ""):
            return str(n.get("proposition", stem))[:200]
    return ""


def _get_root_url(notes: dict, folder_slug: str) -> str:
    """Get the URL path to a source's root note.

    Returns the clusters folder as the primary URL — it's reliable and
    shows all main ideas. The direct root note URL is provided as
    root_direct for agents that want the thesis page specifically.
    """
    return f"/sources/{folder_slug}/claims/clusters/"


def _get_root_direct_url(notes: dict, folder_slug: str) -> str:
    """Get direct URL to the root note (may have special chars in slug)."""
    for stem, n in notes.items():
        if n.get("layer") == 3 and folder_slug in n.get("_path", ""):
            path = n.get("_path", "").replace(".md", "")
            # Quartz uses the filename directly, replacing spaces with dashes
            slug = path.replace(" ", "-")
            return "/" + slug
    return ""


def _write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
