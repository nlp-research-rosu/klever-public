#!/usr/bin/env python3
"""Independent differential checks for HumanEval/117.

The oracle and generated implementation are imported from separate explicit
paths.  This script does not reuse any candidate proof equations.
"""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/117-select-words-audit")


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load_module("trusted_canonical", SCRATCH / "canonical.py")
generated = load_module("generated_solution", SCRATCH / "solution.py")

examples = [
    ("Mary had a little lamb", 4, ["little"]),
    ("Mary had a little lamb", 3, ["Mary", "lamb"]),
    ("simple white space", 2, []),
    ("Hello world", 4, ["world"]),
    ("Uncle sam", 3, ["Uncle"]),
]

boundaries = [
    ("", 0),
    ("", 1),
    (" ", 0),
    ("   ", 0),
    ("a", 0),
    ("A", 0),
    ("b", 0),
    ("b", 1),
    ("aeiou AEIOU", 0),
    ("b c", 1),
    (" b  a c ", 0),
    (" b  a c ", 1),
    ("abc", 2),
    ("abc ", 2),
    (" abc", 2),
    ("a  bc   DEF ", 2),
    ("Å β İ", 1),
    ("éclair Ωmega", 3),
]

checks = 0
mismatches: list[tuple[str, int, object, object]] = []


def check(s: str, n: int) -> None:
    global checks
    checks += 1
    expected = canonical.select_words(s, n)
    actual = generated.select_words(s, n)
    if actual != expected:
        mismatches.append((s, n, expected, actual))


for s, n, expected in examples:
    oracle = canonical.select_words(s, n)
    if oracle != expected:
        raise AssertionError((s, n, expected, oracle))
    check(s, n)

for s, n in boundaries:
    check(s, n)

# Exhaust all short strings around each branch: vowel/consonant, case, space,
# token start/end, repeated separators, and n below/equal/above word length.
alphabet = "aBEc "
for length in range(0, 7):
    for chars in itertools.product(alphabet, repeat=length):
        s = "".join(chars)
        for n in range(0, 8):
            check(s, n)

# A broader deterministic sample over prompt-valid letters and spaces.
rng = random.Random(117)
sample_alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ "
for _ in range(3000):
    s = "".join(rng.choice(sample_alphabet) for _ in range(rng.randrange(0, 65)))
    n = rng.randrange(0, 70)
    check(s, n)

print(f"documented_examples={len(examples)}")
print(f"boundary_cases={len(boundaries)}")
print("exhaustive_alphabet='aBEc '")
print("exhaustive_lengths=0..6")
print("exhaustive_n=0..7")
print("random_seed=117")
print("random_cases=3000")
print(f"checks={checks}")
print(f"mismatches={len(mismatches)}")
for mismatch in mismatches[:20]:
    print(f"MISMATCH {mismatch!r}")

raise SystemExit(1 if mismatches else 0)
