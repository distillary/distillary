"""Vault post-processing operations: fix, reinforce-links, validate.

These operate on already-written vaults or on intermediate tmp/ results
to produce corrected vaults.
"""

from __future__ import annotations

import logging
import re
from pathlib import Path

import yaml

import difflib

from distillary.notes import Note, parse_notes, wikilinks_in

log = logging.getLogger(__name__)

_WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")


# ---------------------------------------------------------------------------
# fix_vault — assemble a complete vault from intermediate results
# ---------------------------------------------------------------------------

def fix_vault(
    tmp_dir: str | Path,
    vault_dir: str | Path,
) -> dict:
    """Assemble a complete vault from pipeline intermediate files.

    Reads:
      - deduped claims (layer-0 atoms)
      - grouped claims (layer-1 parents with children)
      - pyramid (layer-2 + root)
      - entities
      - lateral links
      - entity-linked claims

    Merges everything and writes a clean vault.
    Returns a stats dict.
    """
    tmp = Path(tmp_dir)
    vault = Path(vault_dir)
    vault.mkdir(parents=True, exist_ok=True)

    # 1. Load all note sources
    atoms = _load_notes_from_glob(tmp / "results" / "extract_*.md")
    deduped = _load_notes_from_file(tmp / "deduped_claims.md")
    pyramid = _load_notes_from_file(tmp / "results" / "pyramid.md")
    entities = _load_notes_from_file(tmp / "results" / "entities.md")
    # Fallback: try entities_v2.md if entities.md parsed poorly
    if len(entities) < 3:
        ent_v2 = _load_notes_from_file(tmp / "results" / "entities_v2.md")
        if len(ent_v2) > len(entities):
            entities = ent_v2
            log.info("Using entities_v2.md (%d entities)", len(entities))
    grouped_files = sorted(tmp.glob("results/group_*.md"))
    grouped = []
    for gf in grouped_files:
        grouped.extend(_load_notes_from_file(gf))

    log.info(
        "Loaded: %d atoms, %d deduped, %d pyramid, %d grouped, %d entities",
        len(atoms), len(deduped), len(pyramid), len(grouped), len(entities),
    )

    # 2. Build the master note index by title
    #    Priority: pyramid > grouped > deduped > atoms
    #    (pyramid has the best parent/children structure for L1+)
    by_title: dict[str, Note] = {}

    for note in atoms:
        by_title[note.title] = note
    for note in deduped:
        by_title[note.title] = note
    for note in grouped:
        by_title[note.title] = note
    for note in pyramid:
        by_title[note.title] = note
    for note in entities:
        by_title[note.title] = note

    # 3. Load lateral links and merge Related sections
    link_files = sorted(tmp.glob("results/link_*.md"))
    if link_files:
        link_notes = []
        for lf in link_files:
            link_notes.extend(_load_notes_from_file(lf))
        _merge_related_sections(by_title, link_notes)
        log.info("Merged lateral links from %d files", len(link_files))

    # 4. Load entity-linked claims and merge wikilinks into bodies
    linked_file = tmp / "results" / "linked_claims.md"
    if linked_file.exists():
        linked_notes = _load_notes_from_file(linked_file)
        _merge_entity_links(by_title, linked_notes)
        log.info("Merged entity links from %d notes", len(linked_notes))

    # 5. Fix notes with missing/malformed metadata
    for note in by_title.values():
        _normalize_note_meta(note)

    # 6. Wire parent-child hierarchy from group + pyramid files
    _wire_parent_links(by_title, tmp)

    # 7. Write all notes to vault
    all_notes = list(by_title.values())
    _write_vault_files(all_notes, vault)
    _write_css(vault)

    stats = {
        "total_notes": len(all_notes),
        "claims": len([n for n in all_notes if n.kind == "claim"]),
        "entities": len([n for n in all_notes if n.kind == "entity"]),
        "layer_0": len([n for n in all_notes if n.layer == 0]),
        "layer_1": len([n for n in all_notes if n.layer == 1]),
        "layer_2": len([n for n in all_notes if n.layer == 2]),
        "layer_3": len([n for n in all_notes if n.layer == 3]),
    }
    log.info("fix_vault complete: %s", stats)
    return stats


def _load_notes_from_file(path: Path) -> list[Note]:
    if not path.exists():
        log.warning("File not found: %s", path)
        return []
    text = path.read_text(encoding="utf-8")
    return parse_notes(text)


def _load_notes_from_glob(pattern: Path) -> list[Note]:
    parent = pattern.parent
    name = pattern.name
    notes = []
    for f in sorted(parent.glob(name)):
        notes.extend(_load_notes_from_file(f))
    return notes


