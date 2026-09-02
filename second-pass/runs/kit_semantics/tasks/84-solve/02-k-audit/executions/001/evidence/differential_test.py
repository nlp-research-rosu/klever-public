#!/usr/bin/env python3
"""Independent differential test for trusted canonical.py vs solution.py."""

from __future__ import annotations

import importlib.util
import random
from pathlib import Path


ROOT = Path("/tmp/audit-work/84-solve")


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.solve


def main() -> None:
    trusted_solve = load_function(ROOT / "canonical.py", "trusted_canonical")
    generated_solve = load_function(ROOT / "solution.py", "generated_solution")

    documented = [1000, 150, 147]
    domain_boundaries = [0, 1, 9, 10, 99, 100, 999, 1000, 9999, 10000]
    sum_boundaries = [0, 7, 8, 15, 16, 23, 24, 31, 32, 36]
    witnesses: dict[int, int] = {}
    mismatches: list[tuple[int, object, object]] = []

    for n in range(0, 10001):
        expected = trusted_solve(n)
        actual = generated_solve(n)
        if expected != actual:
            mismatches.append((n, expected, actual))
        digit_sum = sum(int(char) for char in str(n))
        if digit_sum in sum_boundaries and digit_sum not in witnesses:
            witnesses[digit_sum] = n

    if mismatches:
        raise AssertionError(f"first mismatches: {mismatches[:10]}")
    if set(witnesses) != set(sum_boundaries):
        raise AssertionError(f"missing branch-boundary witnesses: {witnesses}")

    rng = random.Random(840084)
    generated = sorted({rng.randrange(0, 10001) for _ in range(256)})
    for n in documented + domain_boundaries + generated + list(witnesses.values()):
        if trusted_solve(n) != generated_solve(n):
            raise AssertionError(f"selected input mismatch: {n}")

    print("contract_domain=all integers 0..10000 inclusive")
    print("empty_case=not_applicable_to_integer_input; lower boundary N=0 tested")
    print(f"documented_examples={documented}")
    print(f"domain_boundaries={domain_boundaries}")
    print(f"branch_sum_boundary_witnesses={dict(sorted(witnesses.items()))}")
    print(f"seeded_representative_inputs={len(generated)} seed=840084")
    print("exhaustive_differential_cases=10001 mismatches=0")


if __name__ == "__main__":
    main()
