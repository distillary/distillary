"""Doctor agent — fix issues and suggest explorations.

Runs after vault assembly. Fixes mechanical problems, discovers
ghost concepts, flags potential tensions, writes _suggestions.md.
"""

from __future__ import annotations

import logging
import re
from collections import Counter
from pathlib import Path

import yaml

log = logging.getLogger(__name__)

_WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")


def doctor(vault_dir: str | Path) -> dict:
    """Fix issues and generate suggestions for a vault.

    Fixes (mechanical):
      - Ghost wikilinks: numbered prefixes + fuzzy mismatches
      - Orphan atoms: assigns them to nearest parent by domain tag
      - Missing propositions: generates from title

    Discovers:
      - Ghost concepts: phrases in 3+ claims without entity notes
      - Over-extracted entities: referenced by only 1 claim
      - Orphans that couldn't be auto-fixed

    Writes _suggestions.md with actionable exploration ideas.

    Returns stats dict.
    """
    vault = Path(vault_dir)
    stats = {"fixes": 0, "ghosts_created": 0, "suggestions": 0}

    # --- FIX GHOST WIKILINKS FIRST ---
    from distillary.vault_ops import fix_ghost_links
    ghost_stats = fix_ghost_links(vault_dir)
    stats["fixes"] += ghost_stats.get("ghosts_fixed", 0)

    # Load all notes
    notes = _load_vault(vault)

    # --- FIXES ---

    # 1. Fix missing propositions (generate from title)
    for stem, data in notes.items():
        meta = data["meta"]
        if meta.get("kind") == "claim" and "proposition" not in meta:
            # Derive proposition from title: lowercase, strip filler
            prop = stem.lower()
            for prefix in ["the ", "a ", "an "]:
                if prop.startswith(prefix):
                    prop = prop[len(prefix):]
            meta["proposition"] = prop
            _write_meta(data["path"], meta, data["body"])
            stats["fixes"] += 1

    # 2. Fix orphan atoms: find nearest parent by shared domain tag
    entity_stems = {s for s, d in notes.items() if d["meta"].get("kind") == "entity"}
    claim_stems = {s for s, d in notes.items() if d["meta"].get("kind") == "claim"}

    # Find notes that nothing links to (excluding entities and structure notes)
    linked_to = Counter()
    for stem, data in notes.items():
        for link in _WIKILINK_RE.findall(data["body"]):
            linked_to[link] += 1

    orphan_atoms = []
    for stem, data in notes.items():
        if data["meta"].get("kind") != "claim":
            continue
        if data["meta"].get("layer", 0) != 0:
            continue
        if linked_to.get(stem, 0) == 0 and "Parent:" not in data["body"]:
            orphan_atoms.append(stem)

    # Try to assign orphans to a parent with matching domain
    l1_parents = {
        s: d for s, d in notes.items()
        if d["meta"].get("kind") == "claim" and d["meta"].get("layer") == 1
    }

    fixed_orphans = []
    remaining_orphans = []
    for orphan in orphan_atoms:
        orphan_tags = set(notes[orphan]["meta"].get("tags", []))
        orphan_domains = {t for t in orphan_tags if t.startswith("domain/")}

        best_parent = None
        best_overlap = 0
        for parent_stem, parent_data in l1_parents.items():
            parent_tags = set(parent_data["meta"].get("tags", []))
            parent_domains = {t for t in parent_tags if t.startswith("domain/")}
            overlap = len(orphan_domains & parent_domains)
            if overlap > best_overlap:
                best_overlap = overlap
                best_parent = parent_stem

        if best_parent:
            # Add Parent: line to orphan
            data = notes[orphan]
            if "Parent:" not in data["body"]:
                data["body"] = data["body"].rstrip() + f"\n\nParent: [[{best_parent}]]"
                _write_body(data["path"], data["body"])
                fixed_orphans.append((orphan, best_parent))
                stats["fixes"] += 1
        else:
            remaining_orphans.append(orphan)

    # --- DISCOVER ---

    # 3. Find ghost concepts: words/phrases in 3+ claims that aren't entity notes
    # Count all wikilink targets across claims
    link_counts = Counter()
    for stem, data in notes.items():
        if data["meta"].get("kind") != "claim":
            continue
        for link in _WIKILINK_RE.findall(data["body"]):
            link_counts[link] += 1

    # Ghost = linked 3+ times but no file exists
    all_stems = set(notes.keys())
    ghosts = []
    for link, count in link_counts.most_common():
        if link not in all_stems and count >= 3:
            ghosts.append((link, count))

    # Also find frequently mentioned plain-text concepts without entity notes
    # (scan body text for capitalized phrases that repeat)
    phrase_counts = Counter()
    for stem, data in notes.items():
        if data["meta"].get("kind") != "claim":
            continue
        body = data["body"]
        # Remove existing wikilinks before scanning
        clean = _WIKILINK_RE.sub("", body)
        # Find capitalized multi-word phrases (2-4 words)
        for match in re.finditer(r"\b([A-Z][a-z]+(?: [A-Z][a-z]+){1,3})\b", clean):
            phrase = match.group(1)
            if phrase not in all_stems and phrase not in entity_stems:
                phrase_counts[phrase] += 1

    discovered_concepts = []
    for phrase, count in phrase_counts.most_common():
        if count >= 3 and not any(phrase.lower() in g[0].lower() for g in ghosts):
            discovered_concepts.append((phrase, count))
            if len(discovered_concepts) >= 15:
                break

    # Create ghost notes for discovered concepts
    for concept, count in discovered_concepts[:10]:
        ghost_path = vault / "entities" / "concepts" / f"{_safe_filename(concept)}.md"
        if ghost_path.exists():
            continue
        ghost_path.parent.mkdir(parents=True, exist_ok=True)
        content = f"""---
tags:
  - type/entity/concept
  - priority/support
  - certainty/established
kind: entity
entity_type: concept
---

Ghost concept discovered by doctor agent. Mentioned in {count} claims.
Promote this note by adding a proper description.
"""
        ghost_path.write_text(content, encoding="utf-8")
        stats["ghosts_created"] += 1

    # 4. Find over-extracted entities (referenced by only 1 claim)
    over_extracted = []
    for stem in entity_stems:
        if linked_to.get(stem, 0) <= 1:
            over_extracted.append(stem)

    # --- WRITE _suggestions.md ---

    suggestions = []

    if ghosts:
        suggestions.append("## Ghost concepts to explore\n")
        suggestions.append("These concepts appear in multiple claims but have no dedicated note.\n")
        for link, count in ghosts[:15]:
            suggestions.append(f"- [[{link}]] ({count} mentions)")
        suggestions.append("")

    if discovered_concepts:
        suggestions.append("## Discovered concepts\n")
        suggestions.append("Frequently mentioned phrases that could become entity notes.\n")
        for phrase, count in discovered_concepts[:15]:
            suggestions.append(f"- [[{phrase}]] ({count} mentions)")
        suggestions.append("")

    if remaining_orphans:
        suggestions.append("## Orphan notes\n")
        suggestions.append("These claims aren't linked to any parent note.\n")
        for orphan in remaining_orphans[:20]:
            suggestions.append(f"- [[{orphan}]]")
        suggestions.append("")

    if fixed_orphans:
        suggestions.append("## Auto-fixed orphans\n")
        suggestions.append("These claims were automatically assigned to the nearest matching parent.\n")
        for orphan, parent in fixed_orphans[:20]:
            suggestions.append(f"- [[{orphan}]] → [[{parent}]]")
        suggestions.append("")

    if over_extracted:
        suggestions.append("## Potentially over-extracted entities\n")
        suggestions.append("These entities are referenced by 0-1 claims. Consider merging or removing.\n")
        for stem in over_extracted[:15]:
            suggestions.append(f"- [[{stem}]]")
        suggestions.append("")

    # Stats section
    suggestions.insert(0, "# Vault Suggestions\n")
    suggestions.insert(1, f"*Generated by doctor agent*\n")
    suggestions.insert(2, f"**{stats['fixes']}** fixes applied | "
                         f"**{stats['ghosts_created']}** ghost notes created | "
                         f"**{len(ghosts)}** frontier concepts | "
                         f"**{len(remaining_orphans)}** remaining orphans\n")
    suggestions.insert(3, "---\n")

    stats["suggestions"] = len(ghosts) + len(discovered_concepts) + len(remaining_orphans)

    sug_path = vault / "_suggestions.md"
    sug_path.write_text("\n".join(suggestions), encoding="utf-8")
    log.info("doctor: %d fixes, %d ghosts, %d suggestions → %s",
             stats["fixes"], stats["ghosts_created"], stats["suggestions"], sug_path)

    return stats


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _split_frontmatter(content: str) -> tuple[str | None, str]:
    """Split on standalone --- lines, not table |---|---| separators."""
    lines = content.split("\n")
    first = second = -1
    for i, line in enumerate(lines):
        if line.strip() == "---":
            if first == -1:
                first = i
            else:
                second = i
                break
        elif line.strip() and first == -1 and i > 2:
            return None, content
    if first == -1 or second == -1:
        return None, content
    return "\n".join(lines[first+1:second]), "\n".join(lines[second+1:])


