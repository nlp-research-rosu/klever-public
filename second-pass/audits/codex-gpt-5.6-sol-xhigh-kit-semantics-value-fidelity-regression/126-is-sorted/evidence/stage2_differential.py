#!/usr/bin/env python3
"""Independent candidate/canonical differential test for HumanEval 126."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import random
from collections import Counter
from pathlib import Path
from types import ModuleType
from typing import Callable


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def independent_oracle(values: list[int]) -> bool:
    adjacent_ordered = all(
        left <= right for left, right in zip(values, values[1:])
    )
    multiplicities_ok = all(count <= 2 for count in Counter(values).values())
    return adjacent_ordered and multiplicities_ok


def add_unique(cases: list[list[int]], seen: set[tuple[int, ...]], case: list[int]) -> None:
    key = tuple(case)
    if key not in seen:
        seen.add(key)
        cases.append(case)


def build_cases() -> tuple[list[list[int]], dict[str, int]]:
    cases: list[list[int]] = []
    seen: set[tuple[int, ...]] = set()

    examples = [
        [5],
        [1, 2, 3, 4, 5],
        [1, 3, 2, 4, 5],
        [1, 2, 3, 4, 5, 6],
        [1, 2, 3, 4, 5, 6, 7],
        [1, 3, 2, 4, 5, 6, 7],
        [1, 2, 2, 3, 3, 4],
        [1, 2, 2, 2, 3, 4],
    ]
    boundaries = [
        [],
        [0],
        [0, 0],
        [0, 0, 0],
        [0, 0, 0, 0],
        [0, 1],
        [1, 0],
        [1, 1],
        [1, 1, 0],
        [2, 1, 1],
        [1, 2, 1],
        [0, 1, 1, 2, 2],
        [0, 1, 1, 1, 2],
        [10**100, 10**100],
        [10**100, 10**100, 10**100],
        [0, 10**100],
        [10**100, 0],
    ]
    for case in examples + boundaries:
        add_unique(cases, seen, case)
    after_named = len(cases)

    for length in range(7):
        for values in itertools.product(range(5), repeat=length):
            add_unique(cases, seen, list(values))
    after_exhaustive = len(cases)

    rng = random.Random(126)
    for _ in range(1000):
        length = rng.randrange(31)
        case = [rng.randrange(21) for _ in range(length)]
        add_unique(cases, seen, case)

    return cases, {
        "named_unique": after_named,
        "exhaustive_unique_after_named": after_exhaustive,
        "random_unique_added": len(cases) - after_exhaustive,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--canonical", required=True, type=Path)
    parser.add_argument("--generated", required=True, type=Path)
    parser.add_argument("--inputs-out", required=True, type=Path)
    args = parser.parse_args()

    canonical_module = load_module("trusted_canonical_126", args.canonical)
    generated_module = load_module("candidate_solution_126", args.generated)
    canonical: Callable[[list[int]], bool] = canonical_module.is_sorted
    generated: Callable[[list[int]], bool] = generated_module.is_sorted

    cases, groups = build_cases()
    mismatches: list[dict[str, object]] = []
    digest = hashlib.sha256()
    with args.inputs_out.open("w", encoding="utf-8") as inputs_file:
        for case_id, values in enumerate(cases):
            serialized = json.dumps(
                {"id": case_id, "input": values},
                separators=(",", ":"),
                sort_keys=True,
            )
            inputs_file.write(serialized + "\n")
            digest.update((serialized + "\n").encode())

            canonical_result = canonical(values.copy())
            generated_result = generated(values.copy())
            oracle_result = independent_oracle(values)
            if not (
                canonical_result == generated_result == oracle_result
                and isinstance(canonical_result, bool)
                and isinstance(generated_result, bool)
            ):
                mismatches.append(
                    {
                        "id": case_id,
                        "input": values,
                        "canonical": canonical_result,
                        "generated": generated_result,
                        "oracle": oracle_result,
                    }
                )

    print(f"GROUP_COUNTS={json.dumps(groups, sort_keys=True)}")
    print(f"TOTAL_CASES={len(cases)}")
    print(f"INPUTS_SHA256={digest.hexdigest()}")
    print(f"MISMATCHES={len(mismatches)}")
    for mismatch in mismatches[:20]:
        print(f"MISMATCH={json.dumps(mismatch, sort_keys=True)}")
    return 0 if not mismatches else 1


if __name__ == "__main__":
    raise SystemExit(main())
