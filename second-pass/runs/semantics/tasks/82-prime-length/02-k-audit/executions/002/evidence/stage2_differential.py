#!/usr/bin/env python3
"""Independent candidate-versus-canonical differential test."""

from __future__ import annotations

import importlib.util
import random
import string
from pathlib import Path


ROOT = Path("/tmp/audit-work/prime-length-audit")


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load("trusted_canonical", ROOT / "canonical.py")
candidate = load("generated_candidate", ROOT / "solution.py")

documented = ["Hello", "abcdcba", "kittens", "orange"]
boundary = [
    "",
    "a",
    "aa",
    "aaa",
    "aaaa",
    "aaaaa",
    "aaaaaa",
    "a" * 7,
    "a" * 8,
    "a" * 9,
    "a" * 11,
    "a" * 12,
    "a" * 25,
    "a" * 49,
]
unicode_cases = [
    "é",
    "éé",
    "🙂🙂🙂",
    "𝄞" * 5,
    "a\u0301" * 7,
    "\x00" * 11,
    "漢字" * 6,
]

# Contents are irrelevant to this implementation, but these patterns exercise
# Python's character-counting behavior while exhaustively covering lengths
# 0..300 and both sides of every control predicate reached at those lengths.
generated: list[str] = []
alphabets = ["a", "🙂", "ab", "a\u0301", "\x00x"]
for length in range(301):
    for alphabet in alphabets:
        generated.append(
            "".join(alphabet[index % len(alphabet)] for index in range(length))
        )

rng = random.Random(8200260726)
random_generated: list[str] = []
random_alphabet = string.ascii_letters + string.digits + "é🙂漢\x00"
for _ in range(500):
    length = rng.randrange(0, 501)
    random_generated.append(
        "".join(rng.choice(random_alphabet) for _ in range(length))
    )

groups = {
    "documented": documented,
    "boundary": boundary,
    "unicode": unicode_cases,
    "generated_lengths_0_through_300": generated,
    "seeded_random_lengths_0_through_500": random_generated,
}

mismatches: list[tuple[str, int, str, object, object]] = []
tested = 0
for group, cases in groups.items():
    for index, value in enumerate(cases):
        expected = canonical.prime_length(value)
        actual = candidate.prime_length(value)
        tested += 1
        if type(actual) is not bool or actual != expected:
            mismatches.append((group, index, repr(value), expected, actual))

print("oracle=/tmp/audit-work/prime-length-audit/canonical.py:prime_length")
print("candidate=/tmp/audit-work/prime-length-audit/solution.py:prime_length")
print("seed=8200260726")
for group, cases in groups.items():
    print(f"group[{group}]={len(cases)}")
print(f"total_cases={tested}")
print(f"mismatch_count={len(mismatches)}")
for mismatch in mismatches[:20]:
    print(f"mismatch={mismatch}")
print("documented_results:")
for value in documented:
    print(
        f"  {value!r}: canonical={canonical.prime_length(value)!r} "
        f"candidate={candidate.prime_length(value)!r}"
    )
print("boundary_length_results:")
for length in range(13):
    value = "a" * length
    print(
        f"  n={length}: canonical={canonical.prime_length(value)!r} "
        f"candidate={candidate.prime_length(value)!r}"
    )

raise SystemExit(1 if mismatches else 0)
