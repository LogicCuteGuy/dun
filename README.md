# dun

A Claude Code skill for **structured reflection with a tarot frame** — not prediction, not therapy, but a single session of being heard with real psych grounding.

> `dun` = ดูดวง (Thai for "fortune-telling") — short, easy to type, easy to invoke.

## What it does

- Up to **7 relentless grounding probes** before drawing cards (one at a time, with recommended answers)
- Reads from **real psych science**: CBT distortions, IFS-lite, somatic awareness, polyvagal-style window of tolerance
- Default 3-card Past / Present / Future spread
- Reads past sessions from `memory/` to pick up threads
- Hard emotional-safety boundaries: crisis > cards, never fabricate, never promise outcomes
- Default mode: **healing** (reflection). Predictive mode only when user explicitly asks.

## Install

```bash
git clone https://github.com/<you>/dun.git
cp -r dun ~/.claude/skills/
```

Or symlink (single source of truth):

```bash
ln -s "$(pwd)/dun" ~/.claude/skills/dun
```

Then invoke with `/dun` and your question.

## Layout

```
dun/
├── SKILL.md          main skill — phase flow + entry point
├── physics.md        real psych grounding (CBT, IFS, somatic, window)
├── questions.md      probe protocol — one question at a time
├── healing.md        what healing can/can't be in this context
├── cards-major.md    22 Major Arcana meanings
├── cards-minor.md    Minor Arcana (suit-based)
├── spreads.md        1 / 3 / 5 / 7-card layouts
├── boundaries.md     crisis, no fabrication, scope, window of tolerance
├── memory/           gitignored, personal reading history
└── README.md
```

## Read in this order (for the curious implementer)

1. `SKILL.md` — flow
2. `physics.md` — *why* it works
3. `questions.md` — *how* to ask
4. `healing.md` — *what* it does and doesn't do
5. `boundaries.md` — *where* to stop

## What it explicitly is not

- ❌ Not therapy. Single-session reflection only.
- ❌ Not prediction. Reads energy, not fate.
- ❌ Not a chatbot persona. A skill that lives in your existing Claude Code session.

## Why a skill and not a chat UI

The user's whole context lives in the skill folder. Reading past sessions, emotional memory, and tarot data co-locate. No server, no deploy, no API key to leak. `git clone && cp` is the whole install.

## License

MIT.