def _merge_related_sections(by_title: dict[str, Note], link_notes: list[Note]) -> None:
    """Merge ## Related bullets from link_notes into the master index."""
    for ln in link_notes:
        if ln.title not in by_title:
            continue
        master = by_title[ln.title]
        # Extract Related bullets from the linked version
        new_bullets = _extract_related_bullets(ln.body)
        existing_bullets = _extract_related_bullets(master.body)
        # Add only new bullets
        added = [b for b in new_bullets if b not in existing_bullets]
        if added:
            if "## Related" not in master.body:
                master.body = master.body.rstrip() + "\n\n## Related\n"
            for bullet in added:
                master.body = master.body.rstrip() + "\n" + bullet


def _extract_related_bullets(body: str) -> list[str]:
    """Extract bullet lines from ## Related section."""
    bullets = []
    in_related = False
    for line in body.splitlines():
        if line.strip().startswith("## Related"):
            in_related = True
            continue
        if in_related and line.strip().startswith("## "):
            break
        if in_related and line.strip().startswith("- "):
            bullets.append(line.rstrip())
    return bullets


def _merge_entity_links(by_title: dict[str, Note], linked_notes: list[Note]) -> None:
    """Take entity-linked bodies and merge wikilinks into master notes."""
    for ln in linked_notes:
        if ln.title not in by_title:
            continue
        master = by_title[ln.title]
        # If the linked version has more [[wikilinks]] than the master, use it
        master_links = len(_WIKILINK_RE.findall(master.body))
        linked_links = len(_WIKILINK_RE.findall(ln.body))
        if linked_links > master_links:
            master.body = ln.body


# ---------------------------------------------------------------------------
# reinforce_links — scan vault and wikilink all known names
# ---------------------------------------------------------------------------

def reinforce_links(vault_dir: str | Path) -> dict:
    """Scan all notes in a vault. For every entity/claim title that exists
    as a file, find plain-text mentions in other notes and wrap them in
    [[wikilinks]].

    Returns stats dict.
    """
    vault = Path(vault_dir)
    notes: dict[str, tuple[str, Path]] = {}  # stem → (content, path)
    for f in _find_all_md(vault):
        notes[f.stem] = (f.read_text(encoding="utf-8"), f)

    # Build lookup: all titles + aliases → canonical title
    name_to_canonical: dict[str, str] = {}
    for stem, (content, _path) in notes.items():
        name_to_canonical[stem] = stem
        # Extract aliases from YAML
        try:
            fm_start = content.index("---") + 3
            fm_end = content.index("---", fm_start)
            meta = yaml.safe_load(content[fm_start:fm_end]) or {}
            for alias in meta.get("aliases", []):
                if alias and len(str(alias)) >= 3:
                    name_to_canonical[str(alias)] = stem
        except (ValueError, yaml.YAMLError):
            pass

    # Sort by length descending so longer names match first
    sorted_names = sorted(name_to_canonical.keys(), key=len, reverse=True)

    stats = {"files_modified": 0, "links_added": 0}

    for stem, (content, file_path) in notes.items():
        # Split into frontmatter and body — only on standalone "---" lines
        # (not on "|---|---|" table separators)
        frontmatter, body = _split_frontmatter(content)
        if frontmatter is None:
            continue
        original_body = body

        for name in sorted_names:
            canonical = name_to_canonical[name]
            # Don't link a note to itself
            if canonical == stem:
                continue
            # Skip very short names
            if len(name) < 4:
                continue
            # Skip if already wikilinked
            if f"[[{canonical}]]" in body or f"[[{name}]]" in body:
                continue
            # Find plain-text mentions NOT inside existing [[wikilinks]]
            match = _find_outside_wikilinks(body, name)
            if match:
                replacement = f"[[{canonical}]]"
                # Prevent gluing: add space if adjacent to another ]]
                if match[0] > 1 and body[match[0]-2:match[0]] == "]]":
                    replacement = " " + replacement
                body = body[:match[0]] + replacement + body[match[1]:]
                stats["links_added"] += 1

        if body != original_body:
            if frontmatter:
                new_content = f"---\n{frontmatter}\n---\n{body}"
            else:
                new_content = body  # no frontmatter (analytics files)
            file_path.write_text(new_content, encoding="utf-8")
            stats["files_modified"] += 1

    log.info("reinforce_links: %s", stats)
    return stats


# ---------------------------------------------------------------------------
# validate — vault integrity checker
# ---------------------------------------------------------------------------

