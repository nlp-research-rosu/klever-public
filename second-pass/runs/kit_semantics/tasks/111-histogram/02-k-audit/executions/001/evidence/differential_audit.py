#!/usr/bin/env python3
"""Independent canonical-vs-candidate differential test for HumanEval 111."""

from __future__ import annotations

import importlib.util
import itertools
import random
import re
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/111-histogram-audit")


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.histogram


canonical = load_function("trusted_canonical", SCRATCH / "canonical.py")
candidate = load_function("candidate_solution", SCRATCH / "solution.py")

examples = [
    "a b c",
    "a b b a",
    "a b c a b",
    "b b b b a",
    "",
]

# Empty and boundary cases, every branch direction, repeated-key updates,
# alphabet endpoints, ties, unique maxima, and spacing variations.
directed = examples + [
    " ",
    "   ",
    "a",
    "z",
    "a z",
    "a a",
    "z z a",
    "a z z a",
    "a a b c",
    "a b c c",
    "a  b",
    "  a b  ",
    "a   a   z",
    "ab",
    "a bc",
    "aa bb aa",
]

alphabet = "abc "
exhaustive = [
    "".join(chars)
    for length in range(0, 8)
    for chars in itertools.product(alphabet, repeat=length)
]

rng = random.Random(111)
generated_intended = []
for _ in range(1000):
    token_count = rng.randrange(0, 81)
    generated_intended.append(
        " ".join(rng.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(token_count))
    )

cases = list(dict.fromkeys(directed + exhaustive + generated_intended))


def strict_documented_shape(text: str) -> bool:
    """Single lowercase-letter tokens separated by one ASCII space."""
    return text == "" or re.fullmatch(r"[a-z](?: [a-z])*", text) is not None


mismatches = []
intended_mismatches = []
for text in cases:
    expected = canonical(text)
    actual = candidate(text)
    if expected != actual:
        row = (text, expected, actual)
        mismatches.append(row)
        if strict_documented_shape(text):
            intended_mismatches.append(row)

print(f"documented examples: {len(examples)}")
print(f"directed cases: {len(directed)}")
print("exhaustive raw strings: lengths 0..7 over alphabet 'abc '")
print(f"generated strict-domain cases: {len(generated_intended)}")
print(f"unique cases: {len(cases)}")
print(f"strict documented-shape cases: {sum(map(strict_documented_shape, cases))}")
print(f"all canonical/candidate mismatches: {len(mismatches)}")
print(f"strict documented-shape mismatches: {len(intended_mismatches)}")
print("first ten mismatches (all are outside the strict documented shape):")
for text, expected, actual in mismatches[:10]:
    print(f"  {text!r}: canonical={expected!r}; candidate={actual!r}")

assert all(candidate(text) == canonical(text) for text in examples)
assert not intended_mismatches
assert candidate("ab") != canonical("ab")
