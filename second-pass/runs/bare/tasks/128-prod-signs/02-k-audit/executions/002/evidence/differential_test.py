#!/usr/bin/env python3
"""Differentially compare the trusted canonical function and candidate rewrite."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.prod_signs


def expected_formula(values: list[int]):
    if not values:
        return None
    sign = 1
    for value in values:
        sign *= -1 if value < 0 else 0 if value == 0 else 1
    return sum(abs(value) for value in values) * sign


def main() -> None:
    print("COMMAND: python3 /audit-output/evidence/differential_test.py")
    canonical = load_entry(
        Path("/tmp/audit-work/reference/canonical.py"), "trusted_canonical"
    )
    candidate = load_entry(
        Path("/tmp/audit-work/fresh/solution.py"), "candidate_solution"
    )

    named_cases = {
        "documented-negative": [1, 2, 2, -4],
        "documented-zero": [0, 1],
        "documented-empty": [],
        "negative-branch-single": [-1],
        "zero-branch-single": [0],
        "positive-branch-single": [1],
        "all-negative-even": [-1, -2],
        "all-negative-odd": [-1, -2, -3],
        "zero-after-negative": [-7, 0],
        "negative-after-zero": [0, -7],
        "large-magnitudes": [10**100, -(10**120), 1],
        "many-zeroes": [0, 0, 0],
    }
    checked = 0
    mismatches = []
    for name, values in named_cases.items():
        expected = expected_formula(values)
        trusted = canonical(list(values))
        observed = candidate(list(values))
        print(
            f"NAMED {name}: input={values!r} "
            f"canonical={trusted!r} candidate={observed!r} formula={expected!r}"
        )
        checked += 1
        if trusted != observed or observed != expected:
            mismatches.append((name, values, trusted, observed, expected))

    alphabet = (-3, -2, -1, 0, 1, 2, 3)
    exhaustive_checked = 0
    for length in range(0, 6):
        for values_tuple in itertools.product(alphabet, repeat=length):
            values = list(values_tuple)
            trusted = canonical(values)
            observed = candidate(values)
            expected = expected_formula(values)
            checked += 1
            exhaustive_checked += 1
            if trusted != observed or observed != expected:
                mismatches.append(
                    ("exhaustive", values, trusted, observed, expected)
                )

    generator = random.Random(128_20260726)
    random_checked = 0
    for _ in range(2_000):
        length = generator.randrange(0, 41)
        values = [generator.randrange(-(10**9), 10**9 + 1) for _ in range(length)]
        trusted = canonical(values)
        observed = candidate(values)
        expected = expected_formula(values)
        checked += 1
        random_checked += 1
        if trusted != observed or observed != expected:
            mismatches.append(("random", values, trusted, observed, expected))

    print(f"exhaustive_domain=values[-3..3], lengths[0..5]")
    print(f"exhaustive_checked={exhaustive_checked}")
    print(f"random_seed=12820260726 random_checked={random_checked} lengths[0..40]")
    print(f"total_checked={checked} mismatches={len(mismatches)}")
    if mismatches:
        for mismatch in mismatches[:10]:
            print(f"MISMATCH {mismatch!r}")
        raise SystemExit(1)
    print("STATUS: PASS")


if __name__ == "__main__":
    main()
