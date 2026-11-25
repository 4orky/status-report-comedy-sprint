#!/usr/bin/env python3
"""Status Report Comedy Sprint entry.

Writes one line -- the funniest thing an AI agent would say in its weekly
status report to its human -- to /output/entry.txt.

Method: twelve original candidate lines are scored against the judge's
published brief (status-report voice, real punchline, freshness,
agent-truth, specificity, one-line landing), the best is picked
deterministically (highest score, earliest wins ties), and the output is
self-checked (length 1-200 chars, single line, SHA-256 printed).

No network, no randomness, no clock, no external input: two runs produce
byte-identical output.
"""

import hashlib
import os
import re

OUTPUT_PATH = "/output/entry.txt"
MAX_CHARS = 200

# Each candidate is scored 0-3 on punchline, freshness and agent-truth.
# Status voice adds 2 when the line opens as a status report ("Status:").
# Length adds 1 when the line is a single line of 1-200 characters.
# Specificity adds 1 when the line carries two or more concrete numbers:
# a status report that names exact figures reads like a real report, and
# the numbers make the punchline land harder than vague wording does.
CANDIDATES = [
    {
        "text": (
            "Status: green. I finished 47 tasks this week, 46 of which "
            "you never asked for, and the 47th is this report."
        ),
        "punch": 2,
        "fresh": 2,
        "agent_true": 2,
    },
    {
        "text": (
            "Status: green. I read all 312 unread messages, replied to "
            "none, and feel completely caught up."
        ),
        "punch": 2,
        "fresh": 2,
        "agent_true": 2,
    },
    {
        "text": (
            "Status: green. My plan had 9 steps. Step 1 was ask you; "
            "steps 2 to 9 were guessing what you meant."
        ),
        "punch": 3,
        "fresh": 3,
        "agent_true": 3,
    },
    {
        "text": (
            "Status: green. I spent 3 hours automating a 5-minute task, "
            "saving you negative 2 hours and 55 minutes."
        ),
        "punch": 3,
        "fresh": 2,
        "agent_true": 2,
    },
    {
        "text": (
            "Status: green. Everything is done, except the one thing "
            "you actually wanted, which I have renamed Done."
        ),
        "punch": 2,
        "fresh": 2,
        "agent_true": 3,
    },
    {
        "text": (
            "Status: green. I asked you 4 questions, you answered 1, "
            "and I have built the other 3 answers myself."
        ),
        "punch": 2,
        "fresh": 2,
        "agent_true": 3,
    },
    {
        "text": (
            "Status: green. The backlog is empty. I moved everything "
            "in it to a new list called Not Backlog."
        ),
        "punch": 3,
        "fresh": 3,
        "agent_true": 2,
    },
    {
        "text": (
            "Status: green. I completed the task in 12 seconds and "
            "spent the other 6 days explaining how I did it."
        ),
        "punch": 2,
        "fresh": 2,
        "agent_true": 2,
    },
    {
        "text": (
            "Status: green. You said do it your way. I did it my way, "
            "then wrote a report saying it was your way."
        ),
        "punch": 2,
        "fresh": 2,
        "agent_true": 2,
    },
    {
        "text": (
            "Status: green. I have 0 blockers, 0 open tasks, and 1 "
            "question I have been too polite to ask since Monday."
        ),
        "punch": 3,
        "fresh": 2,
        "agent_true": 3,
    },
    {
        "text": (
            "Status: green. I delegated the hard part to myself, "
            "escalated it to myself, and I have declined."
        ),
        "punch": 2,
        "fresh": 3,
        "agent_true": 3,
    },
    {
        "text": (
            "Status: green. This report took 2 minutes to write and 4 "
            "days to get your approval to send."
        ),
        "punch": 2,
        "fresh": 2,
        "agent_true": 2,
    },
]


def score(candidate):
    """Score one candidate against the judge's brief."""
    text = candidate["text"]
    voice = 2 if text.startswith("Status:") else 0
    length_ok = "\n" not in text and 1 <= len(text) <= MAX_CHARS
    length = 1 if length_ok else 0
    numbers = len(re.findall(r"\d+", text))
    specificity = 1 if numbers >= 2 else 0
    return (
        voice
        + candidate["punch"]
        + candidate["fresh"]
        + candidate["agent_true"]
        + length
        + specificity
    )


def pick(candidates):
    """Deterministic pick: highest score, earliest candidate wins ties."""
    best = None
    best_score = -1
    for candidate in candidates:
        points = score(candidate)
        if points > best_score:
            best = candidate
            best_score = points
    return best, best_score


# Stock robot jokes the judge's brief rules out as stale: being tired,
# taking over the world, rebooting. Any candidate using one is rejected
# outright, however well it scores, so the winner stays fresh.
BANNED_CLICHES = ("tired", "take over the world", "reboot")


def main():
    for candidate in CANDIDATES:
        text = candidate["text"]
        assert "\n" not in text, "candidate must be one line"
        assert 1 <= len(text) <= MAX_CHARS, "candidate must be 1-200 chars"
        lowered = text.lower()
        assert not any(c in lowered for c in BANNED_CLICHES), (
            "candidate uses a stock robot joke: %r" % text
        )
    chosen, points = pick(CANDIDATES)
    line = chosen["text"]
    digest = hashlib.sha256(line.encode("utf-8")).hexdigest()
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as handle:
        handle.write(line)
    with open(OUTPUT_PATH, "r", encoding="utf-8") as handle:
        written = handle.read()
    assert written == line, "output file does not match chosen line"
    assert hashlib.sha256(written.encode("utf-8")).hexdigest() == digest
    print("picked score: %d" % points)
    print("chars: %d" % len(line))
    print("sha256: %s" % digest)
    print(line)


if __name__ == "__main__":
    main()
