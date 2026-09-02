#!/usr/bin/env python3
"""Independent Python differential tests for HumanEval/35."""

from __future__ import annotations

import importlib.util
import json
import random
from pathlib import Path
import sys


REFERENCE = Path("/reference/canonical.py")
CANDIDATE = Path("/tmp/audit-work/35-max-element/solution.py")


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.max_element


def outcome(fn, value):
    try:
        result = fn(value.copy())
        return {"kind": "return", "type": type(result).__name__, "value": result}
    except Exception as err:
        return {"kind": "raise", "type": type(err).__name__, "message": str(err)}


def main() -> int:
    canonical = load_function("trusted_humaneval_35", REFERENCE)
    candidate = load_function("generated_humaneval_35", CANDIDATE)

    documented = [
        [1, 2, 3],
        [5, 3, -5, 2, -3, 3, 9, 0, 123, 1, -10],
    ]
    branch_boundaries = [
        [0],
        [-1],
        [1, 2],
        [2, 1],
        [1, 1],
        [-2, -1],
        [-1, -2],
        [0, 0, 0],
        [-(10**100), 0, 10**100],
        [10**100, 0, -(10**100)],
        [3, 1, 3, 2],
        [-5, -5, -4, -4],
    ]
    comparable_non_integer = [
        [1.5, -2.0, 1.5001],
        [-0.0, 0.0],
        ["alpha", "zeta", "mu"],
        [False, True, False],
        [1, 2.5, -3],
    ]

    rng = random.Random(350035)
    generated: list[list[int]] = []
    for _ in range(500):
        length = rng.randint(1, 40)
        generated.append([rng.randint(-(10**12), 10**12) for _ in range(length)])

    mismatches = []
    checked = 0
    for group, cases in (
        ("documented", documented),
        ("branch_boundaries", branch_boundaries),
        ("generated_integer", generated),
        ("comparable_non_integer", comparable_non_integer),
    ):
        for index, case in enumerate(cases):
            left = outcome(canonical, case)
            right = outcome(candidate, case)
            checked += 1
            if left != right:
                mismatches.append(
                    {
                        "group": group,
                        "index": index,
                        "input": case,
                        "canonical": left,
                        "candidate": right,
                    }
                )

    empty_canonical = outcome(canonical, [])
    empty_candidate = outcome(candidate, [])
    print(
        json.dumps(
            {
                "oracle": str(REFERENCE),
                "candidate": str(CANDIDATE),
                "checked_nonempty": checked,
                "group_counts": {
                    "documented": len(documented),
                    "branch_boundaries": len(branch_boundaries),
                    "generated_integer": len(generated),
                    "comparable_non_integer": len(comparable_non_integer),
                },
                "mismatch_count_nonempty": len(mismatches),
                "mismatches": mismatches,
                "empty_boundary": {
                    "canonical": empty_canonical,
                    "candidate": empty_candidate,
                    "contract_note": "No maximum exists; exception type is outside the return-value contract.",
                },
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 1 if mismatches else 0


if __name__ == "__main__":
    sys.exit(main())
