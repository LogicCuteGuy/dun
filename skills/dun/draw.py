#!/usr/bin/env python3
"""
dun — deterministic tarot card draw

Takes a text seed (the user's question) and draws cards deterministically.
Same seed = same draw every time — like shuffling while thinking of the same question.

Usage:
    python draw.py "เรื่องความสัมพันธ์"
    python draw.py "รัก" --count 5
    python draw.py "งาน" --json
"""

import hashlib
import random
import sys
import io
import json
import argparse

# Force UTF-8 output on Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


# ─── Deck definition ───────────────────────────────────────────────

MAJOR = [
    "The Fool", "The Magician", "The High Priestess", "The Empress",
    "The Emperor", "The Hierophant", "The Lovers", "The Chariot",
    "Strength", "The Hermit", "Wheel of Fortune", "Justice",
    "The Hanged Man", "Death", "Temperance", "The Devil",
    "The Tower", "The Star", "The Moon", "The Sun",
    "Judgement", "The World",
]

SUITS = {
    "Wands": "Fire",
    "Cups": "Water",
    "Swords": "Air",
    "Pentacles": "Earth",
}

RANKS = [
    "Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10",
    "Page", "Knight", "Queen", "King",
]

REVERSED_CUE = {
    "Wands": "blocked energy, burnout, recklessness",
    "Cups": "emotional loss, blocked creativity, emptiness",
    "Swords": "confusion, brutality, chaos",
    "Pentacles": "lost opportunity, disorganized, overwhelmed",
}


def build_deck():
    """Build a full 78-card deck."""
    deck = []
    for name in MAJOR:
        deck.append({"name": name, "type": "major", "suit": None, "rank": None})
    for suit in SUITS:
        for rank in RANKS:
            deck.append({
                "name": f"{rank} of {suit}",
                "type": "minor",
                "suit": suit,
                "rank": rank,
            })
    return deck


def seed_from_text(text):
    """Hash text to a deterministic integer seed."""
    h = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return int(h[:16], 16)


def draw(seed_text, count=3):
    """
    Draw `count` cards from a shuffled deck, seeded by `seed_text`.
    Each card has ~50% chance of being reversed.
    """
    seed = seed_from_text(seed_text)
    rng = random.Random(seed)

    deck = build_deck()
    rng.shuffle(deck)

    drawn = []
    for i in range(count):
        card = deck[i].copy()
        card["reversed"] = rng.random() < 0.5
        card["position"] = i + 1
        drawn.append(card)

    return drawn


