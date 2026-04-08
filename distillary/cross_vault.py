"""Cross-vault operations: combine vaults, map concepts, build bridges.

Creates a combined vault from multiple book vaults with:
- Merged notes from all books
- Bridge entity notes for same-concept-different-name pairs
- Cross-references between original entities and bridges
- Analytics (comparison, entity mapping, graph, stats)
"""

from __future__ import annotations

import logging
import os
import re
import shutil
from pathlib import Path

import yaml

log = logging.getLogger(__name__)

_WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")


def combine_vaults(
    vault_dirs: list[str | Path],
    output_dir: str | Path,
    concept_pairs: list[dict] | None = None,
) -> dict:
    """Combine multiple vaults into one with cross-references.

    Args:
        vault_dirs: paths to source vaults
        output_dir: path for combined vault
        concept_pairs: list of {"ls": "name", "mt": "name", "merged": "name",
                       "description": "..."} dicts for same-concept mapping.
                       If None, skips bridge creation.

    Returns stats dict.
    """
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    # 1. Copy all notes from all vaults
    copied = 0
    seen_stems: set[str] = set()
    for vault in vault_dirs:
        vault = Path(vault)
        for root, dirs, files in os.walk(vault):
            if ".obsidian" in root:
                continue
            rel = os.path.relpath(root, vault)
            dest_dir = output / rel
            dest_dir.mkdir(parents=True, exist_ok=True)
            for f in files:
                if f.startswith("_") or f.endswith(".base"):
                    continue
                stem = f[:-3] if f.endswith(".md") else f
                if stem in seen_stems:
                    continue  # skip collisions (first vault wins)
                seen_stems.add(stem)
                shutil.copy2(os.path.join(root, f), dest_dir / f)
                copied += 1

    log.info("Combined %d files from %d vaults", copied, len(vault_dirs))

    # 2. Build bridge notes for concept pairs
    bridges = 0
    if concept_pairs:
        bridges = _build_bridges(output, concept_pairs)

    # 3. Write CSS
    snippets = output / ".obsidian" / "snippets"
    snippets.mkdir(parents=True, exist_ok=True)
    (snippets / "distillary-tags.css").write_text(_CSS, encoding="utf-8")

    return {"copied": copied, "bridges": bridges}


def _build_bridges(vault: Path, pairs: list[dict]) -> int:
    """Create bridge entity notes and cross-references."""
    created = 0
    alias_map: dict[str, str] = {}

    for pair in pairs:
        names = [pair.get("ls"), pair.get("mt")]
        names = [n for n in names if n]
        merged = pair.get("merged")
        desc = pair.get("description", "")

        if not merged or not names:
            continue

        # Collect aliases from originals
        all_aliases: set[str] = set(names)
        for name in names:
            for md in vault.rglob(f"{name}.md"):
                text = md.read_text(encoding="utf-8")
                parts = text.split("---", 2)
                if len(parts) >= 3:
                    try:
                        meta = yaml.safe_load(parts[1])
                        if isinstance(meta, dict):
                            for a in meta.get("aliases", []):
                                if a:
                                    all_aliases.add(str(a))
                    except:
                        pass
        all_aliases.discard(merged)

        # Collect backlinks from both originals
        refs_by_source: dict[str, list[str]] = {}
        for name in names:
            refs = []
            for md in vault.rglob("*.md"):
                if ".obsidian" in str(md):
                    continue
                text = md.read_text(encoding="utf-8")
                if f"[[{name}]]" in text and md.stem != name:
                    source = "lean-startup" if "ries" in text.lower() else "mom-test"
                    refs.append(md.stem)
            refs_by_source[name] = refs

        # Read original descriptions
        perspectives = []
        for name in names:
            for md in vault.rglob(f"{name}.md"):
                text = md.read_text(encoding="utf-8")
                parts = text.split("---", 2)
                if len(parts) >= 3:
                    body = parts[2].strip().split("\n## ")[0].strip()
                    if body:
                        perspectives.append((name, body))

        # Write bridge note
        aliases_yaml = "\n".join(f"  - {a}" for a in sorted(all_aliases))
        body_parts = [desc, ""]
        for name, perspective in perspectives:
            body_parts.append(f"**[[{name}]]**: {perspective}")
            body_parts.append("")

        for name, refs in refs_by_source.items():
            if refs:
                body_parts.append(f"## Referenced by — [[{name}]]")
                body_parts.append("")
                for r in sorted(set(refs)):
                    body_parts.append(f"- [[{r}]]")
                body_parts.append("")

        content = f"""---
tags:
  - type/entity/concept
  - priority/core
  - certainty/established
  - domain/validation
  - source/cross-vault
kind: entity
entity_type: concept
aliases:
{aliases_yaml}
---

{"".join(line + chr(10) for line in body_parts)}
"""
        path = vault / "entities" / "concepts" / f"{merged}.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        created += 1

        # Track aliases for cross-referencing
        for name in names:
            if name != merged:
                alias_map[name] = merged

    # Add "Cross-book concept" links to original entities
    for old_name, bridge_name in alias_map.items():
        for md in vault.rglob(f"{old_name}.md"):
            text = md.read_text(encoding="utf-8")
            if f"[[{bridge_name}]]" not in text:
                text = text.rstrip() + f"\n\n**Cross-book concept**: See [[{bridge_name}]] for how this maps across books.\n"
                md.write_text(text, encoding="utf-8")

    log.info("Built %d bridge notes, %d cross-references", created, len(alias_map))
    return created


_CSS = """\
.tag[href="#priority/core"]    { background: #E24B4A; color: white; }
.tag[href="#priority/key"]     { background: #EF9F27; color: white; }
.tag[href="#certainty/speculative"] { background: #F09595; color: #501313; }
.tag[href="#certainty/established"] { background: #97C459; color: #173404; }
.tag[href="#stance/endorsed"]  { background: #85B7EB; color: #042C53; }
.tag[href="#stance/criticized"]{ background: #F0997B; color: #4A1B0C; }
.tag[href^="#type/entity"]     { background: #D85A30; color: white; }
.tag[href="#source/cross-vault"] { background: #9B59B6; color: white; }
.internal-link.is-unresolved {
    color: #D85A30;
    opacity: 0.7;
    font-style: italic;
    text-decoration: dashed underline;
}
"""
