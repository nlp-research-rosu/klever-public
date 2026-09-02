#!/usr/bin/env python3
"""Independent candidate-versus-trusted-canonical differential test."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import random
import sys
from pathlib import Path
from typing import Any, Callable


TRUSTED_CANONICAL = Path("/reference/canonical.py")
GENERATED_SOLUTION = Path("/tmp/audit-work/audit73/solution.py")
INPUT_RECORD = Path("/audit-output/evidence/differential-inputs.json")
SEED = 730073


def load_entry(module_name: str, path: Path) -> Callable[[list[int]], int]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.smallest_change


def make_corpus() -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = [
        {"id": "example-1", "kind": "documented", "arr": [1, 2, 3, 5, 4, 7, 9, 6]},
        {"id": "example-2", "kind": "documented", "arr": [1, 2, 3, 4, 3, 2, 2]},
        {"id": "example-3", "kind": "documented", "arr": [1, 2, 3, 2, 1]},
        {"id": "empty-left-gt-right", "kind": "branch-boundary", "arr": []},
        {"id": "singleton-left-eq-right", "kind": "branch-boundary", "arr": [7]},
        {"id": "pair-equal", "kind": "branch-boundary", "arr": [4, 4]},
        {"id": "pair-unequal", "kind": "branch-boundary", "arr": [4, 5]},
        {"id": "odd-outer-equal-inner-unequal", "kind": "branch-boundary", "arr": [1, 2, 0, 3, 1]},
        {"id": "odd-outer-unequal-inner-equal", "kind": "branch-boundary", "arr": [1, 2, 0, 2, 3]},
        {"id": "negative-and-large", "kind": "integer-boundary", "arr": [-(2**63), 0, 2**63 - 1]},
        {"id": "long-palindrome-recursion-boundary", "kind": "runtime-boundary", "arr": [0] * 2200},
        {
            "id": "long-all-mismatch-recursion-boundary",
            "kind": "runtime-boundary",
            "arr": list(range(1100)) + list(range(2200, 1100, -1)),
        },
    ]

    for length in range(9):
        for index, values in enumerate(itertools.product((-1, 0, 1), repeat=length)):
            cases.append(
                {
                    "id": f"exhaustive-small-n{length}-{index}",
                    "kind": "exhaustive-small",
                    "arr": list(values),
                }
            )

    rng = random.Random(SEED)
    values = [-(2**63), -100, -2, -1, 0, 1, 2, 100, 2**63 - 1]
    for index in range(2000):
        length = rng.randrange(0, 81)
        cases.append(
            {
                "id": f"random-{index}",
                "kind": "seeded-random",
                "arr": [rng.choice(values) for _ in range(length)],
            }
        )
    return cases


def outcome(fn: Callable[[list[int]], int], arr: list[int]) -> dict[str, Any]:
    try:
        return {"status": "return", "value": fn(list(arr))}
    except Exception as error:  # an exception is an observable differential outcome
        return {
            "status": "exception",
            "type": type(error).__name__,
            "message": str(error),
        }


def main() -> int:
    canonical = load_entry("trusted_canonical_73", TRUSTED_CANONICAL)
    generated = load_entry("generated_solution_73", GENERATED_SOLUTION)
    cases = make_corpus()
    INPUT_RECORD.write_text(
        json.dumps(
            {
                "trusted_oracle": str(TRUSTED_CANONICAL),
                "generated_program": str(GENERATED_SOLUTION),
                "seed": SEED,
                "generator_scope": {
                    "documented_and_boundary_cases": 12,
                    "exhaustive_small": "all arrays of lengths 0..8 over {-1,0,1}",
                    "seeded_random": "2000 arrays of lengths 0..80 over nine boundary/representative integers",
                },
                "cases": cases,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )

    mismatches: list[dict[str, Any]] = []
    counts: dict[str, int] = {}
    for case in cases:
        counts[case["kind"]] = counts.get(case["kind"], 0) + 1
        expected = outcome(canonical, case["arr"])
        actual = outcome(generated, case["arr"])
        if expected != actual:
            encoded = json.dumps(case["arr"], separators=(",", ":")).encode()
            mismatches.append(
                {
                    "id": case["id"],
                    "kind": case["kind"],
                    "length": len(case["arr"]),
                    "input_sha256": hashlib.sha256(encoded).hexdigest(),
                    "canonical": expected,
                    "generated": actual,
                }
            )

    print(f"PYTHON_VERSION: {sys.version.split()[0]}")
    print(f"RECURSION_LIMIT: {sys.getrecursionlimit()}")
    print(f"SEED: {SEED}")
    print(f"CASE_COUNTS: {json.dumps(counts, sort_keys=True)}")
    print(f"TOTAL_CASES: {len(cases)}")
    print(f"MISMATCH_COUNT: {len(mismatches)}")
    for mismatch in mismatches:
        print(f"MISMATCH: {json.dumps(mismatch, sort_keys=True)}")
    print(f"INPUT_RECORD: {INPUT_RECORD}")
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
