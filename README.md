# dun-skills

Tarot-based structured reflection skills for Claude Code.

## What it does

Structured reflection with a tarot frame — not prediction, not therapy, but a single session of being heard with real psych grounding.

- Up to **7 relentless grounding probes** before drawing cards
- Real psych science: CBT distortions, IFS-lite, somatic awareness, window of tolerance
- Deterministic card draw from user's own words (`draw.py`)
- Default 3-card Past / Present / Future spread
- Reads past sessions from `memory/` to pick up threads
- Hard emotional-safety boundaries: crisis > cards, never fabricate, never promise outcomes
- Default mode: **healing** (reflection). Predictive mode only when user explicitly asks.

## Install

### With `npx skills` (Recommended)

```bash
npx skills add your-username/dun-skills
```

### Alternative — Bash script

Symlink every skill into `~/.claude/skills/`:

```bash
./scripts/link-skills.sh
```

List every `SKILL.md` in the repo:

```bash
./scripts/list-skills.sh
```

## Layout

```
dun-skills/
├── .claude-plugin/plugin.json
├── CLAUDE.md
├── README.md
├── scripts/
│   ├── link-skills.sh
│   └── list-skills.sh
├── skills/
│   └── misc/
│       └── dun/
│           ├── SKILL.md
│           ├── draw.py
│           ├── cards-major.md
│           ├── cards-minor.md
│           ├── spreads.md
│           ├── physics.md
│           ├── questions.md
│           ├── healing.md
│           ├── boundaries.md
│           └── memory/
└── README.md
```

## Read in this order

1. `skills/misc/dun/SKILL.md` — flow + persona
2. `skills/misc/dun/physics.md` — *why* it works
3. `skills/misc/dun/questions.md` — *how* to ask
4. `skills/misc/dun/healing.md` — *what* it does and doesn't
5. `skills/misc/dun/boundaries.md` — *where* to stop

## What it explicitly is not

- ❌ Not therapy. Single-session reflection only.
- ❌ Not prediction. Reads energy, not fate.
- ❌ Not a chatbot persona. A skill that lives in your existing Claude Code session.

## License

MIT.
