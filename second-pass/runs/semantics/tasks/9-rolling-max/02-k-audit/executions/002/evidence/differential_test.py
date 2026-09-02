#!/usr/bin/env python3
"""Independent differential test for HumanEval/9 rolling_max."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import random
from pathlib import Path


CANONICAL_PATH = Path("/reference/canonical.py")
GENERATED_PATH = Path("/tmp/audit-work/9-rolling-max/solution.py")


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.rolling_max


def main() -> int:
    canonical = load_function("trusted_canonical", CANONICAL_PATH)
    generated = load_function("candidate_generated", GENERATED_PATH)

    documented_and_boundary = [
        [],
        [1, 2, 3, 2, 3, 4, 2],
        [0],
        [-1],
        [1],
        [5, 4],       # first branch, then else/no-new-maximum
        [5, 5],       # equality boundary in max
        [4, 5],       # else/new-maximum
        [-8, -9, -3, -3, -10],
        [0, -1, 0, 1],
        [-(2**4096), 0, 2**4096, -(2**4097)],
        [10**100, -(10**101), 10**101],
        list(range(1000)),
        list(range(999, -1, -1)),
    ]

    exhaustive_small = [
        list(values)
        for length in range(7)
        for values in itertools.product((-2, -1, 0, 1, 2), repeat=length)
    ]

    rng = random.Random(0x9_2026_07_26)
    random_cases: list[list[int]] = []
    fixed_pool = [
        -(2**256),
        -(10**50),
        -2,
        -1,
        0,
        1,
        2,
        10**50,
        2**256,
    ]
    for _ in range(3000):
        length = rng.randrange(0, 101)
        case = [
            rng.choice(fixed_pool)
            if rng.randrange(4)
            else rng.randrange(-(10**100), 10**100 + 1)
            for _ in range(length)
        ]
        random_cases.append(case)

    cases = documented_and_boundary + exhaustive_small + random_cases
    encoded = json.dumps(cases, separators=(",", ":")).encode()
    mismatches = []
    summary_mismatches = []
    mutation_failures = []
    for index, original in enumerate(cases):
        canonical_input = list(original)
        generated_input = list(original)
        expected = canonical(canonical_input)
        actual = generated(generated_input)
        if expected != actual or type(expected) is not type(actual):
            mismatches.append((index, original, expected, actual))
        # Direct executable reading of verification.k's nextRolling/rollingAcc
        # recurrences, kept separate from both imported implementations.
        formal_summary = []
        first = True
        maximum = 0
        for value in original:
            maximum = value if first else max(maximum, value)
            first = False
            formal_summary.append(maximum)
        if expected != formal_summary:
            summary_mismatches.append((index, original, expected, formal_summary))
        if canonical_input != original or generated_input != original:
            mutation_failures.append((index, original, canonical_input, generated_input))

    print("oracle", CANONICAL_PATH)
    print("generated", GENERATED_PATH)
    print("documented_and_boundary_count", len(documented_and_boundary))
    print("exhaustive_small_domain", "lengths 0..6; values {-2,-1,0,1,2}")
    print("exhaustive_small_count", len(exhaustive_small))
    print("random_seed", hex(0x9_2026_07_26))
    print("random_domain", "3000 lists; lengths 0..100; unbounded-magnitude representatives")
    print("random_count", len(random_cases))
    print("total_case_count", len(cases))
    print("serialized_inputs_sha256", hashlib.sha256(encoded).hexdigest())
    print("mismatch_count", len(mismatches))
    print("formal_summary_mismatch_count", len(summary_mismatches))
    print("input_mutation_failure_count", len(mutation_failures))
    for index, case in enumerate(documented_and_boundary):
        print("boundary", index, "input", repr(case), "output", repr(generated(list(case))))
    if mismatches:
        print("first_mismatch", repr(mismatches[0]))
    if summary_mismatches:
        print("first_formal_summary_mismatch", repr(summary_mismatches[0]))
    if mutation_failures:
        print("first_input_mutation", repr(mutation_failures[0]))
    return 0 if not mismatches and not summary_mismatches and not mutation_failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
