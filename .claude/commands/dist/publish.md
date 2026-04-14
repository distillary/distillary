Publish the brain as a website.

Options: $ARGUMENTS

**Examples:**

```
/dist:publish
/dist:publish preview
```

Read `.claude/skills/distillary-publish.md` FIRST.

- No argument → build and deploy to GitHub Pages
- "preview" → start local dev server

**Before publishing:**
- Check each source's `_source.md` for `publishable: false`
- Exclude chunks from copyrighted sources
- Generate `agent.json` manifest so other agents can query the site

**Print:** the published URL when done.
