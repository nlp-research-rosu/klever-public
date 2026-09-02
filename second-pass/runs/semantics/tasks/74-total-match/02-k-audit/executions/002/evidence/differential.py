#!/usr/bin/env python3
"""Independent canonical-vs-generated differential test for HumanEval/74."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


ROOT = Path("/tmp/audit-work/74-total-match")


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load("trusted_canonical", ROOT / "canonical.py").total_match
generated = load("candidate_solution", ROOT / "solution.py").total_match


def expected_choice(left: list[str], right: list[str]) -> list[str]:
    return left if sum(map(len, left)) <= sum(map(len, right)) else right


def check(left: list[str], right: list[str], label: str) -> None:
    global checked
    trusted_result = canonical(left, right)
    generated_result = generated(left, right)
    mathematical_result = expected_choice(left, right)
    checked += 1
    if trusted_result != generated_result or generated_result != mathematical_result:
        mismatches.append((label, left, right, trusted_result, generated_result, mathematical_result))
    # Returning an equal copy would violate "return the list", so check selected-object identity.
    if trusted_result is not mathematical_result or generated_result is not mathematical_result:
        identity_mismatches.append((label, left, right))


documented = [
    ([], []),
    (["hi", "admin"], ["hI", "Hi"]),
    (["hi", "admin"], ["hi", "hi", "admin", "project"]),
    (["hi", "admin"], ["hI", "hi", "hi"]),
    (["4"], ["1", "2", "3", "4", "5"]),
]
boundaries = [
    ([], [""]),
    ([""], []),
    ([""], [""]),
    (["a"], []),
    ([], ["a"]),
    (["a"], ["b"]),
    (["aa"], ["b"]),
    (["a"], ["bb"]),
    (["", "a"], ["b", ""]),
    (["é"], ["x"]),
    (["🙂"], ["x"]),
    (["e\u0301"], ["x"]),
    (["ab", ""], ["c", "d"]),
    (["long"], ["", "", "abc"]),
]

checked = 0
mismatches: list[tuple] = []
identity_mismatches: list[tuple] = []
for index, (left, right) in enumerate(documented):
    check(left, right, f"documented-{index}")
for index, (left, right) in enumerate(boundaries):
    check(left, right, f"boundary-{index}")

# Exhaustive list pairs over a small alphabet, including empty and Unicode strings.
strings = ["", "a", "bb", "é", "🙂"]
lists = [
    list(values)
    for size in range(4)
    for values in itertools.product(strings, repeat=size)
]
for left_index, left in enumerate(lists):
    for right_index, right in enumerate(lists):
        check(left, right, f"exhaustive-{left_index}-{right_index}")

# Broader deterministic generated sample.
rng = random.Random(740074)
characters = ["a", "Z", "0", "é", "🙂", "\u0301", " "]
for index in range(10_000):
    left = [
        "".join(rng.choice(characters) for _ in range(rng.randrange(0, 9)))
        for _ in range(rng.randrange(0, 9))
    ]
    right = [
        "".join(rng.choice(characters) for _ in range(rng.randrange(0, 9)))
        for _ in range(rng.randrange(0, 9))
    ]
    check(left, right, f"generated-{index}")

print(f"DOCUMENTED_CASES {len(documented)}")
print(f"BOUNDARY_CASES {len(boundaries)}")
print(f"EXHAUSTIVE_LISTS {len(lists)}")
print(f"EXHAUSTIVE_PAIRS {len(lists) ** 2}")
print("GENERATED_CASES 10000 seed=740074 max_list_len=8 max_string_len=8")
print(f"TOTAL_CHECKS {checked}")
print(f"VALUE_MISMATCHES {len(mismatches)}")
print(f"IDENTITY_MISMATCHES {len(identity_mismatches)}")
if mismatches:
    print(f"FIRST_VALUE_MISMATCH {mismatches[0]!r}")
if identity_mismatches:
    print(f"FIRST_IDENTITY_MISMATCH {identity_mismatches[0]!r}")
raise SystemExit(1 if mismatches or identity_mismatches else 0)
