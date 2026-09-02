#!/usr/bin/env python3
"""Independent differential test of canonical.py and the submitted solution.py."""

from __future__ import annotations

import importlib.util
import itertools
import json
import pathlib
import random
import sys


def load_function(module_name: str, path: pathlib.Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.odd_count


def main() -> int:
    canonical = load_function(
        "trusted_canonical", pathlib.Path("/tmp/audit-work/trusted/canonical.py")
    )
    generated = load_function(
        "submitted_solution", pathlib.Path("/tmp/audit-work/source/solution.py")
    )

    cases: list[list[str]] = [
        ["1234567"],
        ["3", "11111111"],
        [],
        [""],
        ["0"],
        ["1"],
        ["9"],
        ["0123456789"],
        ["0246802468"],
        ["1357913579"],
        ["11111111111"],
        ["00000000000"],
        ["10", "", "2468", "13579"],
    ]
    cases.append([str(digit) for digit in range(10)])

    # Exhaust every digit string through length three. Each is a separate
    # single-element input list so every per-string odd-count branch is checked.
    digits = "0123456789"
    for length in range(4):
        for tup in itertools.product(digits, repeat=length):
            cases.append(["".join(tup)])

    # Deterministic broader and multi-element samples, including long strings
    # that force multi-digit count rendering.
    rng = random.Random(113)
    for _ in range(250):
        item_count = rng.randrange(0, 7)
        cases.append(
            [
                "".join(rng.choice(digits) for _ in range(rng.randrange(0, 65)))
                for _ in range(item_count)
            ]
        )

    records = []
    mismatches = []
    for index, case in enumerate(cases):
        expected = canonical(case)
        actual = generated(case)
        record = {
            "index": index,
            "input": case,
            "canonical": expected,
            "generated": actual,
            "match": expected == actual,
        }
        records.append(record)
        if not record["match"]:
            mismatches.append(record)

    print(
        json.dumps(
            {
                "scope": {
                    "documented_examples": 2,
                    "explicit_boundary_cases": 12,
                    "all_digit_strings_length_0_through_3": 1111,
                    "deterministic_generated_cases": 250,
                    "total_cases": len(cases),
                },
                "records": records,
                "mismatch_count": len(mismatches),
                "mismatches": mismatches,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
