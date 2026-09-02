#!/usr/bin/env python3
"""Independent candidate-vs-canonical differential test for HumanEval 104."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import random
import sys
from pathlib import Path


CANONICAL_PATH = Path("/tmp/audit-work/104-unique-digits/reference/canonical.py")
CANDIDATE_PATH = Path("/tmp/audit-work/104-unique-digits/candidate/solution.py")
SEED = 0x104


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.unique_digits


def outcome(function, values: list[int]):
    try:
        return {"kind": "return", "value": function(values.copy())}
    except BaseException as error:  # Deliberately compare observable exceptions.
        return {
            "kind": "exception",
            "type": type(error).__name__,
            "message": str(error),
        }


def digest(values: list[int]) -> str:
    encoded = ",".join(str(value) for value in values).encode()
    return hashlib.sha256(encoded).hexdigest()


def compact_outcome(result):
    if result["kind"] == "exception":
        return result
    values = result["value"]
    return {
        "kind": "return",
        "length": len(values),
        "sha256": digest(values),
        "preview": values[:8],
    }


def main() -> int:
    canonical = load_entry(CANONICAL_PATH, "trusted_canonical_104")
    candidate = load_entry(CANDIDATE_PATH, "audited_candidate_104")

    curated = [
        ("example_1", [15, 33, 1422, 1]),
        ("example_2", [152, 323, 1422, 10]),
        ("empty", []),
        ("base_one", [1]),
        ("single_even", [2]),
        ("single_odd", [9]),
        ("decimal_boundary_10", [9, 10, 11]),
        ("even_middle_digit", [101, 111]),
        ("even_leading_digit", [211, 311]),
        ("recursive_accept", [13579]),
        ("recursive_reject", [13578]),
        ("duplicates", [97531, 7, 111, 97531]),
        ("reverse_order", [999, 777, 555, 333, 111]),
        ("mixed_order", [531, 3, 24681, 97531, 15, 2]),
        ("power_boundaries", [99, 100, 101, 999, 1000, 1001]),
    ]

    generated: list[tuple[str, list[int]]] = []
    generated.extend((f"singleton_{n}", [n]) for n in range(1, 2001))
    for power in range(1, 19):
        base = 10**power
        for delta in (-2, -1, 0, 1, 2):
            value = base + delta
            if value > 0:
                generated.append((f"power10_{power}_{delta:+d}", [value]))

    rng = random.Random(SEED)
    for index in range(1000):
        length = rng.randrange(0, 21)
        values = [rng.randrange(1, 10**18 + 1) for _ in range(length)]
        generated.append((f"random_{index}", values))

    ordinary_mismatches = []
    for name, values in curated + generated:
        expected = outcome(canonical, values)
        actual = outcome(candidate, values)
        if expected != actual:
            ordinary_mismatches.append(
                {
                    "name": name,
                    "input": values,
                    "canonical": compact_outcome(expected),
                    "candidate": compact_outcome(actual),
                }
            )

    deep_cases = [
        ("deep_all_odd_1200_digits", int("1" * 1200)),
        ("deep_all_odd_2000_digits", int("1" * 2000)),
    ]
    deep_results = []
    for name, value in deep_cases:
        expected = outcome(canonical, [value])
        actual = outcome(candidate, [value])
        deep_results.append(
            {
                "name": name,
                "input_construction": f"int('1' * {len(str(value))})",
                "positive": value > 0,
                "canonical": compact_outcome(expected),
                "candidate": compact_outcome(actual),
                "match": expected == actual,
            }
        )

    report = {
        "oracle": str(CANONICAL_PATH),
        "candidate": str(CANDIDATE_PATH),
        "documented_examples": 2,
        "curated_case_count": len(curated),
        "exhaustive_singletons": "1..2000 inclusive",
        "power_of_ten_boundary_cases": 18 * 5,
        "random_seed": SEED,
        "random_case_count": 1000,
        "random_values": "list lengths 0..20; integers 1..10^18",
        "ordinary_case_count": len(curated) + len(generated),
        "ordinary_mismatch_count": len(ordinary_mismatches),
        "ordinary_mismatches": ordinary_mismatches,
        "deep_boundary_results": deep_results,
        "total_mismatch_count": len(ordinary_mismatches)
        + sum(not item["match"] for item in deep_results),
        "python_recursion_limit": sys.getrecursionlimit(),
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["total_mismatch_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