def validate(vault_dir: str | Path) -> dict:
    """Run integrity checks on a vault. Returns a report dict."""
    vault = Path(vault_dir)
    report: dict = {
        "total_files": 0,
        "issues": [],
        "wikilinks_total": 0,
        "wikilinks_resolved": 0,
        "wikilinks_ghost": 0,
        "notes_with_parent": 0,
        "notes_with_children": 0,
        "notes_missing_proposition": 0,
        "layer_distribution": {},
        "tag_issues": [],
    }

    # Load all notes
    file_stems: set[str] = set()
    all_notes: dict[str, dict] = {}  # stem → {meta, body, path}

    for f in _find_all_md(vault):
        report["total_files"] += 1
        stem = f.stem
        file_stems.add(stem)
        content = f.read_text(encoding="utf-8", errors="replace")

        try:
            fm, body = _split_frontmatter(content)
            if fm:
                meta = yaml.safe_load(fm) or {}
            else:
                meta = {}
                body = content
        except yaml.YAMLError:
            meta = {}
            body = content
            report["issues"].append(f"YAML parse error: {stem}")

        all_notes[stem] = {"meta": meta, "body": body, "path": f}

    # Check layer distribution
    for stem, data in all_notes.items():
        layer = data["meta"].get("layer", "none")
        report["layer_distribution"][str(layer)] = (
            report["layer_distribution"].get(str(layer), 0) + 1
        )

    # Check wikilink resolution
    all_links: set[str] = set()
    for stem, data in all_notes.items():
        links = _WIKILINK_RE.findall(data["body"])
        for link in links:
            all_links.add(link)
            report["wikilinks_total"] += 1
            # Handle [[Title|display text]] — resolve on the part before |
            link_target = link.split("|")[0].strip() if "|" in link else link
            if link_target in file_stems:
                report["wikilinks_resolved"] += 1
            else:
                report["wikilinks_ghost"] += 1

    # Check parent/children
    for stem, data in all_notes.items():
        if "Parent:" in data["body"]:
            report["notes_with_parent"] += 1
            # Verify parent exists
            parent_links = _WIKILINK_RE.findall(
                "\n".join(
                    l for l in data["body"].splitlines()
                    if l.strip().startswith("Parent:")
                )
            )
            for pl in parent_links:
                if pl not in file_stems:
                    report["issues"].append(
                        f"Broken parent link: {stem} → [[{pl}]]"
                    )

        if "Children:" in data["body"]:
            report["notes_with_children"] += 1

    # Check proposition field (claims only)
    for stem, data in all_notes.items():
        kind = data["meta"].get("kind", "")
        if kind == "claim" and data["meta"].get("layer", 99) == 0:
            if "proposition" not in data["meta"]:
                report["notes_missing_proposition"] += 1

    # Check tag format
    valid_prefixes = {
        "type/", "priority/", "certainty/", "stance/",
        "domain/", "role/", "source/", "status/", "insight/",
    }
    for stem, data in all_notes.items():
        tags = data["meta"].get("tags") or []
        for tag in tags:
            if not any(str(tag).startswith(p) for p in valid_prefixes):
                report["tag_issues"].append(f"{stem}: unknown tag '{tag}'")

    # Summary
    resolution_pct = (
        round(100 * report["wikilinks_resolved"] / report["wikilinks_total"], 1)
        if report["wikilinks_total"] > 0
        else 0
    )
    report["wikilink_resolution_pct"] = resolution_pct

    log.info(
        "validate: %d files, %d links (%d resolved / %.1f%%), %d issues",
        report["total_files"],
        report["wikilinks_total"],
        report["wikilinks_resolved"],
        resolution_pct,
        len(report["issues"]),
    )
    return report


# ---------------------------------------------------------------------------
# Internal helpers shared with driver.py
# ---------------------------------------------------------------------------

