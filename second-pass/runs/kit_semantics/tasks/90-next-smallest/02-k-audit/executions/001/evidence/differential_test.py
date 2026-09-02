#!/usr/bin/env python3
"""Independent CPython differential for HumanEval 90.

The generated implementation and trusted canonical implementation are loaded
under separate module names.  The oracle below is an independent one-pass
implementation of the docstring's second-distinct-minimum contract.
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
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.next_smallest


def docstring_oracle(values: list[int]):
    first = None
    second = None
    for value in values:
        if first is None or value < first:
            if first is not None:
                second = first
            first = value
        elif value != first and (second is None or value < second):
            second = value
    return second


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--canonical", type=Path, required=True)
    args = parser.parse_args()

    candidate = load_entry(args.candidate, "audited_generated_solution")
    canonical = load_entry(args.canonical, "trusted_canonical_solution")

    documented = [
        ([1, 2, 3, 4, 5], 2),
        ([5, 1, 4, 3, 2], 2),
        ([], None),
        ([1, 1], None),
    ]
    branch_and_boundary = [
        [0],
        [0, 0, 0],
        [2, 1],                 # new minimum creates a second
        [1, 2],                 # first candidate second
        [1, 3, 2],              # update second
        [1, 2, 3],              # retain second
        [3, 1, 2],              # new minimum then update second
        [2, 1, 1, 2],           # duplicate minimum and second
        [-1, -2, -3],
        [-(10**200), 0, 10**200],
        [10**200, -(10**200)],
        [7] * 100,
        list(range(1000, -1001, -1)),
    ]

    mismatches: list[tuple[list[int], object, object, object]] = []
    checked = 0

    def check(values: list[int], expected=...):
        nonlocal checked
        before = list(values)
        oracle_value = docstring_oracle(values)
        if expected is not ... and oracle_value != expected:
            raise AssertionError((values, oracle_value, expected))
        candidate_value = candidate(values)
        canonical_value = canonical(values)
        checked += 1
        if values != before:
            raise AssertionError(f"input mutated: before={before!r}, after={values!r}")
        if candidate_value != oracle_value or canonical_value != oracle_value:
            mismatches.append(
                (before, oracle_value, candidate_value, canonical_value)
            )

    for values, expected in documented:
        check(list(values), expected)
    for values in branch_and_boundary:
        check(list(values))

    exhaustive = 0
    for length in range(0, 8):
        for values in itertools.product(range(-3, 4), repeat=length):
            check(list(values))
            exhaustive += 1

    rng = random.Random(0x90_20260731)
    random_cases = 20_000
    for _ in range(random_cases):
        length = rng.randrange(0, 101)
        values = [rng.randrange(-(10**80), 10**80) for _ in range(length)]
        if values and rng.randrange(2):
            # Force duplicates often enough to exercise distinctness.
            values[rng.randrange(length)] = values[rng.randrange(length)]
        check(values)

    print("documented_cases=4")
    print(f"branch_and_boundary_cases={len(branch_and_boundary)}")
    print("exhaustive_domain=lengths 0..7, values -3..3")
    print(f"exhaustive_cases={exhaustive}")
    print("random_seed=0x90_20260731")
    print("random_domain=20000 lists, lengths 0..100, integers in [-10^80,10^80)")
    print(f"random_cases={random_cases}")
    print(f"total_checked={checked}")
    print(f"mismatch_count={len(mismatches)}")
    if mismatches:
        for mismatch in mismatches[:20]:
            print("MISMATCH", repr(mismatch))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
