#!/usr/bin/env python3
"""Independent differential check of trusted canonical.py and candidate solution.py."""

from __future__ import annotations

import argparse
import importlib.util
import json
import random
from pathlib import Path
from typing import Any, Callable


def load_entry(path: Path, module_name: str) -> Callable[[list[str], list[int]], int]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.do_algebra


def outcome(fn: Callable[[list[str], list[int]], int], ops: list[str], nums: list[int]) -> dict[str, Any]:
    try:
        value = fn(list(ops), list(nums))
        return {"kind": "return", "type": type(value).__name__, "value": value}
    except Exception as err:  # Comparing documented exceptional boundary behavior is intentional.
        return {"kind": "raise", "type": type(err).__name__, "message": str(err)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--canonical", type=Path, required=True)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--results", type=Path, required=True)
    args = parser.parse_args()

    canonical = load_entry(args.canonical, "audit_canonical")
    candidate = load_entry(args.candidate, "audit_candidate")

    # Named cases cover the prompt example, all five operator branches, both scan
    # directions, precedence boundaries, associativity, zero values, and division
    # by zero (which is permitted by the stated non-negative operand domain).
    cases: list[dict[str, Any]] = [
        {"name": "prompt-example", "ops": ["+", "*", "-"], "nums": [2, 3, 4, 5]},
        {"name": "minimum-plus", "ops": ["+"], "nums": [0, 0]},
        {"name": "minimum-minus", "ops": ["-"], "nums": [0, 7]},
        {"name": "minimum-times", "ops": ["*"], "nums": [0, 9]},
        {"name": "minimum-floor", "ops": ["//"], "nums": [7, 3]},
        {"name": "minimum-power", "ops": ["**"], "nums": [2, 5]},
        {"name": "zero-power-zero", "ops": ["**"], "nums": [0, 0]},
        {"name": "division-by-zero", "ops": ["//"], "nums": [3, 0]},
        {"name": "minus-left-assoc", "ops": ["-", "-"], "nums": [20, 5, 3]},
        {"name": "floor-left-assoc", "ops": ["//", "//"], "nums": [20, 3, 2]},
        {"name": "power-right-assoc", "ops": ["**", "**"], "nums": [2, 3, 2]},
        {"name": "plus-vs-minus-rightmost-split", "ops": ["-", "+"], "nums": [9, 4, 2]},
        {"name": "times-vs-floor-rightmost-split", "ops": ["//", "*"], "nums": [20, 2, 3]},
        {"name": "power-leftmost-split", "ops": ["**", "+", "**"], "nums": [2, 3, 2, 2]},
        {"name": "all-precedence-levels", "ops": ["+", "*", "**", "//", "-"], "nums": [4, 3, 2, 3, 5, 1]},
        {"name": "floor-zero-after-precedence", "ops": ["//", "-"], "nums": [4, 1, 1]},
        {"name": "negative-intermediate", "ops": ["-", "*"], "nums": [1, 3, 2]},
        {"name": "power-precedes-times", "ops": ["*", "**"], "nums": [2, 3, 2]},
    ]

    # Deterministic generated cases use the complete operator alphabet, lengths
    # 1..5, and operands 0..8. At most one exponentiation per generated case
    # bounds arithmetic size; adjacent-power associativity is covered above.
    rng = random.Random(160)
    alphabet = ["+", "-", "*", "//", "**"]
    for index in range(400):
        count = rng.randint(1, 5)
        ops = [rng.choice(alphabet) for _ in range(count)]
        if ops.count("**") > 1:
            first = ops.index("**")
            ops = [op if op != "**" or pos == first else rng.choice(["+", "-", "*", "//"])
                   for pos, op in enumerate(ops)]
        nums = [rng.randint(0, 8) for _ in range(count + 1)]
        cases.append({"name": f"generated-{index:03d}", "ops": ops, "nums": nums})

    records = []
    mismatches = 0
    for case in cases:
        expected = outcome(canonical, case["ops"], case["nums"])
        actual = outcome(candidate, case["ops"], case["nums"])
        match = expected == actual
        mismatches += int(not match)
        records.append({**case, "canonical": expected, "candidate": actual, "match": match})

    payload = {
        "oracle": str(args.canonical),
        "candidate": str(args.candidate),
        "seed": 160,
        "operator_alphabet": alphabet,
        "case_count": len(records),
        "mismatch_count": mismatches,
        "cases": records,
    }
    args.results.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({key: payload[key] for key in ("seed", "case_count", "mismatch_count")}, sort_keys=True))
    if mismatches:
        for record in records:
            if not record["match"]:
                print(json.dumps(record, sort_keys=True))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
