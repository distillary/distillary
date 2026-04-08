# Distillary — The Plan

## What this is

A tool that turns books into navigable Obsidian vaults. You give it a book,
it gives you a pyramid of claims, entities, and connections. The vault is
the output. Git is the distribution. Anyone can process a book and share
the result.

## What works today

- Extract atomic claims from EPUB/PDF/TXT
- Deduplicate, group into a pyramid, find lateral connections
- Extract and link entities
- Write organized Obsidian vault with folders, index, CSS, Bases
- Parallel haiku/opus agents make it fast (~15 min per book)
- `fix_vault`, `reinforce_links`, `validate` post-processing

## What's missing

### 1. Agents that fix and discover automatically

The pipeline produces a vault. Then it should run a **doctor agent** that:

- Finds orphan notes (no parent, no links) and connects them to the nearest parent
- Finds entity names mentioned as plain text and wikilinks them
- Finds concepts that appear in 3+ claims but have no entity note — creates ghost notes for them
- Finds claims that contradict each other but aren't marked as tensions — adds tension links
- Reports what it fixed and what it suggests exploring

This isn't a separate step. It's the last step of the pipeline. One haiku
agent scans the vault, fixes mechanical issues, and writes a `_suggestions.md`
note listing ghosts worth promoting and tensions worth investigating.

The user opens the vault and sees: "Here's what the book says. Here's 12
concepts at the frontier you might want to explore. Here are 4 tensions
between claims that deserve your attention."

### 2. Source references — page/section traceability

Every atomic claim should optionally carry a `source_ref` field:

```yaml
source_ref: "Chapter 3, p.47"
```

or

```yaml
source_ref: "Part II, Section 'Validated Learning', para 3"
```

This is critical for:
- **Fact-checking**: Click a claim, see where in the book it comes from, verify it
- **Trust**: Users can trace any claim back to its origin
- **Citation**: Academic or professional use requires page numbers

