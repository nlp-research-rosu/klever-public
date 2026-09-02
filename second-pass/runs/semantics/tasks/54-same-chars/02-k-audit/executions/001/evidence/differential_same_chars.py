#!/usr/bin/env python3
"""Independent differential audit for HumanEval 54 same_chars."""

from __future__ import annotations

import importlib.util
import itertools
import json
import random
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.same_chars


canonical = load_entry(
    "trusted_canonical", Path("/tmp/audit-work/trusted/canonical.py")
)
candidate = load_entry(
    "candidate_solution", Path("/tmp/audit-work/candidate-source/solution.py")
)

documented = [
    ("eabcdzzzz", "dddzzzzzzzddeddabc", True),
    ("abcd", "dddddddabc", True),
    ("dddddddabc", "abcd", True),
    ("eabcd", "dddddddabc", False),
    ("abcd", "dddddddabce", False),
    ("eabcdzzzz", "dddzzzzzzzddddabc", False),
]

# Outcome and set-relation boundaries, plus representative character classes.
curated = [
    ("", "", True),
    ("", "a", False),
    ("a", "", False),
    ("a", "a", True),
    ("a", "aaaa", True),
    ("ab", "ba", True),
    ("ab", "a", False),
    ("a", "ab", False),
    ("ab", "cd", False),
    ("Aa", "aA", True),
    ("Aa", "aa", False),
    (" \t", "\t ", True),
    ("\x00a", "a\x00\x00", True),
    ("é", "éé", True),
    ("é", "e", False),
    ("🙂a", "a🙂🙂", True),
]

mismatches: list[tuple[str, str, object, object]] = []
checked = 0


def check(left: str, right: str, expected: bool | None = None) -> None:
    global checked
    ref = canonical(left, right)
    got = candidate(left, right)
    checked += 1
    if ref != got or (expected is not None and (ref != expected or got != expected)):
        mismatches.append((left, right, ref, got))


print("DOCUMENTED_AND_CURATED_RESULTS")
for left, right, expected in documented + curated:
    check(left, right, expected)
    print(
        json.dumps(
            {
                "s0": left,
                "s1": right,
                "expected": expected,
                "canonical": canonical(left, right),
                "candidate": candidate(left, right),
            },
            ensure_ascii=True,
            sort_keys=True,
        )
    )

# Exhaust every pair of strings of length 0..4 over a three-character alphabet.
small_strings = [
    "".join(chars)
    for length in range(5)
    for chars in itertools.product("ab!", repeat=length)
]
for left in small_strings:
    for right in small_strings:
        check(left, right)

# Deterministic broader sample, including non-ASCII and NUL.
rng = random.Random(540054)
alphabet = ["a", "b", "z", "A", "0", " ", "\x00", "é", "🙂"]
for _ in range(2000):
    left = "".join(rng.choice(alphabet) for _ in range(rng.randrange(0, 25)))
    right = "".join(rng.choice(alphabet) for _ in range(rng.randrange(0, 25)))
    check(left, right)

print(f"SMALL_STRING_COUNT={len(small_strings)}")
print(f"EXHAUSTIVE_PAIR_COUNT={len(small_strings) ** 2}")
print("RANDOM_SEED=540054")
print("RANDOM_PAIR_COUNT=2000")
print(f"TOTAL_CHECKS={checked}")
print(f"MISMATCH_COUNT={len(mismatches)}")
if mismatches:
    for mismatch in mismatches[:20]:
        print("MISMATCH", repr(mismatch))
    raise SystemExit(1)
