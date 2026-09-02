#!/usr/bin/env python3
"""Independent differential test for trusted canonical.py vs submitted solution.py."""

from __future__ import annotations

import argparse
import importlib.util
import json
import random
from pathlib import Path
from typing import Any, Callable


def load_entry(path: Path, module_name: str) -> Callable[[int, int], Any]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.modp


def outcome(function: Callable[[int, int], Any], n: int, p: int) -> dict[str, Any]:
    try:
        value = function(n, p)
        return {"kind": "return", "type": type(value).__name__, "value": value}
    except Exception as error:  # Deliberately compare public exception behavior.
        return {
            "kind": "exception",
            "type": type(error).__name__,
            "message": str(error),
        }


def add_unique(cases: list[tuple[int, int]], seen: set[tuple[int, int]], case: tuple[int, int]) -> None:
    if case not in seen:
        seen.add(case)
        cases.append(case)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--canonical", type=Path, required=True)
    parser.add_argument("--solution", type=Path, required=True)
    parser.add_argument("--inputs-out", type=Path, required=True)
    arguments = parser.parse_args()

    canonical = load_entry(arguments.canonical, "audit_trusted_canonical")
    solution = load_entry(arguments.solution, "audit_submitted_solution")

    intended: list[tuple[int, int]] = []
    seen: set[tuple[int, int]] = set()

    documented_examples = [(3, 5), (1101, 101), (0, 101), (3, 11), (100, 101)]
    boundaries = [
        (0, 1),
        (0, 2),
        (1, 1),
        (1, 2),
        (2, 1),
        (2, 2),
        (31, 7),
        (32, 7),
        (63, 97),
        (64, 97),
        (10000, 65537),
    ]
    for case in documented_examples + boundaries:
        add_unique(intended, seen, case)

    # Exhaust the small formal domain around both loop and modulus boundaries.
    for n in range(0, 33):
        for p in range(1, 34):
            add_unique(intended, seen, (n, p))

    generator = random.Random(490049)
    generated = [
        (generator.randrange(0, 2049), generator.randrange(1, 1001))
        for _ in range(256)
    ]
    for case in generated:
        add_unique(intended, seen, case)

    # Diagnostic probes outside N >= 0 and P > 0; not counted as theorem-domain failures.
    outside = [
        (-5, 7),
        (-2, 5),
        (-1, 1),
        (-1, 5),
        (0, -7),
        (1, -7),
        (5, -7),
        (0, 0),
        (1, 0),
    ]

    arguments.inputs_out.write_text(
        json.dumps(
            {
                "formal_domain": "n >= 0 and p > 0",
                "documented_examples": documented_examples,
                "boundary_cases": boundaries,
                "exhaustive_grid": {"n": [0, 32], "p": [1, 33]},
                "random_seed": 490049,
                "generated_cases": generated,
                "deduplicated_intended_cases": intended,
                "outside_domain_diagnostics": outside,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    mismatches: list[dict[str, Any]] = []
    for n, p in intended:
        canonical_outcome = outcome(canonical, n, p)
        solution_outcome = outcome(solution, n, p)
        if canonical_outcome != solution_outcome:
            mismatches.append(
                {
                    "input": [n, p],
                    "canonical": canonical_outcome,
                    "solution": solution_outcome,
                }
            )

    print(f"documented_examples={len(documented_examples)}")
    print(f"boundary_cases={len(boundaries)}")
    print("exhaustive_grid=n:0..32,p:1..33")
    print(f"generated_seed=490049 generated_count={len(generated)}")
    print(f"intended_unique_count={len(intended)}")
    print(f"intended_mismatch_count={len(mismatches)}")
    for mismatch in mismatches[:20]:
        print("INTENDED_MISMATCH " + json.dumps(mismatch, sort_keys=True))

    print("outside_domain_diagnostics:")
    for n, p in outside:
        record = {
            "input": [n, p],
            "canonical": outcome(canonical, n, p),
            "solution": outcome(solution, n, p),
        }
        print(json.dumps(record, sort_keys=True))

    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
