Add something to the brain — a book, PDF, article, video, or any document.

Read the skill instructions from `.claude/skills/distillary-add-source.md` FIRST, then follow the full pipeline. Read agent definitions from `.claude/agents/` — never rewrite agent instructions from memory.

What to add: $ARGUMENTS

**Auto-detect the type from the argument:**

- File path ending in `.pdf`, `.epub`, `.txt`, `.md` → extract text directly
- YouTube URL (`youtube.com`, `youtu.be`) → download transcript with yt-dlp, then process
- Web URL → fetch with WebFetch, clean HTML, then process
- Directory path → ask if user wants `/dist:create` instead

**Examples the user might type:**

```
/dist:add books/rich-dad-poor-dad.pdf
/dist:add books/my-book.epub
/dist:add https://youtube.com/watch?v=abc123
/dist:add https://paulgraham.com/ds.html
```

**For every source:**
1. Save chunks permanently to `brain/sources/{slug}/chunks/`
2. Extract with v4.0 format (backing + passages)
3. Report progress at every step: "Extracting claims...", "Deduping...", "Grouping..."
4. After completion, run concept-mapper if other sources exist
5. Print final summary:

```
Done! "{title}" added to brain.

  Claims: {N} atoms → {M} clusters → {K} structure → 1 root
  Entities: {X} concepts, {Y} people
  Bridges: {B} concepts connecting to other sources
  Chunks: {N} stored
  Output: brain/sources/{slug}/
```
