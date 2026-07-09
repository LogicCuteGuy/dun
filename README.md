# dun

A Claude Code skill for emotionally-aware tarot fortune-telling.

> `dun` = ดูดวง (Thai for "fortune-telling") — short, easy to type, easy to invoke.

## Install

```bash
git clone https://github.com/<you>/dun.git
cp -r dun ~/.claude/skills/
```

Or symlink it instead of copying:

```bash
ln -s "$(pwd)/dun" ~/.claude/skills/dun
```

Then invoke with `/dun` and your question.

## What it does

- Draws tarot cards (default 3-card past / present / future)
- Asks 1–3 grounding questions before drawing
- Reads past sessions from `memory/` to pick up threads
- Has hard emotional-safety boundaries

## Layout

```
dun/
├── SKILL.md          main skill (Claude Code reads this)
├── cards-major.md    22 Major Arcana meanings
├── cards-minor.md    Minor Arcana (suit-based, no per-card data)
├── spreads.md        1 / 3 / 5 card layouts
├── boundaries.md     safety rules
├── memory/           personal reading history (gitignored)
└── README.md
```

## Why a skill and not a chat UI

The user's whole context lives in the skill folder. Reading past sessions, emotional memory, and tarot data co-locate. No server, no deploy, no API key to leak. `git clone && cp` is the whole install.

## Design notes

See [/dun's design intent](https://example) — or just read `boundaries.md` first.

## License

MIT.
