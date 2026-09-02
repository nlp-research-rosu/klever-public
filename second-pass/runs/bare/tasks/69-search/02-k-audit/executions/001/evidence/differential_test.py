#!/usr/bin/env python3
"""Independent differential check for HumanEval 69-search.

The oracle and candidate are loaded from separate, explicit file paths. The
in-domain corpus contains the three documented examples, named branch/boundary
cases, every positive list over 1..5 of lengths 1..6, and a deterministic
broader random sample. Empty/zero/negative cases are retained separately as
out-of-domain diagnostics.
"""

from __future__ import annotations

import argparse
import importlib.util
import itertools
import json
import random
from pathlib import Path
from typing import Any, Callable


def load_search(path: Path, module_name: str) -> Callable[[list[int]], int]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.search


def outcome(fn: Callable[[list[int]], int], values: list[int]) -> dict[str, Any]:
    try:
        return {"kind": "return", "value": fn(values.copy())}
    except Exception as err:  # The exception type is part of boundary behavior.
        return {"kind": "raise", "type": type(err).__name__, "message": str(err)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--canonical", type=Path, required=True)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--inputs-jsonl", type=Path, required=True)
    args = parser.parse_args()

    oracle = load_search(args.canonical, "audit_trusted_canonical")
    candidate = load_search(args.candidate, "audit_candidate_solution")

    documented = [
        ("example_one", [4, 1, 2, 2, 3, 1]),
        ("example_two", [1, 2, 2, 3, 3, 3, 4, 4, 4]),
        ("example_three", [5, 5, 4, 4, 4]),
    ]
    boundaries = [
        ("minimum_qualifies", [1]),
        ("single_two_fails_count", [2]),
        ("two_at_threshold", [2, 2]),
        ("three_below_threshold", [3, 3]),
        ("three_at_threshold", [3, 3, 3]),
        ("qualified_smaller_then_unqualified_larger", [1, 4]),
        ("both_qualify_larger_wins", [1, 2, 2]),
        ("duplicate_candidate_revisits_value_gt_answer_false", [2, 2, 2]),
        ("order_permutation", [3, 1, 3, 2, 3, 2]),
        ("large_value_fails", [1000000]),
    ]
    out_of_domain = [
        ("empty", []),
        ("contains_zero", [0]),
        ("contains_negative", [-2, -2, 1]),
    ]

    cases: list[tuple[str, list[int], bool, str]] = []
    for name, values in documented:
        cases.append((name, values, True, "documented"))
    for name, values in boundaries:
        cases.append((name, values, True, "boundary"))
    for length in range(1, 7):
        for values in itertools.product(range(1, 6), repeat=length):
            cases.append(("", list(values), True, "exhaustive_1_to_5_len_1_to_6"))

    rng = random.Random(690069)
    for index in range(2000):
        length = rng.randint(1, 40)
        values = [rng.randint(1, 100) for _ in range(length)]
        cases.append((f"random_{index}", values, True, "deterministic_random"))
    for name, values in out_of_domain:
        cases.append((name, values, False, "out_of_domain_diagnostic"))

    mismatches: list[dict[str, Any]] = []
    in_domain_count = 0
    out_of_domain_count = 0
    with args.inputs_jsonl.open("w", encoding="utf-8") as corpus:
        for index, (name, values, in_domain, group) in enumerate(cases):
            if in_domain:
                in_domain_count += 1
            else:
                out_of_domain_count += 1
            expected = outcome(oracle, values)
            actual = outcome(candidate, values)
            record = {
                "index": index,
                "name": name,
                "group": group,
                "in_domain": in_domain,
                "input": values,
                "canonical": expected,
                "candidate": actual,
                "match": expected == actual,
            }
            corpus.write(json.dumps(record, sort_keys=True) + "\n")
            if expected != actual:
                mismatches.append(record)

    in_domain_mismatches = [item for item in mismatches if item["in_domain"]]
    out_domain_mismatches = [item for item in mismatches if not item["in_domain"]]
    summary = {
        "canonical": str(args.canonical),
        "candidate": str(args.candidate),
        "in_domain_cases": in_domain_count,
        "in_domain_mismatches": len(in_domain_mismatches),
        "out_of_domain_cases": out_of_domain_count,
        "out_of_domain_mismatches": len(out_domain_mismatches),
        "out_of_domain_details": out_domain_mismatches,
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 1 if in_domain_mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
