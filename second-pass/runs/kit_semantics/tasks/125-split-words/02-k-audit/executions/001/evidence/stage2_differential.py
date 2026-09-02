#!/usr/bin/env python3
"""Independent docstring-first differential for HumanEval 125."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path
from typing import Any, Callable


SCRATCH = Path("/tmp/audit-work/125-split-words")


def load_function(module_name: str, path: Path) -> Callable[[str], Any]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.split_words


candidate = load_function("audit_candidate", SCRATCH / "solution.py")
canonical = load_function("audit_canonical", SCRATCH / "canonical.py")


def docstring_oracle(txt: str) -> list[str] | int:
    """A direct, independent reading of the docstring's three-way contract."""
    if any(char.isspace() for char in txt):
        return txt.split()
    if "," in txt:
        return txt.split(",")
    odd_zero_based_ascii = set("bdfhjlnprtvxz")
    return sum(char in odd_zero_based_ascii for char in txt)


documented: list[tuple[str, list[str] | int]] = [
    ("Hello world!", ["Hello", "world!"]),
    ("Hello,world!", ["Hello", "world!"]),
    ("abcdef", 3),
]

boundaries = [
    "",
    "a",
    "b",
    "z",
    "A",
    "B",
    "!",
    ",",
    ",a",
    "a,",
    ",,",
    "a,,b",
    " ",
    "  ",
    " a",
    "a ",
    "a  b",
    "a,b c",
    "a,b\tc",
    "\t",
    "\n",
    "\r",
    "\v",
    "\f",
    "\u001c",
    "\u001d",
    "\u001e",
    "\u001f",
    "\u0085",
    "\u00a0",
    "\u1680",
    "\u2000",
    "\u2007",
    "\u2028",
    "\u2029",
    "\u202f",
    "\u205f",
    "\u3000",
    "\u200b",
    "é",
    "β",
    "a\u00a0b",
    "a\u200bb",
    "bdz",
    "bdfhjlnprtvxz",
    "acegikmoqsuwy",
]

alphabet = ["a", "b", "z", "A", ",", " ", "\t", "\v", "\u00a0", "\u200b", "é", "!"]
exhaustive = [
    "".join(chars)
    for length in range(5)
    for chars in itertools.product(alphabet, repeat=length)
]

rng = random.Random(125_20260730)
random_alphabet = (
    alphabet
    + ["c", "d", "f", "x", "\n", "\r", "\f", "\u2028", "β", "中", "0", "_"]
)
generated = [
    "".join(rng.choice(random_alphabet) for _ in range(rng.randrange(0, 31)))
    for _ in range(5000)
]

cases = list(dict.fromkeys([text for text, _ in documented] + boundaries + exhaustive + generated))

documented_failures = []
candidate_oracle_mismatches = []
candidate_canonical_mismatches = []
branch_counts = {"whitespace": 0, "comma": 0, "count": 0}

for text in cases:
    expected = docstring_oracle(text)
    actual = candidate(text)
    witness = canonical(text)
    if any(char.isspace() for char in text):
        branch_counts["whitespace"] += 1
    elif "," in text:
        branch_counts["comma"] += 1
    else:
        branch_counts["count"] += 1
    if actual != expected:
        candidate_oracle_mismatches.append((text, actual, expected))
    if actual != witness:
        candidate_canonical_mismatches.append((text, actual, witness))

for text, expected in documented:
    actual = candidate(text)
    if actual != expected:
        documented_failures.append((text, actual, expected))

print("oracle=docstring whitespace precedence, then literal-comma split, then ASCII b,d,...,z count")
print("exhaustive_alphabet=", repr(alphabet))
print("exhaustive_lengths=0..4")
print("random_seed=12520260730 random_count=5000 random_lengths=0..30")
print("total_unique_cases=", len(cases))
print("branch_counts=", branch_counts)
print("documented_failures=", len(documented_failures))
print("candidate_oracle_mismatches=", len(candidate_oracle_mismatches))
print("candidate_canonical_mismatches=", len(candidate_canonical_mismatches))
print("candidate_canonical_first_20=")
for mismatch in candidate_canonical_mismatches[:20]:
    print(repr(mismatch))

if documented_failures or candidate_oracle_mismatches:
    print("candidate_oracle_first_20=")
    for mismatch in candidate_oracle_mismatches[:20]:
        print(repr(mismatch))
    raise SystemExit(1)
