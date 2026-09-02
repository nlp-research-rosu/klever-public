#!/usr/bin/env python3
"""Concrete satisfying witnesses for every reachability claim."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


TRUSTED = Path("/tmp/audit-work/26-remove-duplicates/trusted/canonical.py")
GENERATED = Path("/tmp/audit-work/26-remove-duplicates/candidate/solution.py")


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.remove_duplicates


def count(values: list[int], value: int) -> int:
    return sum(item == value for item in values)


def keep_singles_acc(
    accumulator: list[int], remaining: list[int], all_values: list[int]
) -> list[int]:
    result = list(accumulator)
    for value in remaining:
        if count(all_values, value) == 1:
            result.append(value)
    return result


def main() -> int:
    canonical = load_function("trusted_canonical_witness", TRUSTED)
    candidate = load_function("candidate_solution_witness", GENERATED)
    witnesses = [
        {
            "claim": "loop-invariant",
            "all": [1, 2, 2, 3],
            "remaining": [2, 2, 3],
            "accumulator": [1],
            "precondition": True,
            "k_post_list": [1, 3],
        },
        {
            "claim": "entry-empty",
            "input": [],
            "precondition": True,
            "k_post_list": [],
        },
        {
            "claim": "entry-keep",
            "input": [1, 2, 2, 3],
            "precondition": count([1, 2, 2, 3], 1) == 1,
            "k_post_list": [1, 3],
        },
        {
            "claim": "entry-drop",
            "input": [1, 1, 2],
            "precondition": count([1, 1, 2], 1) != 1,
            "k_post_list": [2],
        },
    ]

    failures: list[str] = []
    for witness in witnesses:
        if witness["claim"] == "loop-invariant":
            actual_summary = keep_singles_acc(
                witness["accumulator"], witness["remaining"], witness["all"]
            )
            if actual_summary != witness["k_post_list"]:
                failures.append(f"{witness['claim']}: summary mismatch")
            full_input = witness["all"]
        else:
            full_input = witness["input"]
            if candidate(list(full_input)) != witness["k_post_list"]:
                failures.append(f"{witness['claim']}: candidate mismatch")
            if canonical(list(full_input)) != witness["k_post_list"]:
                failures.append(f"{witness['claim']}: canonical mismatch")
        if not witness["precondition"]:
            failures.append(f"{witness['claim']}: unsatisfied precondition")
        witness["canonical_result"] = canonical(list(full_input))
        witness["candidate_result"] = candidate(list(full_input))

    print(json.dumps(witnesses, indent=2, sort_keys=True))
    print(f"failure_count={len(failures)}")
    if failures:
        print(json.dumps(failures, indent=2))
        return 1
    print("RESULT=PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
