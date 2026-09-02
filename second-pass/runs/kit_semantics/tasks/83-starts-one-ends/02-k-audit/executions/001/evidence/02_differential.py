#!/usr/bin/env python3
"""Independent differential and small-domain contract checks for HumanEval 83."""

from __future__ import annotations

import importlib.util
import random
import sys
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.starts_one_ends


def enumerated_contract_count(n: int) -> int:
    lower = 10 ** (n - 1)
    upper = 10**n
    return sum(
        str(value).startswith("1") or str(value).endswith("1")
        for value in range(lower, upper)
    )


def describe(value: int) -> str:
    decimal_digits = 1 if value == 0 else len(str(value))
    return f"digits={decimal_digits}, bit_length={value.bit_length()}"


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: 02_differential.py TRUSTED_CANONICAL CANDIDATE_SOLUTION")
        return 2

    canonical = load_entry("trusted_canonical_83", Path(sys.argv[1]))
    generated = load_entry("candidate_solution_83", Path(sys.argv[2]))

    # The prompt supplies no examples. The positive-integer domain has no
    # meaningful "empty" value; n=1 is its minimum and the conditional boundary.
    fixed_cases = [1, 2, 3, 4, 6, 10, 50, 100, 500, 1000]
    rng = random.Random(830083)
    generated_cases = [rng.randint(1, 1000) for _ in range(250)]
    cases = sorted(set(fixed_cases + generated_cases))

    mismatches: list[tuple[int, int, int]] = []
    for n in cases:
        expected = canonical(n)
        actual = generated(n)
        if actual != expected:
            mismatches.append((n, expected, actual))

    property_mismatches: list[tuple[int, int, int]] = []
    for n in range(1, 6):
        expected = enumerated_contract_count(n)
        actual = generated(n)
        if actual != expected:
            property_mismatches.append((n, expected, actual))
        print(
            f"enumerated-contract n={n}: expected={expected} "
            f"candidate={actual} equal={expected == actual}"
        )

    print("prompt_examples = none")
    print("empty_case = not_applicable_to_positive_integer_scalar_domain")
    print("branch_boundaries = [1, 2]")
    print(f"differential_case_count = {len(cases)}")
    print(f"differential_min_max = ({min(cases)}, {max(cases)})")
    print(f"differential_mismatches = {len(mismatches)}")
    print(f"enumerated_property_mismatches = {len(property_mismatches)}")
    print(f"n=1 result = {generated(1)}")
    print(f"n=2 result = {generated(2)}")
    print(f"n=1000 result summary = {describe(generated(1000))}")
    if mismatches:
        print("first differential mismatches:", mismatches[:10])
    if property_mismatches:
        print("property mismatches:", property_mismatches)
    return 1 if mismatches or property_mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