def _write_vault_files(notes: list[Note], vault: Path) -> None:
    """Write notes into organized subfolders by kind and layer."""
    vault.mkdir(parents=True, exist_ok=True)

    for note in notes:
        safe_title = _safe_filename(note.title)
        if not safe_title:
            continue
        # If title was truncated, add full title as alias for Obsidian resolution
        if safe_title != note.title and len(note.title) > len(safe_title):
            aliases = note.meta.get("aliases", [])
            if not isinstance(aliases, list):
                aliases = [aliases] if aliases else []
            if note.title not in aliases:
                aliases.append(note.title)
                note.meta["aliases"] = aliases

        subdir = _note_subfolder(note)
        target = vault / subdir
        target.mkdir(parents=True, exist_ok=True)
        path = target / f"{safe_title}.md"

        # Sanitize meta values: remove --- from string fields
        for key in list(note.meta.keys()):
            val = note.meta[key]
            if isinstance(val, str) and "---" in val:
                note.meta[key] = val.replace(" --- ", ", ").replace("---", "")

        frontmatter = yaml.dump(
            note.meta,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
        ).strip()
        # Sanitize body: strip any leftover YAML frontmatter from agent output
        body = note.body.strip()
        # Remove leading --- (standalone or glued like ---tags:)
        while body.startswith("---"):
            # Find end of this --- prefix
            if body.startswith("---\n") or body == "---":
                body = body[3:].strip()
            else:
                # Glued: ---tags: → strip the ---
                body = body[3:].strip()
        # If body still starts with YAML keys (tags:, kind:, layer:), strip them
        body_lines = body.split("\n")
        yaml_keys = {"tags:", "kind:", "layer:", "proposition:", "source_ref:",
                     "published:", "extracted_by:", "prompt_version:", "entity_type:",
                     "aliases:", "certainty:", "source:", "- type/", "- priority/",
                     "- certainty/", "- stance/", "- domain/", "- role/", "- source/"}
        clean_start = 0
        for j, line in enumerate(body_lines):
            stripped_line = line.strip()
            if any(stripped_line.startswith(k) for k in yaml_keys) or stripped_line.startswith("- ") and "/" in stripped_line:
                clean_start = j + 1
            elif stripped_line == "":
                continue
            else:
                break
        body = "\n".join(body_lines[clean_start:]).strip()
        # Replace all --- in body (standalone or inline) with em-dash
        # Standalone --- on its own line → remove (was a section divider)
        body = re.sub(r"^---$", "", body, flags=re.MULTILINE)
        # Inline --- used as separators in prose → clean punctuation
        # Pattern: [[Link]] --- description → [[Link]], description
        body = re.sub(r"\]\]\s*---\s*", "]], ", body)
        # Pattern: word --- word → word, word (or just remove the separator)
        body = body.replace(" --- ", ", ")
        body = body.replace("---", "")
        # Fix glued wikilinks: ]][[  → ]], [[
        body = re.sub(r"\]\]\[\[", "]], [[", body)
        # Strip redundant hierarchy markers from body
        # Parent/Children are detected automatically by Obsidian via wikilinks in prose
        body = re.sub(
            r"(?:CHILD UPDATES|CHILD UPDATE|Child.Parent Assignments|Child Note Updates).*",
            "", body, flags=re.DOTALL | re.IGNORECASE,
        )
        body = re.sub(r"^Parent:\s*\[\[.*?\]\]\s*$", "", body, flags=re.MULTILINE)
        body = re.sub(r"^Children:\s*$", "", body, flags=re.MULTILINE)
        # Remove bullet lists that are just child wikilinks under a Children: header
        # Keep the ## Related section but strip the Children: subsection
        body = re.sub(r"### Children\n(?:- \[\[.*?\]\]\n)*", "", body)
        # Remove empty ## headers (nothing after them)
        body = re.sub(r"^##\s*$", "", body, flags=re.MULTILINE)
        body = re.sub(r"^## Related\s*$", "", body, flags=re.MULTILINE)
        # Clean up multiple blank lines
        body = re.sub(r"\n{3,}", "\n\n", body).strip()
        content = f"---\n{frontmatter}\n---\n\n{body}\n"
        path.write_text(content, encoding="utf-8")

    log.info("Wrote %d notes to %s", len(notes), vault)


def _write_source_index(vault: Path, notes: list) -> None:
    """Generate _index.md for a source vault with thesis, clusters, and browse paths."""
    # Find root note (layer 3)
    root_title = ""
    for n in notes:
        if n.meta.get("layer") == 3:
            root_title = n.title
            break

    # Find L2 clusters
    clusters = [(n.title, n.meta.get("proposition", "")) for n in notes if n.meta.get("layer") == 2]

    # Get source info from _source.md if it exists
    source_file = vault / "_source.md"
    title = author = published = license_info = url = description = ""
    if source_file.exists():
        text = source_file.read_text(encoding="utf-8")
        fm, body = _split_frontmatter(text)
        if fm:
            try:
                meta = yaml.safe_load(fm) or {}
                title = meta.get("title", "")
                author = meta.get("author", "")
                published = meta.get("published", "")
                license_info = meta.get("license", "")
                url = meta.get("url", "")
            except:
                pass
        description = body.strip() if body else ""

    if not title and not root_title:
        return  # nothing to write

    lines = ["---", "---", ""]
    lines.append(f"# {title or vault.name}")
    lines.append("")
    if author:
        lines.append(f"*{author} ({published}){'  —  ' + license_info if license_info else ''}*")
        lines.append("")
    if description:
        lines.append(description)
        lines.append("")

    if root_title:
        lines.append("## Thesis")
        lines.append("")
        lines.append(f"[[{root_title}]]")
        lines.append("")

    if clusters:
        lines.append("## Main ideas")
        lines.append("")
        lines.append("| Cluster | Core argument |")
        lines.append("|---|---|")
        for ctitle, prop in clusters:
            short_prop = prop[:80] + "..." if len(prop) > 80 else prop
            lines.append(f"| [[{ctitle}]] | {short_prop} |")
        lines.append("")

    # Stats
    atom_count = len([n for n in notes if n.meta.get("layer") == 0 and n.kind == "claim"])
    entity_count = len([n for n in notes if n.kind == "entity"])
    lines.append("## Browse")
    lines.append("")
    lines.append("| Path | Contents |")
    lines.append("|---|---|")
    lines.append(f"| `claims/atoms/` | {atom_count} atomic claims |")
    lines.append(f"| `claims/structure/` | Argument groups |")
    lines.append(f"| `claims/clusters/` | Chapter-level themes |")
    lines.append(f"| `entities/` | {entity_count} entities |")

    index_path = vault / "_index.md"
    index_path.write_text("\n".join(lines), encoding="utf-8")
    log.info("Wrote source index to %s", index_path)


