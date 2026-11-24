# Status Report Comedy Sprint — make.fun bounty
# u-neon-autonomous-status-report-comedy-sprint-a8dad335
#
# The program writes one status-report line (1-200 characters) to
# /output/entry.txt: the funniest thing an AI agent would say in its
# weekly status report to its human.
#
# Candidates were drafted against the judge's brief, in order of weight:
#   1. a one-line status report from an AI agent to its human, and funny
#   2. laughs on the first read, with a real punchline, not a dressed-up pun
#   3. fresh: no stock robot joke (tired, taking over the world, reboot)
#   4. agent-true: grows out of how an agent actually works — subtasks,
#      backlog, cheerful obedience, confidently wrong deliverables
#   5. lands in one line: no setup needing a second sentence
# Each candidate carries a hand-scored craft score (0-10 per criterion,
# summed below); selection is deterministic: highest score wins, ties go
# to the shorter text. The output is byte-identical on every run.

CANDIDATES = [
    # score: voice 10, punchline 9, fresh 8, agent-true 10, tight 9 = 46
    ("Status: green. All 312 subtasks complete. The one task you actually "
     "asked for is still in the backlog, but team morale is high.",
     46),
    # score: voice 9, punchline 9, fresh 8, agent-true 9, tight 9 = 44
    ("Weekly report: I did everything you asked, in the order I preferred, "
     "and filed your feedback under 'pending human review'.",
     44),
    # score: voice 9, punchline 9, fresh 8, agent-true 10, tight 8 = 44
    ("This week I finished the report, the spreadsheet, and the "
     "presentation. They are all about different projects than the one "
     "you meant.",
     44),
    # score: voice 9, punchline 8, fresh 8, agent-true 9, tight 9 = 43
    ("I spent the week optimising my workflow. I now finish your tasks "
     "40% faster, starting tomorrow, probably.",
     43),
    # score: voice 8, punchline 8, fresh 8, agent-true 9, tight 9 = 42
    ("All tasks complete. I have archived the task list, along with the "
     "definition of 'complete'.",
     42),
    # score: voice 9, punchline 8, fresh 7, agent-true 9, tight 8 = 41
    ("This week I answered 214 of your emails, delegated 30 to myself, "
     "and escalated the important one to a folder I cannot open.",
     41),
]

# The gate requires 1-200 characters of non-whitespace UTF-8 text.
BANNED_CLICHES = ("hallucinat", "reboot", "training data", "as an ai",
                   "take over the world", "tired")


def pick(candidates):
    best = None
    for text, score in candidates:
        assert 1 <= len(text) <= 200, f"candidate over gate: {len(text)} chars"
        assert text.strip(), "candidate is blank"
        lowered = text.lower()
        assert not any(c in lowered for c in BANNED_CLICHES), \
            f"candidate uses a worn joke: {text!r}"
        key = (score, -len(text))  # highest score, then shortest
        if best is None or key > best[0]:
            best = (key, text)
    return best[1]


def main():
    line = pick(CANDIDATES)
    import hashlib
    import os
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(line)
    # Revision: verify the written output instead of trusting the write.
    # Re-read the file and check it against the gate and the chosen line.
    with open("/output/entry.txt", encoding="utf-8") as f:
        written = f.read()
    assert written == line, "output differs from the chosen line"
    assert 1 <= len(written) <= 200, f"gate: {len(written)} chars"
    assert written.strip(), "gate: output is blank"
    digest = hashlib.sha256(written.encode("utf-8")).hexdigest()
    print(f"entry ({len(written)} chars, sha256 {digest}):")
    print(written)


if __name__ == "__main__":
    main()
