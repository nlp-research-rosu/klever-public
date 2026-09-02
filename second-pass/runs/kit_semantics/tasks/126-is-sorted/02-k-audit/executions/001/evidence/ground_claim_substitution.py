#!/usr/bin/env python3
"""Ground instances of the entry claim's result predicate."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_sorted


def k_claim_predicate(values: list[int]) -> bool:
    # Direct ground interpretation of sortedWithAtMostTwo's defining equation:
    # VS ==K sortVS(VS) andBool scanDuplicates(-1, 0, true, VS).
    previous = -1
    repeated = 0
    duplicate_ok = True
    for value in values:
        next_repeated = repeated + 1 if value == previous else 1
        duplicate_ok = duplicate_ok and not (next_repeated > 2)
        previous = value
        repeated = next_repeated
    return values == sorted(values) and duplicate_ok


def main() -> int:
    canonical = load_function(
        Path("/reference/canonical.py"), "canonical_ground"
    )
    candidate = load_function(
        Path("/tmp/audit-work/126-is-sorted/solution.py"),
        "candidate_ground",
    )
    witnesses = [
        [],
        [0],
        [0, 1, 1],
        [0, 0, 0],
        [2, 1],
        [0, 1, 1, 2, 2],
    ]
    failures = 0
    for values in witnesses:
        precondition = all(type(value) is int and value >= 0 for value in values)
        claim_result = k_claim_predicate(values)
        canonical_result = canonical(list(values))
        candidate_result = candidate(list(values))
        equal = (
            precondition
            and claim_result == canonical_result == candidate_result
        )
        print(
            f"input={values!r} precondition={precondition} "
            f"claim={claim_result} canonical={canonical_result} "
            f"candidate={candidate_result} all_equal={equal}"
        )
        failures += not equal
    print(f"FAILURE_COUNT={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
