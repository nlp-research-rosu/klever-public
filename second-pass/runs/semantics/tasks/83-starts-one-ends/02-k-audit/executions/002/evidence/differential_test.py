#!/usr/bin/env python3
"""Independent differential and small-domain contract test for HumanEval 83."""

from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path
from types import ModuleType


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def brute_count(n: int) -> int:
    lower = 1 if n == 1 else 10 ** (n - 1)
    upper = 10**n
    return sum(
        1
        for value in range(lower, upper)
        if str(value).startswith("1") or str(value).endswith("1")
    )


def claimed_result(n: int) -> int:
    """Concrete substitution into the two K claim right-hand sides."""
    if n == 1:
        return 1
    return 18 * (10 ** (n - 2))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--canonical", type=Path, required=True)
    parser.add_argument("--solution", type=Path, required=True)
    args = parser.parse_args()

    canonical = load_module("trusted_canonical", args.canonical)
    solution = load_module("submitted_solution", args.solution)

    # No examples are stated in prompt.py. 1 and 2 are the branch boundary;
    # 3..50 are exhaustive representative positive sizes; larger values check
    # Python's arbitrary-precision path.
    cases = list(range(1, 51)) + [64, 100, 257]
    mismatches: list[tuple[int, int, int]] = []
    for n in cases:
        expected = canonical.starts_one_ends(n)
        actual = solution.starts_one_ends(n)
        if expected != actual:
            mismatches.append((n, expected, actual))

    brute_mismatches: list[tuple[int, int, int, int]] = []
    for n in range(1, 6):
        counted = brute_count(n)
        expected = canonical.starts_one_ends(n)
        actual = solution.starts_one_ends(n)
        if counted != expected or counted != actual:
            brute_mismatches.append((n, counted, expected, actual))

    witness_inputs = [1, 2, 3, 5, 10]
    witness_rows = [
        (
            n,
            claimed_result(n),
            canonical.starts_one_ends(n),
            solution.starts_one_ends(n),
        )
        for n in witness_inputs
    ]
    witness_mismatches = [
        row for row in witness_rows if not (row[1] == row[2] == row[3])
    ]

    print(f"documented_examples=[]")
    print(f"intended_domain=positive integers")
    print(f"branch_boundary_cases=[1, 2]")
    print(f"differential_cases={cases}")
    print(f"differential_mismatches={mismatches}")
    print(f"brute_force_cases={list(range(1, 6))}")
    print(f"brute_force_mismatches={brute_mismatches}")
    print("witness_columns=(n, claimed_K_rhs, canonical, submitted)")
    print(f"satisfying_claim_witnesses={witness_rows}")
    print(f"claim_witness_mismatches={witness_mismatches}")
    print("empty_case=not_applicable_to_positive_integer_input")
    return 1 if mismatches or brute_mismatches or witness_mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
