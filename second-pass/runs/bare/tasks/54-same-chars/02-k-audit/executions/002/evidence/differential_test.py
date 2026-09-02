#!/usr/bin/env python3
"""Independent differential test: trusted canonical.py vs candidate solution.py."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load_module(
    "trusted_canonical",
    Path("/tmp/audit-work/54-same-chars/reference/canonical.py"),
)
candidate = load_module(
    "candidate_solution",
    Path("/tmp/audit-work/54-same-chars/candidate/solution.py"),
)

documented = [
    ("eabcdzzzz", "dddzzzzzzzddeddabc"),
    ("abcd", "dddddddabc"),
    ("dddddddabc", "abcd"),
    ("eabcd", "dddddddabc"),
    ("abcd", "dddddddabce"),
    ("eabcdzzzz", "dddzzzzzzzddddabc"),
]

boundaries = [
    ("", ""),
    ("", "a"),
    ("a", ""),
    ("a", "a"),
    ("a", "aa"),
    ("aa", "a"),
    ("ab", "ba"),
    ("ab", "abc"),
    ("abc", "ab"),
    ("\0", "\0\0"),
    ("\n", "\n"),
    ("é", "éé"),
    ("é", "e\u0301"),
    ("😀a", "a😀😀"),
    ("𐐷", "𐐷𐐷"),
]

small_alphabet = ("a", "b", "é", "😀")
small_strings = [
    "".join(chars)
    for length in range(5)
    for chars in itertools.product(small_alphabet, repeat=length)
]

rng = random.Random(540054)
random_alphabet = ("a", "b", "c", "é", "\u0301", "😀", "\0", "\n")
random_pairs = [
    (
        "".join(rng.choice(random_alphabet) for _ in range(rng.randrange(33))),
        "".join(rng.choice(random_alphabet) for _ in range(rng.randrange(33))),
    )
    for _ in range(20_000)
]

cases = list(documented)
cases.extend(boundaries)
cases.extend(itertools.product(small_strings, repeat=2))
cases.extend(random_pairs)

mismatches = []
true_count = 0
false_count = 0
for index, (left, right) in enumerate(cases):
    expected = canonical.same_chars(left, right)
    actual = candidate.same_chars(left, right)
    true_count += bool(actual)
    false_count += not actual
    if actual != expected:
        mismatches.append((index, left, right, expected, actual))
        if len(mismatches) >= 20:
            break

print(f"documented_cases={len(documented)}")
print(f"boundary_cases={len(boundaries)}")
print(
    "exhaustive_small_scope="
    f"alphabet={small_alphabet!r},max_length=4,"
    f"strings={len(small_strings)},pairs={len(small_strings) ** 2}"
)
print(
    "random_scope="
    "seed=540054,pairs=20000,max_length=32,"
    f"alphabet={random_alphabet!r}"
)
print(f"cases_executed={true_count + false_count}")
print(f"true_results={true_count}")
print(f"false_results={false_count}")
print(f"mismatches={len(mismatches)}")
for mismatch in mismatches:
    print(f"MISMATCH {mismatch!r}")

raise SystemExit(1 if mismatches else 0)