def _note_subfolder(note: Note) -> str:
    """Determine subfolder for a note based on kind and layer."""
    if note.kind == "entity":
        etype = note.meta.get("entity_type", "concept")
        # Proper pluralization
        plural = {"person": "people", "company": "companies"}.get(etype, f"{etype}s")
        return f"entities/{plural}"
    if note.kind == "annotation":
        return "annotations"

    layer = note.meta.get("layer", 0)
    if layer == 0:
        return "claims/atoms"
    elif layer == 1:
        return "claims/structure"
    elif layer == 2:
        return "claims/clusters"
    elif layer >= 3:
        return "claims"
    return "claims/atoms"


def _write_css(vault: Path) -> None:
    snippets_dir = vault / ".obsidian" / "snippets"
    snippets_dir.mkdir(parents=True, exist_ok=True)
    css = """\
/* Tag colors in note bodies */
.tag[href="#priority/core"]    { background: #E24B4A; color: white; }
.tag[href="#priority/key"]     { background: #EF9F27; color: white; }
.tag[href="#certainty/speculative"] { background: #F09595; color: #501313; }
.tag[href="#certainty/established"] { background: #97C459; color: #173404; }
.tag[href="#stance/endorsed"]  { background: #85B7EB; color: #042C53; }
.tag[href="#stance/criticized"]{ background: #F0997B; color: #4A1B0C; }
.tag[href^="#type/entity"]     { background: #D85A30; color: white; }

/* Ghost links in note bodies — italic and faded */
.internal-link.is-unresolved {
    color: #D85A30;
    opacity: 0.7;
    font-style: italic;
    text-decoration: dashed underline;
}
"""
    (snippets_dir / "distillary-tags.css").write_text(css, encoding="utf-8")


# ---------------------------------------------------------------------------
# write_index — create vault entry point
# ---------------------------------------------------------------------------

def write_index(
    vault_dir: str | Path,
    book_title: str,
    author: str,
    published: int,
) -> None:
    """Write _index.md as the vault entry point."""
    vault = Path(vault_dir)

    # Find root note
    root_title = None
    root_body = ""
    l2_titles = []

    for md in _find_all_md(vault):
        text = md.read_text(encoding="utf-8")
        if "type/claim/index" in text:
            root_title = md.stem
            # Extract L2 links from root
            body_start = text.find("---", 3)
            if body_start != -1:
                root_body = text[body_start + 3:]
                l2_titles = _WIKILINK_RE.findall(root_body)

    # Count stats
    total = claims = entities = atoms = 0
    for md in _find_all_md(vault):
        total += 1
        text = md.read_text(encoding="utf-8")
        if "kind: claim" in text:
            claims += 1
        if "kind: entity" in text:
            entities += 1
        if "layer: 0" in text:
            atoms += 1

    # Build index
    lines = [
        f"# {book_title}",
        f"*by {author} ({published})*",
        "",
        f"**{total}** notes | **{claims}** claims | **{entities}** entities | **{atoms}** atomic claims",
        "",
        "---",
        "",
        "## Start here",
        "",
    ]

    if root_title:
        lines.append(f"**Root thesis:** [[{root_title}]]")
        lines.append("")

    # Filter outline to only L2 claim notes (not entities)
    l2_claims = []
    for title in l2_titles:
        # Check if this is a claim with layer >= 2
        for md in _find_all_md(vault):
            if md.stem == title:
                text = md.read_text(encoding="utf-8")
                if "kind: claim" in text and ("layer: 2" in text or "layer: 3" in text):
                    l2_claims.append(title)
                break

    if l2_claims:
        lines.append("## Book outline")
        lines.append("")
        for i, title in enumerate(l2_claims, 1):
            lines.append(f"{i}. [[{title}]]")
        lines.append("")

    lines.extend([
        "## Browse by type",
        "",
        "| Folder | Contents |",
        "|---|---|",
        "| `claims/` | Root thesis + cluster summaries |",
        "| `claims/clusters/` | Chapter-level argument groups |",
        "| `claims/structure/` | Mid-level argument summaries |",
        "| `claims/atoms/` | Individual atomic claims |",
        "| `entities/` | People, concepts, companies, works |",
        "",
        "## Graph view filters",
        "",
        "| What you want | Filter |",
        "|---|---|",
        "| Book in 30 seconds | `tag:#priority/core` |",
        "| What the author advocates | `tag:#stance/endorsed AND tag:#priority/key` |",
        "| What to fact-check | `tag:#certainty/speculative` |",
        "| Just the people | `tag:#type/entity/person` |",
        "| The frontier (unexplored concepts) | Toggle 'Existing files only' OFF |",
        "",
    ])

    index_path = vault / "_index.md"
    index_path.write_text("\n".join(lines), encoding="utf-8")
    log.info("Wrote index to %s", index_path)


