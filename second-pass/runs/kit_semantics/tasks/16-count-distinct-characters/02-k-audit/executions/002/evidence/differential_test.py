#!/usr/bin/env python3
"""Independent differential test for HumanEval/16."""

from __future__ import annotations

import importlib.util
import itertools
import random
import sys
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.count_distinct_characters


def independent_oracle(text: str) -> int:
    distinct: list[str] = []
    for character in text.lower():
        if character not in distinct:
            distinct.append(character)
    return len(distinct)


canonical = load_entry("trusted_canonical", Path("/reference/canonical.py"))
generated = load_entry(
    "generated_solution", Path("/tmp/audit-work/candidate-src/solution.py")
)

documented = ["xyzXYZ", "Jerry"]
boundaries = [
    "",
    "a",
    "A",
    "aa",
    "aA",
    "AaBb",
    "@A[",
    "`a{",
    "Z[z{",
    "0",
    "!!!",
    "Hello, World!",
    "\x00",
    "İ",
    "ß",
    "Straße",
    "Σσς",
    "𐐀𐐨",
    "éÉ",
    "e\u0301É",
]

alphabet = "aA0!zZ"
exhaustive = [
    "".join(chars)
    for length in range(5)
    for chars in itertools.product(alphabet, repeat=length)
]

rng = random.Random(160729)
random_alphabet = [
    "a",
    "A",
    "z",
    "Z",
    "0",
    "!",
    "İ",
    "ß",
    "Σ",
    "σ",
    "ς",
    "𐐀",
    "𐐨",
    "\x00",
    "\n",
]
generated_cases = [
    "".join(rng.choice(random_alphabet) for _ in range(rng.randrange(0, 65)))
    for _ in range(500)
]

cases = documented + boundaries + exhaustive + generated_cases
mismatches: list[tuple[str, int, int, int]] = []
for text in cases:
    expected = canonical(text)
    actual = generated(text)
    oracle = independent_oracle(text)
    if expected != actual or expected != oracle:
        mismatches.append((text, expected, actual, oracle))

print(f"documented={len(documented)}")
print(f"boundaries={len(boundaries)}")
print(f"exhaustive_small={len(exhaustive)}")
print(f"seeded_generated={len(generated_cases)}")
print(f"total={len(cases)} mismatches={len(mismatches)}")
for text in documented + ["", "aA", "İ", "Straße", "Σσς", "𐐀𐐨"]:
    print(
        f"witness={text!r} canonical={canonical(text)} "
        f"generated={generated(text)} oracle={independent_oracle(text)}"
    )

if mismatches:
    for mismatch in mismatches[:20]:
        print(f"MISMATCH {mismatch!r}")
    sys.exit(1)
