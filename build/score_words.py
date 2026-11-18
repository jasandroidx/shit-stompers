"""Scores every dictionary word for how obvious it is, and writes data/word-levels.txt.

Uses wordfreq (Zipf scale: 7 = "the", 4 = everyday word, 3 = literate, 2 = rare).
The build embeds these as one character per word, so the game can order a board
by "what would a person think of first" without shipping a 50MB data package.

    python3 -m pip install --target /tmp/wf wordfreq
    PYTHONPATH=/tmp/wf python3 build/score_words.py
"""
import os
import re

from wordfreq import zipf_frequency

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "data", "dictionary.txt")


def dict_words():
    words = open(SRC, encoding="utf-8").read().split()
    template = open(os.path.join(ROOT, "src", "game.html"), encoding="utf-8").read()
    crude = re.search(r'const CRUDE_WORDS = \("([^"]*)"\)', template).group(1).split(" ")
    seen, out = set(), []
    for w in words + [c for c in crude if len(c) <= 6]:
        if w and w not in seen:
            seen.add(w)
            out.append(w)
    return out


def level(word):
    # zipf 0-8 -> 0-16, clamped into the 16 buckets a single character can hold
    return max(0, min(15, int(round(zipf_frequency(word, "en") * 2))))


words = dict_words()
lines = ["%s %d" % (w, level(w)) for w in words]
out = os.path.join(ROOT, "data", "word-levels.txt")
open(out, "w").write("\n".join(lines) + "\n")
print("wrote", out, len(lines), "words")
for probe in ("sine", "ion", "sins", "noise", "ess", "sen", "shit", "cunt", "numpty"):
    print("  %-7s %d/15" % (probe, level(probe)))
