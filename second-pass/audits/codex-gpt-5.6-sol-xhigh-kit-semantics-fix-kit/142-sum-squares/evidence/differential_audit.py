#!/usr/bin/env python3
"""Independent differential audit for HumanEval 142 sum_squares."""

from __future__ import annotations

import importlib.util
import itertools
import random
import sys
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sum_squares


def add_case(cases: list[tuple[str, list[int]]], category: str, values) -> None:
    cases.append((category, list(values)))


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: differential_audit.py TRUSTED_CANONICAL GENERATED_SOLUTION", file=sys.stderr)
        return 64

    canonical = load_entry(Path(sys.argv[1]), "trusted_canonical_142")
    generated = load_entry(Path(sys.argv[2]), "generated_solution_142")
    cases: list[tuple[str, list[int]]] = []

    examples = [
        ([1, 2, 3], 6),
        ([], 0),
        ([-1, -5, 2, -1, -5], -126),
    ]
    for values, expected in examples:
        actual = canonical(list(values))
        if actual != expected:
            print(f"TRUSTED_EXAMPLE_DISAGREEMENT input={values!r} expected={expected} canonical={actual}")
            return 2
        add_case(cases, "documented-example", values)

    # Lengths around each residue in one complete lcm(3,4)=12 index period,
    # plus the next index-12 boundary where square takes precedence over cube.
    for length in range(0, 15):
        add_case(cases, "branch-boundary-length", [i - 7 for i in range(length)])
        add_case(cases, "branch-boundary-constant", [2] * length)

    # Value boundaries and very large mathematical integers.
    add_case(cases, "integer-boundary", [0] * 15)
    add_case(cases, "integer-boundary", [-1, 0, 1] * 5)
    add_case(cases, "integer-boundary", [10**100, -(10**100), 2, -2, 3] * 3)

    # Exhaustive finite sample and a deterministic broader generated sample.
    for length in range(0, 7):
        for values in itertools.product(range(-3, 4), repeat=length):
            add_case(cases, "exhaustive-len0-6-values-3-3", values)
    rng = random.Random(142)
    for _ in range(2000):
        length = rng.randrange(0, 101)
        add_case(
            cases,
            "deterministic-random",
            [rng.randint(-(10**18), 10**18) for _ in range(length)],
        )

    counts: dict[str, int] = {}
    mismatches = 0
    mutations = 0
    for category, values in cases:
        counts[category] = counts.get(category, 0) + 1
        left_input = list(values)
        right_input = list(values)
        left = canonical(left_input)
        right = generated(right_input)
        if left_input != values or right_input != values:
            mutations += 1
            print(f"INPUT_MUTATION category={category} input={values!r}")
        if left != right:
            mismatches += 1
            print(
                f"MISMATCH category={category} input={values!r} "
                f"canonical={left!r} generated={right!r}"
            )
        if mismatches + mutations >= 20:
            break

    print(f"CASE_COUNTS={counts}")
    print(f"TOTAL_CASES={len(cases)}")
    print(f"MISMATCHES={mismatches}")
    print(f"INPUT_MUTATIONS={mutations}")
    if mismatches or mutations:
        return 1
    print("DIFFERENTIAL_AUDIT_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