def _load_vault(vault: Path) -> dict[str, dict]:
    """Load all .md files into {stem: {meta, body, path}}."""
    notes = {}
    for md in vault.rglob("*.md"):
        if ".obsidian" in str(md):
            continue
        text = md.read_text(encoding="utf-8", errors="replace")
        fm, body = _split_frontmatter(text)
        if fm:
            try:
                meta = yaml.safe_load(fm) or {}
            except yaml.YAMLError:
                meta = {}
        else:
            meta = {}
            body = text
        notes[md.stem] = {"meta": meta, "body": body, "path": md}
    return notes


def _write_meta(path: Path, meta: dict, body: str) -> None:
    """Rewrite a note with updated meta."""
    frontmatter = yaml.dump(meta, default_flow_style=False,
                            allow_unicode=True, sort_keys=False).strip()
    path.write_text(f"---\n{frontmatter}\n---\n{body}", encoding="utf-8")


def _write_body(path: Path, new_body: str) -> None:
    """Rewrite just the body, preserving frontmatter."""
    text = path.read_text(encoding="utf-8")
    fm, _ = _split_frontmatter(text)
    if fm:
        path.write_text(f"---\n{fm}\n---\n{new_body}", encoding="utf-8")
    else:
        path.write_text(new_body, encoding="utf-8")


def _safe_filename(title: str) -> str:
    for ch in r'<>:"/\|?*':
        title = title.replace(ch, "")
    title = title.replace("/", "-")
    return title.strip()[:200]
