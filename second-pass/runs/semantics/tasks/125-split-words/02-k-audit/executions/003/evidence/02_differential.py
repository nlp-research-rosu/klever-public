#!/usr/bin/env python3
"""Independent candidate-versus-canonical differential test.

The oracle and generated function are loaded from distinct copied source files.
The generated cases include exhaustive short strings around both branch
boundaries plus a deterministic broader sample.
"""

from __future__ import annotations

import importlib.util
import itertools
import random
import sys
from pathlib import Path


WORK = Path("/tmp/audit-work/125-split-words")


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.split_words


canonical = load_function("trusted_canonical", WORK / "canonical.py")
generated = load_function("generated_solution", WORK / "solution.py")

fixed_cases = [
    # Documented examples.
    "Hello world!",
    "Hello,world!",
    "abcdef",
    # Empty and delimiter boundaries.
    "",
    " ",
    "  ",
    ",",
    ",,",
    "a,b",
    "a,,b",
    ",a",
    "a,",
    "a,,,b",
    # Whitespace/comma precedence and every candidate whitespace boundary.
    "a b",
    "a , b",
    "a,\tb",
    "a\tb",
    "a\nb",
    "a\rb",
    "a\vb",
    "a\fb",
    # Count branch boundaries.
    "a",
    "b",
    "z",
    "Bdfz!",
    "abcdefghijklmnopqrstuvwxyz",
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "0123!?",
    # Unrestricted Python-str boundary: canonical islower/ord is Unicode-aware.
    "à",  # U+00E0, lowercase and even code point.
    "β",  # U+03B2, lowercase and even code point.
    "é",  # U+00E9, lowercase but odd code point.
    "a b\u00a0c",  # split() sees the non-breaking-space after branch selection.
]

alphabet = ("a", "b", "c", " ", ",", "\t", "\n", "\r", "\v", "\f")
exhaustive_cases = [
    "".join(chars)
    for length in range(5)
    for chars in itertools.product(alphabet, repeat=length)
]

rng = random.Random(125)
random_alphabet = (
    "abcdefghijklmnopqrstuvwxyz"
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "0123456789!?-_"
    " ,\t\n\r\v\f"
)
random_cases = [
    "".join(rng.choice(random_alphabet) for _ in range(rng.randrange(0, 41)))
    for _ in range(4000)
]

seen: set[str] = set()
cases: list[str] = []
for text in fixed_cases + exhaustive_cases + random_cases:
    if text not in seen:
        seen.add(text)
        cases.append(text)

mismatches: list[tuple[str, object, object]] = []
print("FIXED CASES")
for text in fixed_cases:
    expected = canonical(text)
    actual = generated(text)
    print(
        f"{text!r}: canonical={expected!r}; generated={actual!r}; "
        f"equal={expected == actual}"
    )

for text in cases:
    expected = canonical(text)
    actual = generated(text)
    if expected != actual:
        mismatches.append((text, expected, actual))

print(f"total_unique_cases={len(cases)}")
print(f"exhaustive_alphabet={alphabet!r}")
print("exhaustive_lengths=0..4")
print("deterministic_random_seed=125")
print(f"mismatch_count={len(mismatches)}")
print("FIRST 40 MISMATCHES")
for text, expected, actual in mismatches[:40]:
    print(f"{text!r}: canonical={expected!r}; generated={actual!r}")

sys.exit(1 if mismatches else 0)
