#!/usr/bin/env python3
"""Ground witnesses for the submitted loop and end-to-end preconditions."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


WORK = Path("/tmp/audit-work/24-largest-divisor")


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.largest_divisor


def no_divisor_from(n: int, low: int, high: int) -> bool:
    return all(n % candidate != 0 for candidate in range(low, high + 1))


def is_largest_proper_divisor(n: int, divisor: int) -> bool:
    return (
        0 < divisor < n
        and n % divisor == 0
        and no_divisor_from(n, divisor + 1, n - 1)
    )


def main() -> int:
    canonical = load(WORK / "trusted-canonical.py", "witness_canonical")
    candidate = load(WORK / "solution.py", "witness_candidate")
    n = 15
    d = 14
    expected = 5
    entry_precondition = n > 1
    loop_precondition = (
        n > 1
        and d > 0
        and d < n
        and no_divisor_from(n, d + 1, n - 1)
    )
    result = {
        "entry_witness": {
            "arg": n,
            "initial_env": {},
            "initial_result": "noResult",
            "precondition_N_gt_1": entry_precondition,
        },
        "loop_witness": {
            "arg": n,
            "initial_env": {"n": n, "divisor": d},
            "initial_result": "noResult",
            "precondition": loop_precondition,
            "no_divisor_interval": [d + 1, n - 1],
        },
        "substituted_result": expected,
        "candidate_python_result": candidate(n),
        "canonical_python_result": canonical(n),
        "postcondition": is_largest_proper_divisor(n, expected),
        "false_mutation_result_equals_two": expected == 2,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if (
        entry_precondition
        and loop_precondition
        and candidate(n) == expected
        and canonical(n) == expected
        and is_largest_proper_divisor(n, expected)
        and expected != 2
    ) else 1


if __name__ == "__main__":
    raise SystemExit(main())
