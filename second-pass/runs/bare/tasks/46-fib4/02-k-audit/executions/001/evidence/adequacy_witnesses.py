#!/usr/bin/env python3
"""Ground witnesses for every spec claim precondition and claimed result."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


def load_fib4(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.fib4


def advance_to(a: int, b: int, c: int, d: int, i: int, n: int) -> int:
    while i <= n:
        a, b, c, d = b, c, d, a + b + c + d
        i += 1
    return d


def fib4_spec(n: int) -> int:
    if n == 0:
        return 0
    if n == 1:
        return 0
    if n == 2:
        return 2
    if n == 3:
        return 0
    if n >= 4:
        return advance_to(0, 0, 2, 0, 4, n)
    raise ValueError("outside formal domain")


def main() -> int:
    canonical = load_fib4("witness_canonical", Path("/reference/canonical.py"))
    generated = load_fib4(
        "witness_generated", Path("/tmp/audit-work/46-fib4/solution.py")
    )
    witnesses = [
        {
            "claim": "fib4-spec-link",
            "state": {"N": 7, "M": {}},
            "precondition": "N >= 4",
            "claimed_result": fib4_spec(7),
            "advanceTo": advance_to(0, 0, 2, 0, 4, 7),
            "canonical": canonical(7),
            "generated": generated(7),
        },
        {
            "claim": "loop-correct (loop-entry witness)",
            "state": {
                "N": 7,
                "I": 4,
                "A": 0,
                "B": 0,
                "C": 2,
                "D": 0,
                "E": 0,
            },
            "precondition": "N >= 4; I >= 4; I <= N",
            "claimed_result": advance_to(0, 0, 2, 0, 4, 7),
            "canonical": canonical(7),
            "generated": generated(7),
        },
        {
            "claim": "loop-correct (exit-boundary witness)",
            "state": {
                "N": 7,
                "I": 8,
                "A": 2,
                "B": 4,
                "C": 8,
                "D": 14,
                "E": 14,
            },
            "precondition": "N >= 4; I >= 4; I == N + 1",
            "claimed_result": advance_to(2, 4, 8, 14, 8, 7),
            "canonical": canonical(7),
            "generated": generated(7),
        },
        {
            "claim": "fib4-inductive-init",
            "state": {"N": 4, "arg": 4, "env": {}, "result": "noResult"},
            "precondition": "N >= 4",
            "destination_loop_result_by_composition": advance_to(0, 0, 2, 0, 4, 4),
            "canonical": canonical(4),
            "generated": generated(4),
        },
    ]
    for n in range(4):
        witnesses.append(
            {
                "claim": f"fib4-base-{n}",
                "state": {"arg": n, "env": {}, "result": "noResult"},
                "precondition": "true",
                "claimed_result": fib4_spec(n),
                "canonical": canonical(n),
                "generated": generated(n),
            }
        )
    witnesses.append(
        {
            "claim": "fib4-seven",
            "state": {"arg": 7, "env": {}, "result": "noResult"},
            "precondition": "true",
            "claimed_result": 14,
            "canonical": canonical(7),
            "generated": generated(7),
        }
    )

    mismatches = []
    for witness in witnesses:
        compared = [
            value
            for key, value in witness.items()
            if key
            in {
                "claimed_result",
                "advanceTo",
                "destination_loop_result_by_composition",
                "canonical",
                "generated",
            }
        ]
        if len(set(compared)) != 1:
            mismatches.append(witness["claim"])
    print(
        json.dumps(
            {"witnesses": witnesses, "mismatch_count": len(mismatches), "mismatches": mismatches},
            indent=2,
            sort_keys=True,
        )
    )
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
