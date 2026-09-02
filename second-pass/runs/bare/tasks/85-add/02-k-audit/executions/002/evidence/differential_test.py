#!/usr/bin/env python3
"""Independent differential test of trusted canonical.py and candidate solution.py."""

from __future__ import annotations

import importlib.util
from itertools import product
from pathlib import Path
import random
import sys


ROOT = Path("/tmp/audit-work/85-add-review")


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def outcome(function, values):
    try:
        return ("value", function(list(values)))
    except Exception as err:  # Report exceptional divergence as an outcome.
        return ("exception", type(err).__name__, str(err))


def main() -> int:
    canonical = load("trusted_canonical", ROOT / "canonical.py").add
    candidate = load("generated_candidate", ROOT / "solution.py").add

    fixed = [
        [],
        [0],
        [1],
        [-2],
        [4, 2, 6, 7],  # documented example
        [1, 2],         # first contributing branch
        [1, 3],         # first rejected branch
        [1, 0],
        [1, -2],
        [1, -3],
        [2, 3, 4],
        [2, 4, 3],
        [-1, -2, -3, -4, -5],
        [10**100, -(10**100), 7, 2],
    ]

    cases = list(fixed)
    alphabet = (-3, -2, -1, 0, 1, 2, 3)
    for length in range(0, 6):
        cases.extend(product(alphabet, repeat=length))

    rng = random.Random(850085)
    for _ in range(5000):
        length = rng.randrange(0, 41)
        cases.append([rng.randrange(-10**9, 10**9 + 1) for _ in range(length)])

    mismatches = []
    for number, values in enumerate(cases):
        expected = outcome(canonical, values)
        actual = outcome(candidate, values)
        if actual != expected:
            mismatches.append((number, list(values), expected, actual))

    print("ORACLE=/reference/canonical.py copied byte-for-byte to scratch")
    print("CANDIDATE=/candidate/solution.py copied byte-for-byte to scratch")
    print("FIXED_CASES=" + repr(fixed))
    print(
        "EXHAUSTIVE_SCOPE=all lists of lengths 0..5 over "
        + repr(alphabet)
    )
    print("RANDOM_SCOPE=5000 lists; seed=850085; lengths=0..40; values=-1e9..1e9")
    print(f"TOTAL_CASES={len(cases)}")
    print(f"MISMATCHES={len(mismatches)}")
    for mismatch in mismatches[:20]:
        print("MISMATCH=" + repr(mismatch))

    # Record the implementation-resource boundary separately. It is not folded
    # into the ordinary finite differential set.
    long_values = [0] * 2501
    canonical_long = outcome(canonical, long_values)
    candidate_long = outcome(candidate, long_values)
    print("RESOURCE_BOUNDARY_INPUT=len([0]*2501)")
    print("RESOURCE_BOUNDARY_CANONICAL=" + repr(canonical_long))
    print("RESOURCE_BOUNDARY_CANDIDATE=" + repr(candidate_long))
    print(
        "RESOURCE_BOUNDARY_MATCH="
        + repr(canonical_long == candidate_long)
    )

    return 1 if mismatches else 0


if __name__ == "__main__":
    sys.exit(main())
