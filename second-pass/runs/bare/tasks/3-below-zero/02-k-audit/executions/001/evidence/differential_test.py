#!/usr/bin/env python3
"""Independent differential test for HumanEval/3 below_zero."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import random
from pathlib import Path
from typing import Callable


def load_entry(path: Path, module_name: str) -> Callable[[list[int]], bool]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.below_zero


def build_cases() -> tuple[list[list[int]], dict[str, object]]:
    named = [
        [],
        [1, 2, 3],
        [1, 2, -4, 5],
        [-1],
        [0],
        [1],
        [1, -1],
        [1, -2],
        [5, -5],
        [5, -5, -1],
        [-(10**100)],
        [10**100, -(10**100)],
        [10**100, -(10**100) - 1],
        [2, -1, -1, -1],
    ]

    exhaustive: list[list[int]] = [[]]
    alphabet = list(range(-3, 4))
    for length in range(1, 6):
        prior = [[]]
        for _ in range(length):
            prior = [prefix + [value] for prefix in prior for value in alphabet]
        exhaustive.extend(prior)

    rng = random.Random(0x3B3E10)
    generated = [
        [rng.randint(-(10**9), 10**9) for _ in range(rng.randint(0, 30))]
        for _ in range(1000)
    ]

    unique: list[list[int]] = []
    seen: set[tuple[int, ...]] = set()
    for case in named + exhaustive + generated:
        key = tuple(case)
        if key not in seen:
            seen.add(key)
            unique.append(case)

    scope = {
        "named_cases": named,
        "exhaustive_alphabet": alphabet,
        "exhaustive_lengths": [0, 1, 2, 3, 4, 5],
        "random_seed": "0x3B3E10",
        "random_case_count": 1000,
        "random_length_range": [0, 30],
        "random_value_range": [-(10**9), 10**9],
        "deduplicated_case_count": len(unique),
    }
    return unique, scope


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--canonical", type=Path, required=True)
    parser.add_argument("--generated", type=Path, required=True)
    parser.add_argument("--inputs-out", type=Path, required=True)
    parser.add_argument("--results-out", type=Path, required=True)
    args = parser.parse_args()

    canonical = load_entry(args.canonical, "trusted_canonical")
    generated = load_entry(args.generated, "candidate_generated")
    cases, scope = build_cases()

    args.inputs_out.write_text(
        json.dumps({"scope": scope, "cases": cases}, indent=2) + "\n",
        encoding="utf-8",
    )

    results: list[dict[str, object]] = []
    mismatch_count = 0
    non_bool_count = 0
    for operations in cases:
        expected = canonical(list(operations))
        actual = generated(list(operations))
        if type(actual) is not bool:
            non_bool_count += 1
        if actual != expected or type(actual) is not type(expected):
            mismatch_count += 1
        results.append(
            {
                "operations": operations,
                "canonical": expected,
                "generated": actual,
                "match": actual == expected and type(actual) is type(expected),
            }
        )

    encoded_results = (json.dumps(results, separators=(",", ":")) + "\n").encode()
    args.results_out.write_bytes(encoded_results)
    print(f"cases={len(cases)}")
    print(f"mismatches={mismatch_count}")
    print(f"non_bool_results={non_bool_count}")
    print(f"results_sha256={hashlib.sha256(encoded_results).hexdigest()}")
    return 1 if mismatch_count or non_bool_count else 0


if __name__ == "__main__":
    raise SystemExit(main())