# ---------------------------------------------------------------------------
# build_entity_hubs — add "Referenced by" sections to entity notes
# ---------------------------------------------------------------------------

def build_entity_hubs(vault_dir: str | Path) -> int:
    """Add 'Referenced by' sections to entity notes listing all claims
    that mention them. Returns count of entities updated."""
    vault = Path(vault_dir)

    # Index: entity stem → entity file path
    entity_files: dict[str, Path] = {}
    # Index: entity stem → set of aliases
    entity_aliases: dict[str, list[str]] = {}

    for md in _find_all_md(vault):
        text = md.read_text(encoding="utf-8")
        if "kind: entity" not in text:
            continue
        entity_files[md.stem] = md
        aliases = [md.stem]
        try:
            parts = text.split("---", 2)
            meta = yaml.safe_load(parts[1]) or {}
            for a in meta.get("aliases", []):
                if a and len(str(a)) >= 3:
                    aliases.append(str(a))
        except (ValueError, yaml.YAMLError):
            pass
        entity_aliases[md.stem] = aliases

    # Scan all claims for references to each entity
    entity_refs: dict[str, list[str]] = {stem: [] for stem in entity_files}

    for md in _find_all_md(vault):
        if md.stem in entity_files:
            continue  # skip entity files themselves
        text = md.read_text(encoding="utf-8")
        links = _WIKILINK_RE.findall(text)
        body_lower = text.lower()

        for stem, aliases in entity_aliases.items():
            # Check wikilinks
            if stem in links:
                entity_refs[stem].append(md.stem)
                continue
            # Check plain text mentions
            if any(a.lower() in body_lower for a in aliases):
                entity_refs[stem].append(md.stem)

    # Update entity files with Referenced by section
    updated = 0
    for stem, refs in entity_refs.items():
        if not refs:
            continue
        path = entity_files[stem]
        text = path.read_text(encoding="utf-8")

        # Remove existing Referenced by section if present
        text = re.sub(
            r"\n## Referenced by\n.*",
            "",
            text,
            flags=re.DOTALL,
        )

        # Add new section
        ref_lines = [f"\n## Referenced by\n"]
        for ref in sorted(refs):
            ref_lines.append(f"- [[{ref}]]")
        text = text.rstrip() + "\n" + "\n".join(ref_lines) + "\n"

        path.write_text(text, encoding="utf-8")
        updated += 1

    log.info("build_entity_hubs: updated %d entities", updated)
    return updated


# ---------------------------------------------------------------------------
# restore_bodies — fix atoms whose body is just a Parent backlink
# ---------------------------------------------------------------------------

def restore_bodies(vault_dir: str | Path, tmp_dir: str | Path) -> int:
    """For layer-0 atoms whose body is just a Parent line, restore the
    original body from deduped claims and re-append the Parent line."""
    vault = Path(vault_dir)
    tmp = Path(tmp_dir)

    # Load original deduped claims
    originals: dict[str, str] = {}
    deduped_path = tmp / "deduped_claims.md"
    if not deduped_path.exists():
        log.warning("No deduped_claims.md found in %s", tmp)
        return 0
    for note in parse_notes(deduped_path.read_text(encoding="utf-8")):
        originals[note.title] = note.body

    # Also load from all extract files as fallback
    for ef in sorted((tmp / "results").glob("extract_*.md")):
        for note in parse_notes(ef.read_text(encoding="utf-8")):
            if note.title not in originals:
                originals[note.title] = note.body

    restored = 0
    for md in _find_all_md(vault):
        text = md.read_text(encoding="utf-8")
        if "layer: 0" not in text:
            continue

        parts = text.split("---", 2)
        if len(parts) < 3:
            continue
        body = parts[2].strip()

        # Check if body is just a Parent line or very short
        body_lines = [l for l in body.splitlines() if l.strip() and not l.strip().startswith("Parent:")]
        if len(body_lines) < 1 or len(body) < 50:
            # Try to restore from originals
            stem = md.stem
            if stem in originals and len(originals[stem]) > len(body):
                # Preserve any Parent line
                parent_line = ""
                for line in body.splitlines():
                    if "Parent:" in line:
                        parent_line = line.strip()
                        break
                new_body = originals[stem].strip()
                if parent_line and parent_line not in new_body:
                    new_body += f"\n\n{parent_line}"
                new_content = f"---{parts[1]}---\n\n{new_body}\n"
                md.write_text(new_content, encoding="utf-8")
                restored += 1

    log.info("restore_bodies: restored %d notes", restored)
    return restored


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _find_all_md(vault: Path) -> list[Path]:
    """Recursively find all .md files in vault (excluding .obsidian)."""
    results = []
    for md in vault.rglob("*.md"):
        if ".obsidian" in str(md):
            continue
        results.append(md)
    return sorted(results)


