#!/usr/bin/env python3
"""Independent canonical-vs-candidate differential test for HumanEval/43."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import random
import sys
from pathlib import Path
from typing import Callable


ROOT = Path("/tmp/audit-work/43-pairs-sum-to-zero")


def load(path: Path, module_name: str) -> Callable[[list[int]], bool]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.pairs_sum_to_zero


def outcome(function: Callable[[list[int]], bool], values: list[int]) -> dict[str, object]:
    try:
        result = function(values.copy())
        return {"kind": "return", "type": type(result).__name__, "value": result}
    except BaseException as error:
        return {
            "kind": "exception",
            "type": type(error).__name__,
            "message": str(error),
        }


def main() -> int:
    canonical = load(ROOT / "trusted/canonical.py", "trusted_canonical_43")
    candidate = load(ROOT / "candidate/solution.py", "candidate_solution_43")

    documented = [
        [1, 3, 5, 0],
        [1, 3, -2, 1],
        [1, 2, 3, 7],
        [2, 4, -5, 3, 5, 7],
        [1],
    ]
    targeted = [
        [],
        [0],
        [0, 0],
        [1, -1],
        [-1, 1],
        [5, 5],
        [2, 4, -2],
        [2, 4, -4],
        [2, 4, 6, -2],
        [-(10**100), 10**100],
        [10**100, 1, -(10**100)],
        [-(10**100), -(10**99), 1],
    ]
    exhaustive = [
        list(values)
        for length in range(0, 6)
        for values in itertools.product(range(-3, 4), repeat=length)
    ]
    rng = random.Random(20260726)
    generated = [
        [rng.randrange(-10**12, 10**12 + 1) for _ in range(rng.randrange(0, 81))]
        for _ in range(2000)
    ]
    generated.extend(
        [
            [rng.randrange(1, 10**12 + 1) for _ in range(997)],
            [rng.randrange(1, 10**12 + 1) for _ in range(1200)],
            [1] * 1200,
            [1, -1] + [1] * 1198,
        ]
    )

    groups = {
        "documented": documented,
        "targeted": targeted,
        "exhaustive_lengths_0_to_5_values_-3_to_3": exhaustive,
        "seeded_generated": generated,
    }
    serialized = json.dumps(groups, separators=(",", ":"), sort_keys=True)
    print("python_version:", sys.version.replace("\n", " "))
    print("recursion_limit:", sys.getrecursionlimit())
    print("corpus_sha256:", hashlib.sha256(serialized.encode()).hexdigest())

    mismatches: list[dict[str, object]] = []
    total = 0
    group_counts: dict[str, int] = {}
    for group, inputs in groups.items():
        group_counts[group] = len(inputs)
        for values in inputs:
            total += 1
            expected = outcome(canonical, values)
            actual = outcome(candidate, values)
            if expected != actual:
                mismatches.append(
                    {
                        "group": group,
                        "length": len(values),
                        "input_prefix": values[:12],
                        "input_suffix": values[-4:],
                        "canonical": expected,
                        "candidate": actual,
                    }
                )

    print("group_counts:", json.dumps(group_counts, sort_keys=True))
    print("total_cases:", total)
    print("mismatch_count:", len(mismatches))
    for mismatch in mismatches[:20]:
        print("MISMATCH:", json.dumps(mismatch, sort_keys=True))
    if len(mismatches) > 20:
        print("additional_mismatches_omitted:", len(mismatches) - 20)

    status = 1 if mismatches else 0
    print("DIFFERENTIAL_EXIT_STATUS:", status)
    return status


if __name__ == "__main__":
    raise SystemExit(main())
