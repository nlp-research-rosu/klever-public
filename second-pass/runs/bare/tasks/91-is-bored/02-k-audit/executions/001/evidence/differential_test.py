#!/usr/bin/env python3
"""Independent differential test for HumanEval/91.

Oracle: the trusted /reference/canonical.py.
Subject: the freshly copied /tmp/audit-work/reconstruction/solution.py.
The generated corpus is deterministic and is completely determined by the
literal directed cases, alphabets, Cartesian-product bounds, and RNG seed below.
"""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_bored


canonical = load_entry("trusted_canonical", Path("/reference/canonical.py"))
generated = load_entry(
    "audited_solution", Path("/tmp/audit-work/reconstruction/solution.py")
)

directed = [
    # Documented examples.
    "Hello world",
    "The sky is blue. The sun is shining. I love this weather",
    # Empty and loop-count boundaries.
    "",
    ".",
    "...",
    "I ",
    "I",
    "I a.I b",
    # Every delimiter and repeated/trailing delimiters.
    "I a. I b",
    "I a? I b",
    "I a! I b",
    "I a.?! I b!",
    # True and false startswith branches around the exact two-character prefix.
    "I agree",
    "It is cold",
    "Island",
    " i agree",
    "\tI agree",
    "\nI agree",
    "\u00a0I agree",
    "I\tagree",
    # Whitespace immediately after a delimiter versus at the whole-input start.
    "No. I agree",
    " No. I agree",
    " I am here?You are there!  I agree",
    # Candidate's other ground proof inputs.
    "I am bored. I am still bored! Are you? I think so.",
    "It is cold. Island life! In time? I agree",
    "... ! ?  . I count!",
    "\tI tabbed.\nI newline?\rNot me!",
    "I first! No. I second?",
]

# Exhaustive short strings hit empty/non-empty, each delimiter, spaces, and
# initial-prefix boundaries.  8**0 + ... + 8**4 = 4,681 cases.
short_alphabet = ("I", "i", " ", "a", ".", "?", "!", "\t")
exhaustive = [
    "".join(chars)
    for length in range(5)
    for chars in itertools.product(short_alphabet, repeat=length)
]

# Broader deterministic representative sample, including all Python strip
# whitespace classes used by the candidate semantics.
rng = random.Random(910091)
random_alphabet = (
    "Iit abcXYZ.!?\t\n\r\f\v"
    "\u001c\u001d\u001e\u001f\u0085\u00a0\u1680"
    "\u2000\u2001\u2002\u2003\u2004\u2005\u2006\u2007"
    "\u2008\u2009\u200a\u2028\u2029\u202f\u205f\u3000"
)
random_cases = [
    "".join(rng.choice(random_alphabet) for _ in range(rng.randrange(0, 81)))
    for _ in range(5_000)
]

cases = directed + exhaustive + random_cases
mismatches = []
for index, text in enumerate(cases):
    want = canonical(text)
    got = generated(text)
    if got != want:
        mismatches.append((index, text, want, got))

print("oracle=/reference/canonical.py:is_bored")
print("subject=/tmp/audit-work/reconstruction/solution.py:is_bored")
print(f"directed_cases={len(directed)}")
print(
    "exhaustive_cases="
    f"{len(exhaustive)} alphabet={short_alphabet!r} lengths=0..4"
)
print(
    "random_cases="
    f"{len(random_cases)} seed=910091 lengths=0..80 "
    f"alphabet={random_alphabet!r}"
)
print(f"total_cases={len(cases)}")
print(f"mismatch_count={len(mismatches)}")
for index, text, want, got in mismatches[:25]:
    print(
        f"MISMATCH index={index} input={text!r} "
        f"canonical={want} generated={got}"
    )

raise SystemExit(1 if mismatches else 0)
