#!/usr/bin/env python3
"""Independent candidate-vs-trusted-canonical differential test."""

from __future__ import annotations

import importlib.util
import itertools
import random
import string
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.select_words


canonical = load_entry(Path("/reference/canonical.py"), "trusted_canonical")
candidate = load_entry(Path("/candidate/solution.py"), "generated_solution")


NAMED_CASES = [
    ("prompt-1", "Mary had a little lamb", 4),
    ("prompt-2", "Mary had a little lamb", 3),
    ("prompt-3", "simple white space", 2),
    ("prompt-4", "Hello world", 4),
    ("prompt-5", "Uncle sam", 3),
    ("empty-n0", "", 0),
    ("empty-positive-n", "", 1),
    ("spaces-only", "     ", 0),
    ("leading-trailing-runs", "  a   bc  ", 0),
    ("zero-consonant-vowels", "a AEIOU ee", 0),
    ("single-consonant", "b a z", 1),
    ("all-consonants-exact", "bcdf xyz", 4),
    ("all-consonants-other", "bcdf xyz", 3),
    ("case-boundary", "AEiOU BcD", 3),
    ("n-over-word-length", "a bb ccc", 4),
    ("mixed-branch", "a b ab ba bcd", 1),
]


def check(label: str, source: str, n: int) -> None:
    global checked
    expected = canonical(source, n)
    actual = candidate(source, n)
    checked += 1
    if expected != actual:
        mismatches.append((label, source, n, expected, actual))


checked = 0
mismatches: list[tuple[object, ...]] = []

print("NAMED CASES")
for label, source, n in NAMED_CASES:
    check(label, source, n)
    print(
        repr(label),
        repr(source),
        n,
        "canonical=",
        repr(canonical(source, n)),
        "candidate=",
        repr(candidate(source, n)),
    )

# Exhaustive small domain: every string of length 0..7 over one lower-case
# vowel, one upper-case consonant, and ASCII space; n covers 0 through 8.
exhaustive_strings = 0
for length in range(8):
    for chars in itertools.product("aB ", repeat=length):
        source = "".join(chars)
        exhaustive_strings += 1
        for n in range(9):
            check("exhaustive", source, n)

# A deterministic broader sample over the documented alphabet.
seed = 117_20260726
rng = random.Random(seed)
alphabet = string.ascii_letters + " "
random_cases = 5000
for index in range(random_cases):
    source = "".join(rng.choice(alphabet) for _ in range(rng.randrange(0, 81)))
    n = rng.randrange(0, 25)
    check(f"random-{index}", source, n)

print("SUMMARY")
print("exhaustive-alphabet", repr("aB "))
print("exhaustive-lengths", "0..7")
print("exhaustive-n", "0..8")
print("exhaustive-strings", exhaustive_strings)
print("random-seed", seed)
print("random-alphabet", "ASCII letters plus U+0020")
print("random-lengths", "0..80")
print("random-n", "0..24")
print("random-cases", random_cases)
print("total-comparisons", checked)
print("mismatches", len(mismatches))
for mismatch in mismatches[:20]:
    print("MISMATCH", repr(mismatch))

raise SystemExit(1 if mismatches else 0)
