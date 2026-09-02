#!/usr/bin/env python3
"""Concrete satisfying witnesses for every bounded SPEC entry claim."""

from __future__ import annotations

import importlib.util
import json
import pathlib
from collections.abc import Callable


def load_entry(path: pathlib.Path, module_name: str) -> Callable[[list[int]], bool]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_sorted


def sorted_from(values: list[int], previous: int, repeated: int) -> bool:
    """Direct executable transcription of verification.k's equations."""
    if not values:
        return True
    head, *tail = values
    if head < previous:
        return False
    if head == previous:
        if repeated + 1 > 1:
            return False
        return sorted_from(tail, head, repeated + 1)
    return sorted_from(tail, head, 0)


def main() -> int:
    canonical = load_entry(
        pathlib.Path("/reference/canonical.py"), "witness_canonical"
    )
    generated = load_entry(
        pathlib.Path("/tmp/audit-work/reconstruction/solution.py"),
        "witness_generated",
    )
    mismatches = 0
    for length in range(8):
        values = [0] * length
        precondition = len(values) == length and all(value >= 0 for value in values)
        claimed_result = sorted_from(values, -1, 0)
        canonical_result = canonical(values.copy())
        generated_result = generated(values.copy())
        agrees = (
            precondition
            and claimed_result == canonical_result == generated_result
        )
        mismatches += not agrees
        print(
            json.dumps(
                {
                    "claim": f"SPEC.len-{length}",
                    "input_binding": values,
                    "other_initial_cells": {
                        "env": 0,
                        "scopeLoc": 1,
                        "heap": ".Map",
                        "heapLoc": 0,
                        "stack": ".List",
                        "ret": "noRet",
                        "exc": "NoExc",
                        "exit-code": 0,
                    },
                    "precondition_satisfied": precondition,
                    "sortedAtMostTwice": claimed_result,
                    "trusted_canonical": canonical_result,
                    "generated_solution": generated_result,
                    "agrees": agrees,
                },
                sort_keys=True,
            )
        )
    print(f"mismatches={mismatches}")
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
