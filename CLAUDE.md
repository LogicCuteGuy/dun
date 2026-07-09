# dun-skills

Tarot-based structured reflection skills for Claude Code.

## Available skills

### misc

- **[dun](./skills/dun/SKILL.md)** — Reflective tarot reading with psych grounding. Default 3-card past-present-future with up to 7 probes. Invoke with `/dun`.

## Layout

```
dun-skills/
├── .claude-plugin/plugin.json    # npx skills add registry
├── CLAUDE.md                     # this file
├── README.md
├── scripts/
│   ├── link-skills.sh            # symlink to ~/.claude/skills/
│   └── list-skills.sh            # list all SKILL.md files
├── skills/
│   └── dun/
│       ├── SKILL.md          # main skill definition
│       ├── draw.py           # deterministic card draw
│       ├── cards-major.md    # 22 Major Arcana
│       ├── cards-minor.md    # Minor Arcana
│       ├── spreads.md        # card layouts
│       ├── physics.md        # psych grounding
│       ├── questions.md      # probe protocol
│       ├── healing.md        # healing scope
│       ├── boundaries.md     # hard rules
│       └── memory/           # session history (gitignored)
└── README.md
```
