#!/usr/bin/env python3
"""Evaluate concrete satisfying witnesses in both Python implementations."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def claimed_summary(values: list[int]) -> list[int]:
    # Concrete interpretation of sortVS(filterOdd(VS)) under the named sortVS
    # contract and the filterOdd equations in verification.k.
    return sorted(value for value in values if all(digit not in str(value) for digit in "02468"))


def main() -> int:
    canonical = load(Path(sys.argv[1]), "witness_canonical")
    candidate = load(Path(sys.argv[2]), "witness_candidate")
    witnesses = [[], [1], [15, 33, 1422, 1], [33, 1, 33, 20, 15, 3, 15]]
    failures = 0
    for values in witnesses:
        positive_ints = all(isinstance(value, int) and not isinstance(value, bool) and value > 0 for value in values)
        claimed = claimed_summary(values)
        canonical_result = canonical.unique_digits(list(values))
        candidate_result = candidate.unique_digits(list(values))
        record = {
            "input": values,
            "positiveInts_witness": positive_ints,
            "claimed_sortVS_filterOdd": claimed,
            "canonical": canonical_result,
            "candidate": candidate_result,
        }
        print(json.dumps(record, sort_keys=True))
        if not positive_ints or not (claimed == canonical_result == candidate_result):
            failures += 1
    print(f"WITNESSES: {len(witnesses)}")
    print(f"FAILURES: {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
