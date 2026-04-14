Save the last lookup, research, or any response as a personal note in the brain.

What to save: $ARGUMENTS

**Examples:**

```
/dist:note save the last lookup
/dist:note save as "كيف نفهم أنفسنا"
/dist:note save the last research about debt
```

**What happens:**

1. Find the most recent substantive response (lookup, research, compare, or any brain-related answer) in this conversation
2. Ask for a title if not provided — suggest one based on the content
3. Convert the response into a proper brain note:
   - Add `type/note` tag and appropriate `domain/` tag
   - Convert entity/claim references to `[[wikilinks]]`
   - Preserve the structure and insights
   - Remove any meta-commentary (e.g., "use /dist:research for more")
4. Save to `brain/personal/notes/{title}.md`
5. Confirm: "Saved to brain/personal/notes/{title}.md"

**Format:**

```yaml
---
tags:
  - type/note
  - domain/{inferred from content}
---

{content with [[wikilinks]] to claims, entities, and bridge concepts}
```

**Rules:**
- Titles should be in the same language as the content
- Always add [[wikilinks]] to entities and claims that exist in the brain
- Keep the content faithful to the original response — don't rewrite or expand
- If the user says "save the last X", find that response in conversation history
