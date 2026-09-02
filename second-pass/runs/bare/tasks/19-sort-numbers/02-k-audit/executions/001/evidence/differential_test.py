#!/usr/bin/env python3
"""Independent differential check for HumanEval 19.

Oracle: /reference/canonical.py, the trusted dataset implementation.
Candidate entry point: the clean scratch copy of candidate solution.py.

Input scope:
* the documented example and explicit empty input;
* every numeral absent/present once/present twice boundary;
* all 10^n canonical token sequences for n = 0..5 (111,111 inputs);
* 3,000 deterministic representative sequences of lengths 6, 10, and 25;
* leading, trailing, and repeated-space delimiter cases accepted by the
  canonical implementation.
"""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


WORDS = (
    "zero",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
)


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sort_numbers


canonical = load_entry("trusted_canonical", Path("/reference/canonical.py"))
candidate = load_entry(
    "scratch_candidate", Path("/tmp/audit-work/candidate-src/solution.py")
)

fixed_cases = [
    ("prompt-example", "three one five"),
    ("empty", ""),
    ("already-sorted", "zero one two three four five six seven eight nine"),
    ("reverse", "nine eight seven six five four three two one zero"),
    ("multiplicity", "two two one zero two"),
    ("leading-space", "  three one"),
    ("trailing-space", "three one  "),
    ("repeated-space", "nine   zero  five"),
]
fixed_cases.extend((f"singleton-{word}", word) for word in WORDS)
fixed_cases.extend((f"double-{word}", f"{word} {word}") for word in WORDS)

mismatches: list[tuple[str, str, str]] = []
checked = 0


def check(source: str) -> tuple[str, str]:
    global checked
    expected = canonical(source)
    actual = candidate(source)
    checked += 1
    if actual != expected and len(mismatches) < 20:
        mismatches.append((source, expected, actual))
    return expected, actual


print("FIXED_CASE_RESULTS")
for label, source in fixed_cases:
    expected, actual = check(source)
    print(
        f"{label}: input={source!r} canonical={expected!r} candidate={actual!r}"
    )

exhaustive_checked = 0
for length in range(6):
    for tokens in itertools.product(WORDS, repeat=length):
        check(" ".join(tokens))
        exhaustive_checked += 1

spacing_checked = 0
for first, second in itertools.product(WORDS, repeat=2):
    for source in (
        f" {first} {second}",
        f"{first} {second} ",
        f"{first}  {second}",
    ):
        check(source)
        spacing_checked += 1

rng = random.Random(19019)
generated_checked = 0
for length in (6, 10, 25):
    for _ in range(1000):
        check(" ".join(rng.choice(WORDS) for _ in range(length)))
        generated_checked += 1

print(
    "SUMMARY "
    f"fixed={len(fixed_cases)} "
    f"exhaustive_lengths_0_to_5={exhaustive_checked} "
    f"spacing_boundaries={spacing_checked} "
    f"generated_seed_19019={generated_checked} "
    f"total={checked} mismatches={len(mismatches)}"
)
if mismatches:
    for source, expected, actual in mismatches:
        print(
            f"MISMATCH input={source!r} canonical={expected!r} candidate={actual!r}"
        )
    raise SystemExit(1)