The extraction agent gets the chapter/section context from the text chunk
it's processing. It doesn't know page numbers (EPUB doesn't have fixed pages),
but it knows chapter titles, section headers, and relative position. That's
enough for a reader to find the passage.

Add `source_ref:` to the EXTRACT prompt template. Add it to the YAML frontmatter.
One field. No extra pipeline step.

### 3. Shareable vaults on GitHub

The vault is a folder of markdown files. Git already knows how to version
and share folders. The plan:

**How someone processes a book:**
```bash
fractal decompose book.epub -o vault-book-name/
```

**How they share it:**
```bash
cd vault-book-name/
git init
git add .
git commit -m "Distillary vault: Book Name by Author (2024)"
gh repo create distillary-vault-book-name --public
git push
```

Tag the repo with `distillary-vault` + topic tags like `entrepreneurship`,
`psychology`, `economics`. That's it.

**How someone uses a shared vault:**
```bash
git clone https://github.com/user/distillary-vault-book-name
# Open in Obsidian
```

**How someone combines vaults:**
```bash
git clone .../distillary-vault-lean-startup
git clone .../distillary-vault-mom-test
fractal compare vault-lean-startup/ vault-mom-test/ -o vault-comparison/
```

No platform. No server. No account. Git repos with a tag convention.
GitHub's topic search becomes the discovery mechanism.

**How someone publishes as a website:**
```bash
distillary publish vault-lean-startup/ --topic entrepreneurship
# → builds static site with Quartz (graph view, search, backlinks)
# → creates GitHub repo with distillary-vault tag
# → deploys to GitHub Pages for free
# → live at https://username.github.io/distillary-vault-lean-startup

# Or just preview locally first:
distillary preview vault-lean-startup/
# → http://localhost:8080 with full graph view
```

Quartz converts the Obsidian vault to a static site with graph view,
wikilink resolution, backlinks, full-text search, and tag pages. Free
on GitHub Pages. One command.

**What makes vaults combinable:**
- Same note format (YAML frontmatter + body with wikilinks)
- Same tag taxonomy (priority/, certainty/, stance/, domain/, role/, source/)
- `proposition:` field as the semantic key for cross-vault dedup
- `source/` tag for attribution
- `published:` for temporal ordering

Two vaults produced by two different people on different machines combine
with `cat`. That's the whole interop story.

### 4. The community workflow

```
Someone reads a book
  → runs fractal on it
  → pushes vault to GitHub with distillary-vault tag
  → another person finds it via topic search
  → clones it into their Obsidian
  → adds their own annotations (annotations/ subfolder)
  → optionally pushes their annotated fork
  → a third person combines 5 vaults on the same topic
  → runs fractal compare to build a field-level meta-vault
  → pushes that as a new repo
```

The unit of sharing is a git repo. The unit of combination is `concat`.
The discovery mechanism is GitHub topics. The personal layer is the
`annotations/` subfolder which lives in the user's fork and never
conflicts with the upstream vault.

No central server. No API. No accounts. Just markdown, git, and a tag.

### 5. The doctor agent — what it does

After `fractal decompose` finishes, the doctor agent runs automatically:

```python
def doctor(vault_dir):
    """Fix issues and suggest explorations."""
    
    # Fix: orphans → find nearest parent by tag/domain similarity
    # Fix: plain-text entity mentions → add [[wikilinks]]
    # Fix: missing propositions → generate from body text
    
    # Discover: concepts in 3+ claims without entity notes → create ghost notes
    # Discover: claims that pull in opposite directions → suggest tension links
    # Discover: entity notes referenced by 1 claim → flag as potentially over-extracted
    
    # Write _suggestions.md with:
    #   - "Explore these ghost concepts: [[X]], [[Y]], [[Z]]"
    #   - "These claims may contradict: [[A]] vs [[B]]"
    #   - "These orphan notes need a home: [[C]], [[D]]"
```

The fixes are mechanical (haiku). The suggestions are analytical (haiku
reads claim pairs and flags potential tensions). The user decides what
to act on.

### 6. What NOT to build

- No web app. Obsidian IS the interface.
- No database. The filesystem IS the database.
- No user accounts. Git handles identity.
- No search server. Obsidian search + Bases handle queries.
- No custom sync. Git push/pull is sync.
- No plugin. The vault works in vanilla Obsidian.
- No complex merge logic. `source/` tags prevent ambiguity.

---

## Implementation plan

### Phase 1: Fix what exists (this week)

- [ ] Add `source_ref` field to EXTRACT prompt — chapter/section context
- [ ] Add doctor agent to pipeline (fix orphans, reinforce links, generate ghosts)
- [ ] Write `_suggestions.md` automatically after each vault build
- [ ] Fix the parser bug for good (already done: `## Related` no longer splits)
- [ ] Add `fractal compare` CLI command using existing `distill_field()`

### Phase 2: Make it shareable (next)

- [ ] Add `distillary init` — creates `.gitignore`, `README.md` with vault stats
- [ ] Add `distillary publish` — `git init && git add && git commit && gh repo create --public`
- [ ] Convention: repo name `distillary-vault-{slug}`, topics: `distillary-vault` + domain
- [ ] Add `fractal clone <github-url>` — clone + open in Obsidian
- [ ] Add `fractal combine <vault1> <vault2> -o combined/` — concat + dedupe + re-link

### Phase 3: Community grows (later)

- [ ] `fractal search <topic>` — `gh search repos --topic distillary-vault --topic <topic>`
- [ ] `fractal browse` — list all `distillary-vault` repos on GitHub, show stats
- [ ] Meta-vaults: someone combines 10 entrepreneurship vaults into a field summary
- [ ] Annotation sharing: forks with `annotations/` become book club discussions

---

## The 3 commands that matter most

```bash
# Process a book
fractal decompose book.epub -o vault/

# Compare two vaults
fractal compare vault1/ vault2/ -o comparison/

# Share a vault
distillary publish vault/ --topic entrepreneurship
```

Everything else is convenience. These three are the core loop:
read → distill → share → combine → distill again.

---

## Why this works

The format is simple: markdown files with YAML frontmatter and wikilinks.
Every tool already knows how to read it. Obsidian renders it. Git versions
it. GitHub distributes it. Dataview/Bases query it. The LLM produces it.

No lock-in. No platform risk. No dependency beyond files and folders.

If this repo disappears tomorrow, every vault ever produced still works
in Obsidian. The vaults are the value, not the tool. The tool just makes
them faster to produce.
