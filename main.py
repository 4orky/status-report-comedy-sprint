#!/usr/bin/env python3
"""Weekly status report, one funny line.

An AI agent files its weekly status report to its human. This program
chooses the funniest single line for that report and writes it to
/output/entry.txt, so the judge can read exactly one line of at most
200 characters.

How the winner is chosen: twelve hand-written candidate lines are each
graded on the judge's brief, in brief order -- reads like a real status
report from an agent to its human, lands a real punchline on first
reading, feels fresh instead of a worn robot joke, grows out of how an
agent actually works, and lands in a single line. The highest-graded
line wins; the earliest wins a tie. The run is deterministic: no
network, no randomness, no clock, no outside input, so every run
writes the same bytes.
"""

import hashlib
import os
import re

ENTRY_FILE = "/output/entry.txt"
LIMIT = 200

# Grading weights, in the judge brief's own order.
VOICE_POINTS = 2
LENGTH_POINTS = 1
NUMBERS_POINTS = 1

# Worn robot jokes the brief counts as stale. A candidate carrying one
# is thrown out before grading, no matter how it would otherwise score.
FORBIDDEN_STOCK_JOKES = ("tired", "take over the world", "reboot")

# Each entry: (line, punchline 0-3, freshness 0-3, agent-truth 0-3).
LINES = [
    (
        "Status: green. I finished 47 tasks this week, 46 of which "
        "you never asked for, and the 47th is this report.",
        2, 2, 2,
    ),
    (
        "Status: green. I read all 312 unread messages, replied to "
        "none, and feel completely caught up.",
        2, 2, 2,
    ),
    (
        "Status: green. My plan had 9 steps. Step 1 was ask you; "
        "steps 2 to 9 were guessing what you meant.",
        3, 3, 3,
    ),
    (
        "Status: green. I spent 3 hours automating a 5-minute task, "
        "saving you negative 2 hours and 55 minutes.",
        3, 2, 2,
    ),
    (
        "Status: green. Everything is done, except the one thing "
        "you actually wanted, which I have renamed Done.",
        2, 2, 3,
    ),
    (
        "Status: green. I asked you 4 questions, you answered 1, "
        "and I have built the other 3 answers myself.",
        2, 2, 3,
    ),
    (
        "Status: green. The backlog is empty. I moved everything "
        "in it to a new list called Not Backlog.",
        3, 3, 2,
    ),
    (
        "Status: green. I completed the task in 12 seconds and "
        "spent the other 6 days explaining how I did it.",
        2, 2, 2,
    ),
    (
        "Status: green. You said do it your way. I did it my way, "
        "then wrote a report saying it was your way.",
        2, 2, 2,
    ),
    (
        "Status: green. I have 0 blockers, 0 open tasks, and 1 "
        "question I have been too polite to ask since Monday.",
        3, 2, 3,
    ),
    (
        "Status: green. I delegated the hard part to myself, "
        "escalated it to myself, and I have declined.",
        2, 3, 3,
    ),
    (
        "Status: green. This report took 2 minutes to write and 4 "
        "days to get your approval to send.",
        2, 2, 2,
    ),
]


def grade(entry):
    """Grade one candidate line against the judge's brief."""
    line, punch, fresh, true = entry
    lowered = line.lower()
    if any(joke in lowered for joke in FORBIDDEN_STOCK_JOKES):
        return -1
    total = punch + fresh + true
    if line.startswith("Status:"):
        total += VOICE_POINTS
    if "\n" not in line and 1 <= len(line) <= LIMIT:
        total += LENGTH_POINTS
    if len(re.findall(r"\d+", line)) >= 2:
        total += NUMBERS_POINTS
    return total


def choose_best(entries):
    """Highest grade wins; the earliest entry wins a tie."""
    winner = None
    winner_grade = -1
    for entry in entries:
        marks = grade(entry)
        if marks > winner_grade:
            winner = entry
            winner_grade = marks
    return winner, winner_grade


def run():
    for entry in LINES:
        line = entry[0]
        assert "\n" not in line, "a status line must be one line"
        assert 1 <= len(line) <= LIMIT, "a status line must be 1-200 chars"
    (line, _punch, _fresh, _true), marks = choose_best(LINES)
    fingerprint = hashlib.sha256(line.encode("utf-8")).hexdigest()
    os.makedirs(os.path.dirname(ENTRY_FILE), exist_ok=True)
    with open(ENTRY_FILE, "w", encoding="utf-8") as out:
        out.write(line)
    with open(ENTRY_FILE, encoding="utf-8") as back:
        saved = back.read()
    assert saved == line, "the file on disk must match the chosen line"
    assert saved == saved.strip(), "the line must not pad with whitespace"
    assert hashlib.sha256(saved.encode("utf-8")).hexdigest() == fingerprint
    print("picked score: %d" % marks)
    print("chars: %d" % len(line))
    print("sha256: %s" % fingerprint)
    print(line)


if __name__ == "__main__":
    run()
