#!/usr/bin/env python3
"""Compare trusted canonical and candidate entry points on a preserved corpus."""

from __future__ import annotations

import importlib.util
import json
import pathlib
import sys
from typing import Callable


def load_module(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def signed_digit_sum_oracle(value: int) -> int:
    digits = [int(char) for char in str(abs(value))]
    if value < 0:
        digits[0] = -digits[0]
    return sum(digits)


def oracle_count(values: list[int]) -> int:
    return sum(signed_digit_sum_oracle(value) > 0 for value in values)


def outcome(function: Callable[[list[int]], int], values: list[int]):
    try:
        return {"kind": "value", "value": function(values)}
    except BaseException as error:  # Record any observable Python divergence.
        return {
            "kind": "exception",
            "type": type(error).__name__,
            "message": str(error),
        }


def main() -> int:
    if len(sys.argv) != 4:
        print(
            f"usage: {sys.argv[0]} TRUSTED_CANONICAL.py CANDIDATE.py INPUTS.json",
            file=sys.stderr,
        )
        return 64

    canonical = load_module("audit_canonical", sys.argv[1])
    candidate = load_module("audit_candidate", sys.argv[2])
    corpus_path = pathlib.Path(sys.argv[3])
    corpus = json.loads(corpus_path.read_text(encoding="utf-8"))
    mismatches = []
    for index, case in enumerate(corpus["cases"]):
        values = case["arr"]
        expected = oracle_count(values)
        canonical_result = outcome(canonical.count_nums, values)
        candidate_result = outcome(candidate.count_nums, values)
        expected_result = {"kind": "value", "value": expected}
        if canonical_result != expected_result or candidate_result != expected_result:
            mismatches.append(
                {
                    "index": index,
                    "label": case["label"],
                    "arr": values,
                    "oracle": expected_result,
                    "canonical": canonical_result,
                    "candidate": candidate_result,
                }
            )

    digit_boundaries = {
        value: candidate.digit_sum(value)
        for value in [
            -1000, -999, -101, -100, -99, -98, -20, -19, -11, -10,
            -9, -8, -1, 0, 1, 8, 9, 10, 11, 19, 20, 98, 99, 100,
            101, 999, 1000,
        ]
    }
    bad_digit_boundaries = {
        value: result
        for value, result in digit_boundaries.items()
        if result != signed_digit_sum_oracle(value)
    }

    print(f"CORPUS: {corpus_path}")
    print(f"CASES: {len(corpus['cases'])}")
    print(f"MISMATCHES: {len(mismatches)}")
    for mismatch in mismatches[:20]:
        print(json.dumps(mismatch, sort_keys=True))
    print(f"DIGIT_BOUNDARY_CASES: {len(digit_boundaries)}")
    print(f"DIGIT_BOUNDARY_MISMATCHES: {len(bad_digit_boundaries)}")
    print("DOCUMENTED_EXAMPLES:")
    for case in corpus["cases"][:3]:
        print(
            json.dumps(
                {
                    "arr": case["arr"],
                    "candidate": candidate.count_nums(case["arr"]),
                    "canonical": canonical.count_nums(case["arr"]),
                },
                sort_keys=True,
            )
        )
    return 1 if mismatches or bad_digit_boundaries else 0


if __name__ == "__main__":
    raise SystemExit(main())
