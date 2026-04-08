"""Note model, YAML parser/serializer, and body-query helpers.

The canonical stream format:
    ## Title
    ---
    tags:
      - type/claim/atom
    kind: claim
    layer: 0
    ---

    Body text with [[wikilinks]].

    ## Related
    - Parent: [[Some parent]]
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

import yaml


# ---------------------------------------------------------------------------
# Dataclass
# ---------------------------------------------------------------------------

@dataclass
class Note:
    title: str
    meta: dict = field(default_factory=dict)
    body: str = ""

    # convenience accessors
    @property
    def kind(self) -> str:
        return self.meta.get("kind", "")

    @property
    def layer(self) -> int:
        return int(self.meta.get("layer", 0))

    @property
    def tags(self) -> list[str]:
        return self.meta.get("tags", [])


# ---------------------------------------------------------------------------
# Parsing  — stream text → list[Note]
# ---------------------------------------------------------------------------

_TITLE_RE = re.compile(r"^##\s+(.+)$", re.MULTILINE)
_WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")

# Headers that appear inside note bodies — NOT new note titles
_BODY_HEADERS = {"Related", "Child-Parent Assignments", "Child-to-Parent Assignments"}


def parse_notes(text: str) -> list[Note]:
    """Split a stream on `## Title` lines that start real notes.

    A `## Title` line is a real note boundary only if the text that
    follows it starts with `---` (YAML frontmatter). Lines like
    `## Related` or `## Child-Parent Assignments` inside note bodies
    are NOT treated as new notes.

    Also strips `# H1` section dividers that agents sometimes use
    (e.g., `# LAYER 2 — CLUSTERS`) — these are not note boundaries.
    """
    # Strip h1 section headers that agents use as dividers
    text = re.sub(r"^# .+$", "", text, flags=re.MULTILINE)
    # Strip CHILD UPDATES / Child-Parent Assignments blocks entirely
    # These are agent output artifacts that list parent-child mappings redundantly
    text = re.sub(
        r"(?:CHILD UPDATES|CHILD UPDATE|Child.Parent Assignments|Child Note Updates).*",
        "", text, flags=re.DOTALL | re.IGNORECASE,
    )
    # Fix glued frontmatter fences: ---tags: → ---\ntags:  and  value--- → value\n---
    text = re.sub(r"^---(\w)", r"---\n\1", text, flags=re.MULTILINE)
    text = re.sub(r"(\S)---$", r"\1\n---", text, flags=re.MULTILINE)
    parts = _TITLE_RE.split(text)
    # parts: [preamble, title1, rest1, title2, rest2, ...]
    notes: list[Note] = []
    i = 1
    pending_body_extra = ""

    while i < len(parts) - 1:
        title = parts[i].strip()
        raw = parts[i + 1]

        # Check if this is a body header, not a real note title
        if title in _BODY_HEADERS or not raw.strip().startswith("---"):
            # This is a section header inside the previous note's body
            # Append it back to the previous note
            if notes:
                notes[-1].body = (
                    notes[-1].body.rstrip()
                    + f"\n\n## {title}\n"
                    + raw.rstrip()
                )
            i += 2
            continue

        meta, body = _parse_yaml_body(raw)
        notes.append(Note(title=title, meta=meta, body=body.strip()))
        i += 2

    return notes


def _parse_yaml_body(raw: str) -> tuple[dict, str]:
    """Given text after the ## Title line, extract YAML frontmatter and body.

    Finds closing --- only on its own line (not glued to values like prop---).
    """
    stripped = raw.strip()
    if not stripped.startswith("---"):
        return {}, stripped

    # Find closing --- that is on its own line
    lines = stripped.split("\n")
    # First line is the opening ---
    closing_idx = -1
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            closing_idx = i
            break

    if closing_idx == -1:
        # No proper closing fence — try to parse everything as YAML
        # and split at the first blank line
        yaml_lines = []
        body_start = len(lines)
        for i in range(1, len(lines)):
            if not lines[i].strip():
                body_start = i
                break
            yaml_lines.append(lines[i])
        yaml_str = "\n".join(yaml_lines)
        body = "\n".join(lines[body_start:])
        try:
            meta = yaml.safe_load(yaml_str) or {}
        except yaml.YAMLError:
            meta = {}
        return meta, body

    yaml_str = "\n".join(lines[1:closing_idx])
    body = "\n".join(lines[closing_idx + 1:])
    try:
        meta = yaml.safe_load(yaml_str) or {}
    except yaml.YAMLError:
        meta = {}
    return meta, body


# ---------------------------------------------------------------------------
# Serialization  — list[Note] → stream text
# ---------------------------------------------------------------------------

def serialize(notes: list[Note]) -> str:
    """Convert notes back into the canonical stream format."""
    blocks: list[str] = []
    for note in notes:
        block = f"## {note.title}\n---\n"
        block += yaml.dump(
            note.meta,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
        ).strip()
        block += "\n---\n\n"
        block += note.body
        blocks.append(block)
    return "\n\n".join(blocks)


# ---------------------------------------------------------------------------
# Body query helpers  — relationships live in the body, not YAML
# ---------------------------------------------------------------------------

def wikilinks_in(text: str) -> list[str]:
    """Extract all [[wikilink]] targets from text."""
    return _WIKILINK_RE.findall(text)


def _lines_after(body: str, label: str) -> list[str]:
    """Collect bullet lines that follow a label like 'Parent:' or 'Children:'."""
    lines = body.splitlines()
    results: list[str] = []
    for line in lines:
        stripped = line.strip()
        # single-line label:  Parent: [[X]]
        if stripped.startswith(label):
            results.extend(_WIKILINK_RE.findall(stripped))
        # bullet list under ## Related  —  - [[X]]
    return results


def _bulleted_wikilinks(body: str, prefixes: str) -> list[str]:
    """Extract wikilinks from Related bullets starting with given emoji prefixes."""
    results: list[str] = []
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith("-") and any(p in stripped for p in prefixes):
            results.extend(_WIKILINK_RE.findall(stripped))
    return results


def parents_of(note: Note) -> list[str]:
    return _lines_after(note.body, "Parent:")


def children_of(note: Note) -> list[str]:
    return _lines_after(note.body, "Children:")


def cross_links(note: Note) -> list[str]:
    return _bulleted_wikilinks(note.body, "⚡🔁📊❓")


def mentioned_entities(note: Note) -> list[str]:
    return _lines_after(note.body, "Mentioned:")


# ---------------------------------------------------------------------------
# Collection helpers
# ---------------------------------------------------------------------------

def claim_notes(notes: list[Note]) -> list[Note]:
    return [n for n in notes if n.kind == "claim"]


def entity_notes(notes: list[Note]) -> list[Note]:
    return [n for n in notes if n.kind == "entity"]


def count_roots(notes: list[Note]) -> int:
    return len([n for n in notes if not parents_of(n)])


def has_children(note: Note) -> bool:
    return len(children_of(note)) > 0


def collect_subtree(notes: list[Note], title: str) -> list[Note]:
    """Collect a note and all its descendants by traversing children links."""
    by_title = {n.title: n for n in notes}
    result: list[Note] = []
    stack = [title]
    seen: set[str] = set()
    while stack:
        t = stack.pop()
        if t in seen or t not in by_title:
            continue
        seen.add(t)
        note = by_title[t]
        result.append(note)
        stack.extend(children_of(note))
    return result


def replace_note(notes: list[Note], title: str, updated: Note) -> list[Note]:
    """Replace a note by title, keeping list order."""
    return [updated if n.title == title else n for n in notes]


def topological_order(notes: list[Note]) -> list[Note]:
    """Return notes in top-down order (highest layer first)."""
    return sorted(notes, key=lambda n: -n.layer)
