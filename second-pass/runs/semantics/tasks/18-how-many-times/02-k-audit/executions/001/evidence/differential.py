#!/usr/bin/env python3
"""Independent candidate/canonical differential test for HumanEval 18."""

from __future__ import annotations

import importlib.util
import itertools
import random
import sys
from pathlib import Path


def load_entry(path: str, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.how_many_times


canonical = load_entry("/reference/canonical.py", "trusted_canonical")
generated = load_entry("/candidate/solution.py", "candidate_solution")

documented_and_boundaries = [
    ("", "a"),
    ("aaa", "a"),
    ("aaaa", "aa"),
    ("", ""),
    ("a", ""),
    ("abc", ""),
    ("a", "a"),
    ("a", "b"),
    ("ab", "a"),
    ("ab", "b"),
    ("ab", "ab"),
    ("ab", "abc"),
    ("aaaaa", "aaa"),
    ("abababa", "aba"),
    ("abcabc", "bc"),
    ("🙂🙂🙂", "🙂🙂"),
    ("éée\u0301", "é"),
]


def words(alphabet: str, max_len: int):
    for length in range(max_len + 1):
        for chars in itertools.product(alphabet, repeat=length):
            yield "".join(chars)


cases = list(documented_and_boundaries)
cases.extend(
    (s, p)
    for s in words("ab", 7)
    for p in words("ab", 4)
)

rng = random.Random(180018)
alphabet = "abc🙂"
for _ in range(1000):
    s = "".join(rng.choice(alphabet) for _ in range(rng.randrange(0, 40)))
    p = "".join(rng.choice(alphabet) for _ in range(rng.randrange(0, 9)))
    cases.append((s, p))

mismatches = []
for index, (string, substring) in enumerate(cases):
    expected = canonical(string, substring)
    actual = generated(string, substring)
    if expected != actual:
        mismatches.append((index, string, substring, expected, actual))
        if len(mismatches) >= 20:
            break

print(f"python={sys.version.split()[0]}")
print(f"cases={len(cases)}")
print(f"mismatches={len(mismatches)}")
for mismatch in mismatches:
    print("MISMATCH", repr(mismatch))

raise SystemExit(1 if mismatches else 0)
