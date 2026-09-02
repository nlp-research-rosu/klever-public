#!/usr/bin/env python3
"""Independent candidate-versus-canonical differential test."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/54-same-chars")


def load_entry(module_name: str, source: Path):
    spec = importlib.util.spec_from_file_location(module_name, source)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {source}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.same_chars


candidate = load_entry("audited_candidate", SCRATCH / "solution.py")
canonical = load_entry("trusted_canonical", SCRATCH / "canonical.py")

documented = [
    ("eabcdzzzz", "dddzzzzzzzddeddabc", True),
    ("abcd", "dddddddabc", True),
    ("dddddddabc", "abcd", True),
    ("eabcd", "dddddddabc", False),
    ("abcd", "dddddddabce", False),
    ("eabcdzzzz", "dddzzzzzzzddddabc", False),
]

# Empty strings, equality, order/multiplicity insensitivity, unique-character
# additions on either side, and non-ASCII/code-point boundaries.
boundaries = [
    ("", "", True),
    ("", "a", False),
    ("a", "", False),
    ("a", "a", True),
    ("aa", "a", True),
    ("ab", "ba", True),
    ("ab", "abb", True),
    ("ab", "abc", False),
    ("abc", "ab", False),
    ("A", "a", False),
    (" ", "  ", True),
    ("\x00", "\x00\x00", True),
    ("é", "éé", True),
    ("e\u0301", "é", False),
    ("😀a", "a😀😀", True),
    ("😀a", "a😃", False),
]

alphabet = ("a", "b", "A", " ", "é", "😀", "\u0301", "\x00")
generated_strings = [
    "".join(chars)
    for length in range(4)
    for chars in itertools.product(alphabet, repeat=length)
]

rng = random.Random(540054)
wide_alphabet = tuple(chr(code) for code in [1, 31, 127, 255, 0x3A9, 0x20AC, 0x10348])
random_pairs = [
    (
        "".join(rng.choice(wide_alphabet) for _ in range(rng.randrange(0, 13))),
        "".join(rng.choice(wide_alphabet) for _ in range(rng.randrange(0, 13))),
    )
    for _ in range(5000)
]

mismatches = []
manual_failures = []
tested_pairs = 0

for left, right, expected in documented + boundaries:
    candidate_result = candidate(left, right)
    canonical_result = canonical(left, right)
    tested_pairs += 1
    if candidate_result != canonical_result:
        mismatches.append((left, right, canonical_result, candidate_result))
    if candidate_result is not expected or canonical_result is not expected:
        manual_failures.append(
            (left, right, expected, canonical_result, candidate_result)
        )

for left in generated_strings:
    for right in generated_strings:
        candidate_result = candidate(left, right)
        canonical_result = canonical(left, right)
        tested_pairs += 1
        if candidate_result != canonical_result:
            mismatches.append((left, right, canonical_result, candidate_result))

for left, right in random_pairs:
    candidate_result = candidate(left, right)
    canonical_result = canonical(left, right)
    tested_pairs += 1
    if candidate_result != canonical_result:
        mismatches.append((left, right, canonical_result, candidate_result))

print(f"documented_cases={len(documented)}")
print(f"boundary_cases={len(boundaries)}")
print(f"generated_strings={len(generated_strings)}")
print(f"exhaustive_generated_pairs={len(generated_strings) ** 2}")
print(f"seeded_random_pairs={len(random_pairs)} seed=540054")
print(f"tested_pairs={tested_pairs}")
print(f"candidate_canonical_mismatches={len(mismatches)}")
print(f"manual_expected_failures={len(manual_failures)}")
if mismatches:
    print(f"first_mismatches={mismatches[:10]!r}")
if manual_failures:
    print(f"first_manual_failures={manual_failures[:10]!r}")
if mismatches or manual_failures:
    raise SystemExit(1)
