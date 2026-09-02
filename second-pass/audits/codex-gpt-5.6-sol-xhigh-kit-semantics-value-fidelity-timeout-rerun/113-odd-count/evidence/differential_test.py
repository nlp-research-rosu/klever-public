#!/usr/bin/env python3
"""Independent differential test for HumanEval 113.

The case list is materialized to differential-inputs.json before execution.
The oracle is the trusted, unmodified HumanEval canonical implementation.
"""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import random
from pathlib import Path


EVIDENCE = Path("/audit-output/evidence")
CANONICAL_PATH = Path("/reference/canonical.py")
GENERATED_PATH = Path("/tmp/audit-work/source/solution.py")
INPUTS_PATH = EVIDENCE / "differential-inputs.json"


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.odd_count


def build_cases() -> list[list[str]]:
    # Documented examples and explicit branch/rendering boundaries.
    cases: list[list[str]] = [
        ["1234567"],
        ["3", "11111111"],
        [],
        [""],
        ["0"],
        ["1"],
        ["2"],
        ["9"],
        ["02468"],
        ["13579"],
        ["0123456789"],
        ["1" * 9],
        ["1" * 10],
        ["1" * 11],
        ["1" * 12],
        ["111", "", "2468", "97531"],
        ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
    ]

    # Exhaust every individual decimal string through length four.
    digits = "0123456789"
    for length in range(5):
        for chars in itertools.product(digits, repeat=length):
            cases.append(["".join(chars)])

    # Deterministic representative multi-element and longer inputs.
    rng = random.Random(113)
    for _ in range(500):
        list_length = rng.randrange(0, 9)
        case = [
            "".join(rng.choice(digits) for _ in range(rng.randrange(0, 31)))
            for _ in range(list_length)
        ]
        cases.append(case)
    return cases


def main() -> int:
    canonical = load_function("trusted_canonical_113", CANONICAL_PATH)
    generated = load_function("generated_solution_113", GENERATED_PATH)
    cases = build_cases()

    encoded = json.dumps(cases, ensure_ascii=True, separators=(",", ":"))
    INPUTS_PATH.write_text(encoded + "\n", encoding="utf-8")
    inputs_sha256 = hashlib.sha256((encoded + "\n").encode()).hexdigest()

    mismatches = []
    for index, case in enumerate(cases):
        expected = canonical(case)
        actual = generated(case)
        if actual != expected:
            mismatches.append(
                {
                    "index": index,
                    "input": case,
                    "canonical": expected,
                    "generated": actual,
                }
            )
            if len(mismatches) >= 20:
                break

    print(f"canonical={CANONICAL_PATH}")
    print(f"generated={GENERATED_PATH}")
    print("documented_examples=2")
    print("explicit_boundary_cases=15")
    print("exhaustive_single_strings=11111 (all digit strings length 0..4)")
    print("deterministic_generated_multilists=500 seed=113")
    print(f"total_cases={len(cases)}")
    print(f"inputs_file={INPUTS_PATH}")
    print(f"inputs_sha256={inputs_sha256}")
    print(f"mismatches={len(mismatches)}")
    if mismatches:
        print(json.dumps(mismatches, indent=2, ensure_ascii=True))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
