Manage connected brains — list, add, clone, or remove.

Action: $ARGUMENTS

**Examples:**

```
/dist:brains list
/dist:brains add /path/to/brain-philosophy/
/dist:brains add https://someone.github.io/their-brain/
/dist:brains clone https://someone.github.io/their-brain/
/dist:brains remove Philosophy
```

Read `.claude/skills/distillary-brains.md` FIRST.

- **list** → show all brains from `brains.yaml` with status and source counts
- **add (local path)** → verify path exists, count sources, add to `brains.yaml`
- **add (URL)** → fetch `agent.json`, add as published brain
- **clone (URL)** → download locally for deep analysis (concept-mapping, analytics)
- **remove** → disconnect from `brains.yaml` (does not delete files)
