#!/usr/bin/env python3
"""Independent differential test for HumanEval/142.

Oracle: the trusted /reference/canonical.py entry point, imported directly.
Subject: the candidate solution.py copied into the scratch reconstruction.
The script also checks that neither implementation mutates its list argument.
"""

from __future__ import annotations

import argparse
import importlib.util
import itertools
import random
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sum_squares


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--subject",
        type=Path,
        default=Path("/tmp/audit-work/reconstruction/solution.py"),
    )
    args = parser.parse_args()
    canonical = load_entry(Path("/reference/canonical.py"), "trusted_canonical")
    subject = load_entry(args.subject, "candidate_subject")

    cases: list[tuple[int, ...]] = [
        (1, 2, 3),
        (),
        (-1, -5, 2, -1, -5),
        (7,),
        (0,),
        (-7,),
        tuple(range(1, 14)),
        tuple(range(-6, 8)),
        (10**30, -(10**25), 0, -1, 2, 3, -4, 5, 6, -7, 8, 9, -10),
        tuple([1] * 25),
        tuple([-1] * 25),
    ]
    # Exhaustive finite evidence through six positions. This crosses the
    # index classes 0, 3, and 4 and exercises every branch boundary.
    alphabet = (-2, -1, 0, 1, 2)
    for length in range(7):
        cases.extend(itertools.product(alphabet, repeat=length))

    # Deterministic broader samples cross later 3/4 boundaries (including 12).
    rng = random.Random(142)
    for _ in range(1200):
        length = rng.randrange(0, 41)
        values = []
        for _index in range(length):
            selector = rng.randrange(10)
            if selector == 0:
                values.append(rng.choice([10**18, -(10**18), 10**40, -(10**40)]))
            else:
                values.append(rng.randrange(-1000, 1001))
        cases.append(tuple(values))

    mismatches = []
    mutations = []
    for ordinal, values in enumerate(cases):
        oracle_input = list(values)
        subject_input = list(values)
        oracle_before = oracle_input.copy()
        subject_before = subject_input.copy()
        expected = canonical(oracle_input)
        actual = subject(subject_input)
        if expected != actual:
            mismatches.append((ordinal, values, expected, actual))
        if oracle_input != oracle_before or subject_input != subject_before:
            mutations.append(
                (ordinal, values, oracle_before, oracle_input, subject_before, subject_input)
            )

    examples = [
        ([1, 2, 3], 6),
        ([], 0),
        ([-1, -5, 2, -1, -5], -126),
    ]
    example_failures = []
    for values, expected in examples:
        actual = subject(values.copy())
        if actual != expected:
            example_failures.append((values, expected, actual))

    print(
        f"cases={len(cases)} mismatches={len(mismatches)} "
        f"mutations={len(mutations)} example_failures={len(example_failures)}"
    )
    print(
        "coverage=examples, empty, singleton, negative, zero, large integers, "
        "all branch index classes through index 39"
    )
    for item in mismatches[:10]:
        print(f"mismatch={item!r}")
    for item in mutations[:10]:
        print(f"mutation={item!r}")
    for item in example_failures:
        print(f"example_failure={item!r}")
    return 1 if mismatches or mutations or example_failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
