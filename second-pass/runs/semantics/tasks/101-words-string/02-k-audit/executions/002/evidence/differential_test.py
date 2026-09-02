#!/usr/bin/env python3
"""Independent differential test for HumanEval 101.

Oracle: the trusted /reference/canonical.py implementation.
Subject: the clean scratch copy of the candidate's generated solution.py.
"""

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
    return module.words_string


canonical = load_entry(Path("/reference/canonical.py"), "trusted_canonical")
generated = load_entry(
    Path("/tmp/audit-work/101-words-string-independent-audit/solution.py"),
    "generated_solution",
)

documented_and_boundaries = [
    "Hi, my name is John",
    "One, two, three, four, five, six",
    "",
    "a",
    ",",
    " ",
    ", ",
    " ,",
    ",,",
    "  ",
    "a,b",
    "a b",
    "a, b",
    " a ",
    ",a,",
    "a,,b",
    "a  b",
    "a,\tb\nc",
    "\t\n\r\v\f",
    "alpha\u00a0beta",
    "\u2003alpha,\u2028beta\u3000",
    "naïve,東京 café",
    "\x00,\x00",
]

alphabet = ("a", "B", ",", " ", "\t", "\n", "\u00a0")
exhaustive = (
    "".join(chars)
    for length in range(6)
    for chars in itertools.product(alphabet, repeat=length)
)

rng = random.Random(101)
random_alphabet = (
    string.ascii_letters
    + string.digits
    + ", \t\n\r\v\f"
    + "\u00a0\u1680\u2003\u2028\u2029\u3000"
    + "é東京_-."
)
random_cases = [
    "".join(rng.choice(random_alphabet) for _ in range(rng.randrange(0, 101)))
    for _ in range(2_000)
]

checked = 0
for source in itertools.chain(documented_and_boundaries, exhaustive, random_cases):
    expected = canonical(source)
    actual = generated(source)
    if actual != expected:
        raise AssertionError(
            f"mismatch for {source!r}: canonical={expected!r}, generated={actual!r}"
        )
    checked += 1

print(f"documented_and_boundary_cases={len(documented_and_boundaries)}")
print("exhaustive_alphabet='a','B',comma,space,tab,newline,NBSP")
print("exhaustive_lengths=0..5")
print(f"random_seed=101 random_cases={len(random_cases)} random_max_length=100")
print(f"total_cases={checked}")
print("mismatches=0")