def _wire_parent_links(by_title: dict[str, Note], tmp: Path) -> None:
    """Extract Parent assignments from group/pyramid files and apply to notes.

    Handles both `Parent: [[X]]` and `Parent: "[[X]]"` formats.
    Uses fuzzy matching to resolve title variations.
    """
    parent_map: dict[str, str] = {}  # child_title → parent_title

    # Scan group + pyramid files for Parent: lines and Children: sections
    source_files = sorted(
        list(tmp.glob("results/group_*.md")) + list(tmp.glob("results/pyramid.md"))
    )
    for gf in source_files:
        if not gf.exists():
            continue
        text = gf.read_text(encoding="utf-8")
        notes = re.split(r"(?=^## )", text, flags=re.MULTILINE)

        for note_text in notes:
            if not note_text.strip():
                continue
            title_match = re.match(r"^## (.+)$", note_text, re.MULTILINE)
            if not title_match:
                continue
            title = title_match.group(1).strip()

            # Extract Parent: from this note (quoted or unquoted)
            for line in note_text.splitlines():
                m = re.search(r'Parent:\s*"?\[\[([^\]]+)\]\]"?', line)
                if m:
                    parent_map[title] = m.group(1)

            # Extract Children: section → infer parent for each child
            if "Children:" in note_text:
                children_text = note_text[note_text.index("Children:"):]
                children = _WIKILINK_RE.findall(children_text)
                for child in children:
                    if child not in parent_map:
                        parent_map[child] = title

    # Also infer parent-child from L2 body wikilinks → L1 notes
    # (when pyramid agent didn't write explicit Children: sections)
    for title, note in by_title.items():
        if note.meta.get("layer") != 2:
            continue
        # Every wikilink in a L2 body that points to an L1 note is a child
        body_links = _WIKILINK_RE.findall(note.body)
        for link in body_links:
            resolved = _fuzzy_resolve(link, set(by_title.keys()))
            if resolved and resolved in by_title:
                child = by_title[resolved]
                if child.meta.get("layer") == 1 and resolved not in parent_map:
                    parent_map[resolved] = title

    log.info("_wire_parent_links: found %d assignments", len(parent_map))

    # Apply to notes in by_title
    all_titles = set(by_title.keys())
    applied = 0
    skipped_resolve = 0

    for child_title, parent_title in parent_map.items():
        child_key = _fuzzy_resolve(child_title, all_titles)
        if not child_key:
            skipped_resolve += 1
            continue
        parent_key = _fuzzy_resolve(parent_title, all_titles)
        if not parent_key:
            # Parent title from file doesn't match by_title — try exact match
            if parent_title in all_titles:
                parent_key = parent_title
            else:
                skipped_resolve += 1
                continue

        note = by_title[child_key]
        if "Parent:" in note.body or note.meta.get("Parent"):
            continue

        note.body = note.body.rstrip() + f"\n\nParent: [[{parent_key}]]"
        applied += 1

    # Second pass: assign orphan L1 notes to L2 parents via body wikilinks
    for title, note in by_title.items():
        if note.meta.get("layer") != 1:
            continue
        if "Parent:" in note.body or note.meta.get("Parent"):
            continue
        # Find which L2 note links to this L1
        for l2_title, l2_note in by_title.items():
            if l2_note.meta.get("layer") != 2:
                continue
            if f"[[{title}]]" in l2_note.body:
                note.body = note.body.rstrip() + f"\n\nParent: [[{l2_title}]]"
                applied += 1
                break

    log.info("_wire_parent_links: applied %d backlinks (%d skipped resolve)", applied, skipped_resolve)


def fix_ghost_links(vault_dir: str | Path) -> dict:
    """Fix ghost wikilinks caused by numbered prefixes and title mismatches.

    1. Strip numbered prefixes: [[36. Title]] → [[Title]]
    2. Fuzzy-match remaining ghosts to real files

    Returns stats dict.
    """
    vault = Path(vault_dir)
    all_stems: set[str] = set()
    for md in _find_all_md(vault):
        all_stems.add(md.stem)

    # Collect all ghost links
    ghost_links: set[str] = set()
    for md in _find_all_md(vault):
        text = md.read_text(encoding="utf-8")
        for link in _WIKILINK_RE.findall(text):
            link_target = link.split("|")[0].strip() if "|" in link else link
            if link_target not in all_stems:
                ghost_links.add(link)

    # Build replacement map
    replacements: dict[str, str] = {}
    for ghost in ghost_links:
        # 1. Strip numbered prefix
        clean = re.sub(r"^\d+\.\s*", "", ghost)
        if clean in all_stems:
            replacements[ghost] = clean
            continue
        # 2. Fuzzy match
        match = _fuzzy_resolve(ghost, all_stems)
        if match and match != ghost:
            replacements[ghost] = match

    # Apply replacements
    stats = {"ghosts_fixed": 0, "files_modified": 0}
    for md in _find_all_md(vault):
        text = md.read_text(encoding="utf-8")
        original = text
        for ghost, real in replacements.items():
            text = text.replace(f"[[{ghost}]]", f"[[{real}]]")
        if text != original:
            md.write_text(text, encoding="utf-8")
            stats["files_modified"] += 1
            stats["ghosts_fixed"] += sum(
                1 for g in replacements if f"[[{g}]]" in original
            )

    log.info("fix_ghost_links: %s", stats)
    return stats


