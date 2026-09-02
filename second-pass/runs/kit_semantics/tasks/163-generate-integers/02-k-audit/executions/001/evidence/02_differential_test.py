#!/usr/bin/env python3
"""Independent candidate/canonical/contract differential test."""

from __future__ import annotations

import importlib.util
import random
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.generate_integers


canonical = load_entry("trusted_canonical", Path("/reference/canonical.py"))
generated = load_entry(
    "scratch_generated",
    Path("/tmp/audit-work/reconstruction/solution.py"),
)


def contract_oracle(a: int, b: int) -> list[int]:
    low, high = min(a, b), max(a, b)
    return [digit for digit in (2, 4, 6, 8) if low <= digit <= high]


def check(a: int, b: int, label: str) -> None:
    expected = canonical(a, b)
    actual = generated(a, b)
    direct = contract_oracle(a, b)
    if expected != direct or actual != expected:
        raise AssertionError(
            {
                "label": label,
                "input": (a, b),
                "generated": actual,
                "canonical": expected,
                "contract_oracle": direct,
            }
        )


def main() -> None:
    print("COMMAND: python3 /audit-output/evidence/02_differential_test.py")
    documented = [
        (2, 8, [2, 4, 6, 8]),
        (8, 2, [2, 4, 6, 8]),
        (10, 14, []),
    ]
    checked = 0
    for a, b, documented_result in documented:
        if canonical(a, b) != documented_result:
            raise AssertionError(("trusted canonical/documented example", a, b))
        check(a, b, "documented")
        checked += 1

    # Every threshold has values immediately below, at, and above it in both
    # endpoint positions.  The set also covers the positive-domain lower edge,
    # the cutoff after digit 8, empty spans, equal endpoints, and reversed spans.
    boundaries = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 14)
    for a in boundaries:
        for b in boundaries:
            check(a, b, "branch-boundary-grid")
            checked += 1

    # Exhaustive dense positive grid beyond all branch cutoffs.
    for a in range(1, 129):
        for b in range(1, 129):
            check(a, b, "dense-grid-1..128")
            checked += 1

    # Deterministic broad positive sample and unbounded-integer witnesses.
    rng = random.Random(163_20260729)
    for _ in range(5000):
        a = rng.randrange(1, 10**12)
        b = rng.randrange(1, 10**12)
        check(a, b, "seeded-broad-sample")
        checked += 1
    huge = 10**100
    for a, b in (
        (1, huge),
        (huge, 1),
        (huge, huge + 1),
        (2, huge),
        (huge, 8),
        (7, huge),
    ):
        check(a, b, "unbounded-integer-witness")
        checked += 1

    print(
        "PASS: "
        f"{checked} positive-input pairs; generated == trusted canonical "
        "== independent direct-contract oracle; 0 mismatches"
    )


if __name__ == "__main__":
    main()