def card_meaning(card):
    """Return upright/reversed meaning for a card (brief)."""
    name = card["name"]
    reversed = card["reversed"]
    orientation = "reversed" if reversed else "upright"

    meanings = {
        # Major Arcana
        "The Fool": ("innocence, new beginnings, free spirit", "recklessness, taken advantage of, hesitation"),
        "The Magician": ("willpower, desire, creation, manifestation", "trickery, illusions, manipulation"),
        "The High Priestess": ("intuitive, unconscious, inner voice", "lack of center, lost inner voice, repressed feelings"),
        "The Empress": ("motherhood, fertility, nature, abundance", "dependence, smothering, emptiness"),
        "The Emperor": ("authority, structure, control, fatherhood", "tyranny, rigidity, coldness"),
        "The Hierophant": ("tradition, conformity, morality, institutions", "rebellion, subversiveness, dogma"),
        "The Lovers": ("partnerships, duality, union, love", "loss of balance, one-sidedness, disharmony"),
        "The Chariot": ("direction, control, willpower, victory", "lack of control, lack of direction, aggression"),
        "Strength": ("inner strength, bravery, compassion, focus", "self-doubt, weakness, insecurity"),
        "The Hermit": ("contemplation, search for truth, inner guidance", "loneliness, isolation, lost your way"),
        "Wheel of Fortune": ("change, cycles, inevitable fate", "no control, clinging to control, bad luck"),
        "Justice": ("cause and effect, clarity, truth, fairness", "dishonesty, unaccountability, unfairness"),
        "The Hanged Man": ("sacrifice, release, new perspective", "stalling, needless sacrifice, fear of sacrifice"),
        "Death": ("end of cycle, beginnings, change, metamorphosis", "fear of change, holding on, stagnation"),
        "Temperance": ("middle path, patience, finding meaning", "extremes, excess, lack of balance"),
        "The Devil": ("addiction, materialism, attachment, shadow", "freedom, release, restoring control"),
        "The Tower": ("sudden upheaval, broken pride, disaster", "disaster avoided, delayed disaster, fear of suffering"),
        "The Star": ("hope, faith, rejuvenation, healing", "faithlessness, discouragement, insecurity"),
        "The Moon": ("unconscious, illusions, intuition, dreams", "confusion, fear, misinterpretation"),
        "The Sun": ("joy, success, celebration, positivity", "negativity, depression, sadness"),
        "Judgement": ("reflection, reckoning, awakening, calling", "lack of self-awareness, doubt, self-loathing"),
        "The World": ("fulfillment, harmony, completion", "incompletion, no closure, loose ends"),
    }

    if name in meanings:
        return meanings[name][0] if not reversed else meanings[name][1]

    # Minor arcana — suit + rank logic
    suit = card["suit"]
    rank = card["rank"]

    rank_stage = {
        "Ace": "seed of potential, new feelings",
        "2": "choice, duality, partnership",
        "3": "expansion, first growth, community",
        "4": "foundation, stability, contemplation",
        "5": "friction, conflict, competition",
        "6": "flow, harmony, transition",
        "7": "assessment, perseverance, stance",
        "8": "momentum, rapid action, mastery",
        "9": "culmination, resilience, near-end",
        "10": "completion, full cycle, accomplishment",
        "Page": "curiosity, a beginner's spark, message",
        "Knight": "action, adventure, pursuit",
        "Queen": "compassion, maturity, receptive power",
        "King": "leadership, authority, big picture",
    }

    suit_energy = {
        "Wands": "energy, drive, willpower, creativity",
        "Cups": "emotion, feelings, intuition, relationships",
        "Swords": "logic, ideas, intellect, communication",
        "Pentacles": "nature, body, material world, stability",
    }

    stage = rank_stage.get(rank, "")
    energy = suit_energy.get(suit, "")

    if reversed:
        cue = REVERSED_CUE.get(suit, "")
        return f"{stage} in {energy} — turned inward, {cue}"
    else:
        return f"{stage} in {energy}"


def format_output(cards, output_json=False):
    """Format drawn cards for display."""
    if output_json:
        result = []
        for c in cards:
            result.append({
                "position": c["position"],
                "name": c["name"],
                "reversed": c["reversed"],
                "orientation": "reversed" if c["reversed"] else "upright",
                "meaning": card_meaning(c),
            })
        return json.dumps(result, ensure_ascii=False, indent=2)

    lines = []
    labels = {1: "Past", 2: "Present", 3: "Future"} if len(cards) == 3 else {}

    for c in cards:
        pos = c["position"]
        orientation = "reversed" if c["reversed"] else "upright"
        label = labels.get(pos, f"Card {pos}")
        meaning = card_meaning(c)
        lines.append(f"[ {label} ] {c['name']} ({orientation})")
        lines.append(f"  > {meaning}")
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="dun — deterministic tarot card draw")
    parser.add_argument("seed", help="Text seed (the user's question)")
    parser.add_argument("--count", "-n", type=int, default=3, choices=[1, 3, 5, 7],
                        help="Number of cards to draw (default: 3)")
    parser.add_argument("--json", "-j", action="store_true",
                        help="Output as JSON")

    args = parser.parse_args()
    cards = draw(args.seed, args.count)
    print(format_output(cards, args.json))


if __name__ == "__main__":
    main()
