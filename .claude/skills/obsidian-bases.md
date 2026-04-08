---
name: obsidian-bases
description: Create Obsidian Bases (.base files) for structured vaults. Use when user wants database views, filtered tables, computed properties, or analytical dashboards in Obsidian. Triggers on "create base", "obsidian base", "base file", "database view", "vault analytics".
---

# Obsidian Bases Skill

Create powerful `.base` files for Obsidian vaults with structured YAML frontmatter.

## When to create a Base

Only create a Base when it answers a **specific question** the user can't answer by browsing. A Base is NOT a list — it's an analytical view with computed properties, grouping, or summaries.

**Good reasons to create a Base:**
- "Which notes are most connected?" → Hub analysis with link counting
- "Where are the weak points?" → Computed strength formula + filter
- "How is certainty distributed across topics?" → GroupBy with summaries
- "Which entities dominate?" → Backlink ranking with influence tiers

**Bad reasons (don't create a Base):**
- "Show me all notes with tag X" → User can do this with Obsidian search
- "List all files in folder Y" → File explorer does this
- "Show me everything" → Useless without filtering

## .base file format

`.base` files use YAML syntax. Obsidian reads them as native database views.

### Minimal example

```yaml
filters:
  and:
    - kind == "claim"
views:
  - type: table
    name: My View
    order:
      - file.name
```

### Full-featured example

```yaml
filters:
  and:
    - kind == "claim"
    - layer >= 1
formulas:
  branch_size: file.links.length
  certainty: if(file.hasTag("certainty/established"), "Established", if(file.hasTag("certainty/argued"), "Argued", "Speculative"))
views:
  - type: table
    name: By Certainty
    groupBy:
      property: formula.certainty
      direction: ASC
    order:
      - layer
      - formula.branch_size
      - file.name
    summaries:
      formula.branch_size: Average
  - type: table
    name: Large Branches Only
    filters:
      and:
        - formula.branch_size > 5
    order:
      - formula.branch_size
      - file.name
```

## Syntax rules

### Property references

| Context | Syntax | Example |
|---|---|---|
| `order`, `groupBy` | bare name | `layer`, `proposition`, `file.name` |
| `filters` (string) | bare name | `kind == "claim"`, `layer >= 1` |
| `formulas` | bare name or `file.*` | `file.links.length`, `layer + 1` |

**IMPORTANT**: Do NOT use `note.` prefix in `order` or `groupBy`. Obsidian strips it. Use bare property names: `layer`, `proposition`, `entity_type`.

Use `file.*` for file metadata: `file.name`, `file.links`, `file.backlinks`, `file.tags`, `file.folder`, `file.size`, `file.ctime`, `file.mtime`.

### Filters

```yaml
# Global (all views)
filters:
  and:
    - file.hasTag("priority/core")
    - kind == "claim"

# Per-view (additional)
views:
  - type: table
    filters:
      and:
        - formula.strength == "Weak"
```

Boolean logic: `and`, `or`, `not` (recursive). String filters use `==`, `!=`, `>`, `<`, `>=`, `<=`.

### Filter functions

| Function | Use |
|---|---|
| `file.hasTag("tag")` | Check if note has a tag |
| `file.inFolder("path")` | Check folder location |
| `file.hasLink(other)` | Check if note links to another |
| `file.hasProperty("name")` | Check if property exists |

### Formulas — computed properties

Formulas create new columns from existing data. This is what makes Bases powerful.

```yaml
formulas:
  # Count connections
  total_links: file.links.length + file.backlinks.length
  
  # Classify by threshold
  influence: if(total_links > 10, "Hub", if(total_links > 3, "Connected", "Sparse"))
  
  # Extract from tag list
  domain: tags.find(t => t.startsWith("domain/"))
  
  # Conditional logic
  strength: if(file.hasTag("certainty/established") && file.hasTag("priority/core"), "Strong", if(file.hasTag("certainty/speculative"), "Weak", "Medium"))
  
  # Date math
  age: now() - file.ctime
  days_old: (now() - file.ctime) / duration("1d")
```

**Formula string quoting**: Obsidian auto-strips quotes. Write formulas without wrapping quotes when possible. If YAML parsing breaks, wrap the whole formula in single quotes.

### Views

```yaml
views:
  - type: table          # table | cards | list
    name: View Name
    limit: 20            # max rows
    groupBy:
      property: formula.certainty
      direction: DESC    # ASC or DESC
    order:               # columns shown, in order
      - file.name
      - proposition
      - formula.strength
    summaries:
      formula.branch_size: Average    # Sum, Min, Max, Median, etc.
```

Multiple views = tabs. Each view can have its own filters.

### Available summary functions

Number: `Average`, `Sum`, `Min`, `Max`, `Range`, `Median`, `Stddev`
Date: `Earliest`, `Latest`, `Range`
Boolean: `Checked`, `Unchecked`
Any: `Empty`, `Filled`, `Unique`

### Available list/string functions

Lists: `.length`, `.contains()`, `.filter()`, `.map()`, `.sort()`, `.unique()`, `.join()`, `.flat()`
Strings: `.contains()`, `.startsWith()`, `.endsWith()`, `.lower()`, `.split()`, `.replace()`
Numbers: `.round()`, `.ceil()`, `.floor()`, `.abs()`, `.toFixed()`

## Design principles

1. **Every Base must answer a question**, not just list data
2. **Use formulas** to compute things not visible from titles alone (link counts, classifications, strength scores)
3. **Use groupBy** to reveal patterns (certainty distribution, entity types, claim roles)
4. **Use summaries** to aggregate (average branch size, total per group)
5. **Use multi-view tabs** for different perspectives on same dataset (not separate Bases)
6. **Use per-view filters** to create focused sub-views (e.g., "Weak Claims" tab)
7. **Don't create a Base for simple tag filtering** — Obsidian search does that

## Patterns for knowledge vaults

### Hub analysis
Question: "Which ideas are most connected?"
```yaml
formulas:
  total: file.links.length + file.backlinks.length
  density: if(total > 10, "Hub", if(total > 3, "Connected", "Sparse"))
views:
  - type: table
    filters:
      and:
        - formula.total > 3
    order:
      - formula.total
      - file.name
    summaries:
      formula.total: Average
```

### Entity influence ranking
Question: "Which concepts dominate?"
```yaml
filters:
  and:
    - kind == "entity"
formulas:
  refs: file.backlinks.length
  tier: if(refs > 30, "Central", if(refs > 10, "Important", "Minor"))
views:
  - type: table
    groupBy:
      property: formula.tier
    order:
      - formula.refs
      - file.name
    summaries:
      formula.refs: Average
```

### Claim strength assessment
Question: "Where are the weak spots?"
```yaml
formulas:
  role: if(file.hasTag("role/fact"), "Fact", if(file.hasTag("role/argument"), "Argument", "Other"))
  strength: if(file.hasTag("certainty/established") && file.hasTag("priority/core"), "Strong", if(file.hasTag("certainty/speculative"), "Weak", "Medium"))
views:
  - type: table
    name: By Type
    groupBy:
      property: formula.role
    order:
      - formula.strength
      - file.name
  - type: table
    name: Weak Only
    filters:
      and:
        - formula.strength == "Weak"
```

### Branch depth analysis
Question: "Which arguments are deepest?"
```yaml
filters:
  and:
    - kind == "claim"
    - layer >= 1
formulas:
  children: file.links.length
views:
  - type: table
    groupBy:
      property: layer
      direction: DESC
    order:
      - formula.children
      - file.name
    summaries:
      formula.children: Average
```

### Recently modified
Question: "What have I been working on?"
```yaml
formulas:
  modified: file.mtime.relative()
views:
  - type: table
    limit: 20
    order:
      - file.mtime
      - file.name
```