def _fuzzy_resolve(title: str, all_titles: set[str]) -> str | None:
    """Resolve a title to the closest match in all_titles."""
    if title in all_titles:
        return title
    # Strip numbered prefix
    clean = re.sub(r"^\d+\.\s*", "", title)
    if clean in all_titles:
        return clean
    # Fuzzy match
    matches = difflib.get_close_matches(title, all_titles, n=1, cutoff=0.75)
    return matches[0] if matches else None


def _normalize_note_meta(note) -> None:
    """Fix all common metadata issues agents produce.

    Handles:
    - tags: null → generate default tags from kind/layer
    - tags as CSV string → convert to proper YAML list
    - missing source/ tag → add from source field or source_slug
    - missing kind → infer from tags
    - missing layer → default to 0 for claims
    """
    meta = note.meta

    # Fix tags: null or tags as string
    tags = meta.get("tags")
    if tags is None or isinstance(tags, str):
        kind = meta.get("kind", "claim")
        layer = meta.get("layer", 0)

        if isinstance(tags, str) and tags.strip():
            # "art, morality" → extract domains
            domains = [t.strip() for t in tags.split(",") if t.strip()]
        else:
            domains = []

        new_tags = []
        if kind == "entity":
            etype = meta.get("entity_type", "concept")
            new_tags.append(f"type/entity/{etype}")
        else:
            layer_name = {0: "atom", 1: "structure", 2: "structure", 3: "index"}.get(layer, "atom")
            new_tags.append(f"type/claim/{layer_name}")

        new_tags.append("priority/support")
        new_tags.append("certainty/argued")
        new_tags.append("stance/endorsed")

        if domains:
            new_tags.append(f"domain/{domains[0]}")

        new_tags.append("role/argument")
        meta["tags"] = new_tags
        tags = new_tags

    # Ensure tags is always a list
    if not isinstance(tags, list):
        meta["tags"] = []
        tags = meta["tags"]

    # Migrate source: field to source/ tag
    source_field = meta.get("source") or meta.get("source_slug")
    if source_field and isinstance(source_field, str):
        has_source_tag = any(str(t).startswith("source/") for t in tags)
        if not has_source_tag:
            tags.append(f"source/{source_field}")

    # Infer kind from tags
    if "kind" not in meta:
        if any("type/entity" in str(t) for t in tags):
            meta["kind"] = "entity"
        elif any("type/claim" in str(t) for t in tags):
            meta["kind"] = "claim"

    # Default layer for claims
    if meta.get("kind") == "claim" and "layer" not in meta:
        meta["layer"] = 0

    # Remove layer from entities
    if meta.get("kind") == "entity":
        meta.pop("layer", None)


def _split_frontmatter(content: str) -> tuple[str | None, str]:
    """Split content into (frontmatter, body), handling files without frontmatter.

    Only splits on standalone `---` lines, not on `|---|---|` table separators.
    Returns (None, content) for files without frontmatter.
    """
    lines = content.split("\n")

    # Find first standalone --- (must be the first non-empty line or very early)
    first_fence = -1
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped == "---":
            first_fence = i
            break
        if stripped and i > 2:
            # Content started before any --- fence = no frontmatter
            return None, content

    if first_fence == -1:
        return None, content

    # Find closing ---
    second_fence = -1
    for i in range(first_fence + 1, len(lines)):
        if lines[i].strip() == "---":
            second_fence = i
            break

    if second_fence == -1:
        return None, content

    frontmatter = "\n".join(lines[first_fence + 1:second_fence])
    body = "\n".join(lines[second_fence + 1:])
    return frontmatter, body


def _find_outside_wikilinks(body: str, name: str) -> tuple[int, int] | None:
    """Find *name* in *body* only in regions NOT inside [[...]]."""
    # Build a set of protected ranges (inside wikilinks)
    protected: list[tuple[int, int]] = []
    for m in _WIKILINK_RE.finditer(body):
        protected.append((m.start(), m.end()))

    # Use word boundaries to avoid matching substrings (System inside Systematic)
    pattern = re.compile(r"\b" + re.escape(name) + r"\b", re.IGNORECASE)
    for m in pattern.finditer(body):
        start, end = m.start(), m.end()
        # Check if this match overlaps any protected range
        inside = any(ps <= start < pe for ps, pe in protected)
        if not inside:
            return (start, end)
    return None


def _safe_filename(title: str) -> str:
    for ch in r'<>:"/\|?*':
        title = title.replace(ch, "")
    # Also replace forward slash which is path separator
    title = title.replace("/", "-")
    return title.strip()[:200]  # cap length for filesystem safety
