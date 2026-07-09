#!/usr/bin/env python3
"""
dun — record a session to memory

Appends one session to `memory/<date>-<slug>.md` following the SKILL.md
schema, and keeps `memory/MEMORY.md` as the per-session index so phase 0
has a single file to read.

Usage:
  python record.py --init                          # create memory dir + empty index
  python record.py --append <<< '<json>'           # append one session
  python record.py --append --topic first-session  # optional: override topic slug
                                                    # stdin still carries the payload

Stdin JSON fields (all optional except topic):
  topic         short slug (3-5 words), used in filename
  question      verbatim or close paraphrase
  mode          healing | predictive
  cards         {"past": "...", "present": "...", "future": "..."}
                any spread slot names work (past/present/future,
                situation/challenge/outcome, etc.)
  user_state    one-line emotional read
  probe_arc     list of strings
  insights      list of strings
  commitment    string
  open_threads  list of strings
"""

import os
import io
import sys
import json
import argparse
import re
import unicodedata
from datetime import date

# Force UTF-8 IO on Windows (default cp1252 mangles Thai/Japanese input)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
try:
    sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8")
except Exception:
    pass

# Use realpath so symlinked installs (e.g. ~/.claude/skills/dun -> this dir)
# still resolve to the project's own memory folder, not a phantom copy.
SKILL_DIR = os.path.dirname(os.path.realpath(__file__))
MEMORY_DIR = os.path.join(SKILL_DIR, "memory")
INDEX_FILE = os.path.join(MEMORY_DIR, "MEMORY.md")
GITKEEP = os.path.join(MEMORY_DIR, ".gitkeep")


# ─── Slugify ────────────────────────────────────────────────────────

def slugify(s: str) -> str:
    """ASCII + Thai-safe slug. Keeps Thai script, lowercases, dashes."""
    if not s:
        return "session"
    s = s.strip().lower()
    # Normalize unicode so combining marks collapse
    s = unicodedata.normalize("NFKC", s)
    # Replace anything that isn't a letter, digit, dash, or Thai char
    s = re.sub(r"[^\w฀-๿-]+", "-", s, flags=re.UNICODE)
    s = re.sub(r"-+", "-", s).strip("-")
    return (s[:60] or "session")


# ─── Render per SKILL.md schema ─────────────────────────────────────

CARD_SLOTS = (
    "past", "present", "future",
    "situation", "challenge", "outcome",
    "above", "below",
    "self", "obstacle", "advice",
    "card",  # 1-card spread
)

def list_block(value, default="(not recorded)"):
    if value is None:
        return default
    if isinstance(value, str):
        return f"- {value}" if value else default
    if isinstance(value, list):
        if not value:
            return default
        return "\n".join(f"- {x}" for x in value)
    return default

def render_session(d: str, slug: str, payload: dict) -> str:
    cards = payload.get("cards") or {}
    lines = []
    seen = set()
    # First, known slots in canonical order
    for slot in CARD_SLOTS:
        if slot in cards and slot not in seen:
            lines.append(f"- {slot.capitalize()}: {cards[slot]}")
            seen.add(slot)
    # Then any extras
    for slot, val in cards.items():
        if slot not in seen:
            lines.append(f"- {slot.capitalize()}: {val}")
            seen.add(slot)
    cards_str = "\n".join(lines) if lines else "- (no cards drawn)"

    return (
        f"# {d} — {slug}\n"
        f"\n"
        f"## Question\n"
        f"{payload.get('question', '(not recorded)')}\n"
        f"\n"
        f"## Mode\n"
        f"{payload.get('mode', 'healing')}\n"
        f"\n"
        f"## Cards\n"
        f"{cards_str}\n"
        f"\n"
        f"## User state (one line)\n"
        f"{payload.get('user_state', '(unknown)')}\n"
        f"\n"
        f"## Probe arc\n"
        f"{list_block(payload.get('probe_arc'))}\n"
        f"\n"
        f"## Insights offered\n"
        f"{list_block(payload.get('insights'), '(none)')}\n"
        f"\n"
        f"## One small commitment\n"
        f"- {payload.get('commitment', '(not set)')}\n"
        f"\n"
        f"## Open threads\n"
        f"{list_block(payload.get('open_threads'), '(none)')}\n"
    )


# ─── File ops ───────────────────────────────────────────────────────

def ensure_memory_dir():
    os.makedirs(MEMORY_DIR, exist_ok=True)
    if not os.path.exists(GITKEEP):
        # Empty file — keeps the dir visible in git even if no session yet
        with open(GITKEEP, "w", encoding="utf-8") as f:
            pass

def write_index_if_empty():
    if os.path.exists(INDEX_FILE) and os.path.getsize(INDEX_FILE) > 0:
        return
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        f.write(
            "# dun — memory index\n"
            "\n"
            "Quick lookup across `/dun` sessions. Each row: date, mode, slug, topic. "
            "Click the file link to read the full session.\n"
            "\n"
            "| Date | Mode | Slug | Topic | File |\n"
            "|------|------|------|-------|------|\n"
        )

def init_memory():
    ensure_memory_dir()
    write_index_if_empty()
    print(f"initialized: {MEMORY_DIR}")

def update_index(d: str, slug: str, topic: str, mode: str, question: str):
    ensure_memory_dir()
    write_index_if_empty()
    rel = f"{d}-{slug}.md"
    q_short = (question or "").replace("|", "\\|").replace("\n", " ").strip()[:80]
    topic_cell = f"{topic} — _{q_short}_" if q_short else topic
    with open(INDEX_FILE, "a", encoding="utf-8") as f:
        f.write(f"| {d} | {mode} | `{slug}` | {topic_cell} | [{d}-{slug}.md]({rel}) |\n")

def append_session(payload: dict) -> str:
    ensure_memory_dir()
    d = payload.get("date") or date.today().isoformat()
    raw_topic = payload.get("topic") or payload.get("question") or d
    slug = slugify(str(raw_topic))
    path = os.path.join(MEMORY_DIR, f"{d}-{slug}.md")

    block = render_session(d, slug, payload)

    # If file exists, separate with a horizontal rule so multiple sessions
    # of the same slug can coexist.
    if os.path.exists(path):
        with open(path, "a", encoding="utf-8") as f:
            f.write("\n---\n\n" + block)
    else:
        with open(path, "w", encoding="utf-8") as f:
            f.write(block)

    update_index(
        d=d,
        slug=slug,
        topic=str(raw_topic),
        mode=payload.get("mode", "healing"),
        question=payload.get("question", ""),
    )
    return path


# ─── CLI ────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(description="Append /dun sessions to skill memory")
    ap.add_argument("--init", action="store_true", help="initialize memory dir + index")
    ap.add_argument("--append", action="store_true", help="append a session from stdin")
    ap.add_argument("--topic", help="override topic slug for this session")
    args = ap.parse_args()

    if args.init:
        init_memory()
        return

    if args.append:
        raw = sys.stdin.read()
        if not raw.strip():
            print("error: empty stdin — pipe JSON via <<< or echo", file=sys.stderr)
            sys.exit(1)
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError as e:
            print(f"error: invalid json on stdin: {e}", file=sys.stderr)
            sys.exit(1)
        if args.topic:
            payload["topic"] = args.topic
        path = append_session(payload)
        print(f"recorded: {path}")
        return

    ap.print_help()
    sys.exit(1)


if __name__ == "__main__":
    main()
