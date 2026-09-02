#!/usr/bin/env python3
"""Concrete substitutions into the K entry claim's sortedScan result."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_sorted


def sorted_scan(values: list[int], previous: int = -1, duplicates: int = 0) -> bool:
    """Direct executable transcription of verification.k's equations."""
    if not values:
        return True
    value, *rest = values
    if value < previous:
        return False
    if value == previous and duplicates >= 1:
        return False
    if value > previous:
        return sorted_scan(rest, value, 0)
    if value == previous and duplicates == 0:
        return sorted_scan(rest, value, 1)
    if value == previous and duplicates < 0:
        return False
    raise AssertionError("integer trichotomy/duplicate partition was not exhaustive")


def main() -> int:
    canonical = load(Path("/reference/canonical.py"), "adequacy_canonical")
    generated = load(
        Path("/tmp/audit-work/candidate-src/solution.py"),
        "adequacy_generated",
    )
    cases = [
        [],
        [0],
        [0, 0],
        [0, 0, 0],
        [1, 2, 2],
        [1, 2, 2, 2],
        [1, 0],
        [0, 1],
    ]
    mismatches = 0
    for case in cases:
        precondition = all(type(value) is int and value >= 0 for value in case)
        k_result = sorted_scan(case)
        canonical_result = canonical(case.copy())
        generated_result = generated(case.copy())
        agree = (
            precondition
            and type(k_result) is bool
            and k_result == canonical_result == generated_result
        )
        print(
            f"input={case!r} precondition={precondition} "
            f"sortedScan={k_result} canonical={canonical_result} "
            f"generated={generated_result} agree={agree}"
        )
        mismatches += int(not agree)
    print(f"checked={len(cases)} mismatches={mismatches}")
    return int(mismatches != 0)


if __name__ == "__main__":
    raise SystemExit(main())
