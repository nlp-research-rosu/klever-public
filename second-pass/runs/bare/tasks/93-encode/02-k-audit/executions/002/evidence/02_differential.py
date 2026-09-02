#!/usr/bin/env python3
"""Differentially compare the trusted canonical and candidate entry points."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import random
import string
from pathlib import Path


def load_function(module_name: str, path: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.encode


canonical = load_function("trusted_canonical", "/reference/canonical.py")
candidate = load_function("generated_solution", "/candidate/solution.py")

documented_and_boundaries = [
    "",
    "test",
    "This is a message",
    "a",
    "A",
    "e",
    "E",
    "i",
    "I",
    "o",
    "O",
    "u",
    "U",
    "b",
    "B",
    "z",
    "Z",
    " ",
    "aeiou",
    "AEIOU",
    "bcdfg",
    "BCDFG",
    "aA eE iI oO uU",
    string.ascii_lowercase,
    string.ascii_uppercase,
    string.ascii_letters + " ",
    " " * 8,
    "a" * 128,
    "Z" * 128,
]

# The prompt refers to the English alphabet. These are reported separately as
# out-of-scope diagnostics rather than counted in the intended-domain verdict.
unicode_diagnostics = ["é", "É", "ß", "Ωω", "Жж", "İı"]

alphabet = "aAeEuUbBzZ "
exhaustive = [
    "".join(chars)
    for length in range(5)
    for chars in itertools.product(alphabet, repeat=length)
]

rng = random.Random(930026)
random_cases = [
    "".join(rng.choice(string.ascii_letters + " ") for _ in range(rng.randrange(0, 257)))
    for _ in range(2000)
]

cases = documented_and_boundaries + exhaustive + random_cases
mismatches = []
digest = hashlib.sha256()
for index, message in enumerate(cases):
    expected = canonical(message)
    actual = candidate(message)
    digest.update(
        json.dumps([message, expected, actual], ensure_ascii=False, separators=(",", ":")).encode()
    )
    if expected != actual:
        mismatches.append(
            {"index": index, "input": message, "canonical": expected, "candidate": actual}
        )

print("oracle", "/reference/canonical.py:encode")
print("candidate", "/candidate/solution.py:encode")
print("documented_and_boundary_cases", len(documented_and_boundaries))
print("exhaustive_alphabet", repr(alphabet))
print("exhaustive_lengths", "0..4")
print("exhaustive_cases", len(exhaustive))
print("random_seed", 930026)
print("random_alphabet", "ascii_letters plus space")
print("random_cases", len(random_cases))
print("total_cases", len(cases))
print("comparison_digest", digest.hexdigest())
print("mismatch_count", len(mismatches))
for mismatch in mismatches[:20]:
    print(json.dumps(mismatch, ensure_ascii=False, sort_keys=True))
unicode_mismatches = []
for message in unicode_diagnostics:
    expected, actual = canonical(message), candidate(message)
    if expected != actual:
        unicode_mismatches.append([message, expected, actual])
print("unicode_diagnostics_outside_english_alphabet", len(unicode_diagnostics))
print("unicode_diagnostic_mismatches", json.dumps(unicode_mismatches, ensure_ascii=False))
raise SystemExit(1 if mismatches else 0)
