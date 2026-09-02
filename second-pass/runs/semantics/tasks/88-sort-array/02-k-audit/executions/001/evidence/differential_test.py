#!/usr/bin/env python3
"""Independent differential/contract tests for HumanEval problem 88."""

from __future__ import annotations

import argparse
import importlib.util
import itertools
import json
import random
from pathlib import Path
from types import ModuleType
from typing import Callable


def load_module(path: Path, name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def expected_from_contract(values: list[int]) -> list[int]:
    if not values:
        return []
    reverse = (values[0] + values[-1]) % 2 == 0
    return sorted(values, reverse=reverse)


def check_one(
    values: list[int],
    canonical: Callable[[list[int]], list[int]],
    generated: Callable[[list[int]], list[int]],
) -> tuple[str, int]:
    original_canonical = list(values)
    original_generated = list(values)
    canonical_result = canonical(original_canonical)
    generated_result = generated(original_generated)
    expected = expected_from_contract(values)

    assert original_canonical == values, ("canonical mutated input", values)
    assert original_generated == values, ("generated mutated input", values)
    assert canonical_result is not original_canonical, ("canonical did not copy", values)
    assert generated_result is not original_generated, ("generated did not copy", values)
    assert canonical_result == expected, ("canonical vs contract", values, canonical_result, expected)
    assert generated_result == expected, ("generated vs contract", values, generated_result, expected)
    assert generated_result == canonical_result, (
        "differential mismatch",
        values,
        canonical_result,
        generated_result,
    )

    if not values:
        return "empty", 0
    return ("even" if (values[0] + values[-1]) % 2 == 0 else "odd"), len(values)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--canonical", type=Path, required=True)
    parser.add_argument("--generated", type=Path, required=True)
    parser.add_argument("--inputs-out", type=Path, required=True)
    args = parser.parse_args()

    canonical_module = load_module(args.canonical, "trusted_canonical")
    generated_module = load_module(args.generated, "candidate_generated")
    canonical = canonical_module.sort_array
    generated = generated_module.sort_array

    documented = [
        [],
        [5],
        [2, 4, 3, 0, 1, 5],
        [2, 4, 3, 0, 1, 5, 6],
    ]
    boundaries = [
        [0],
        [1],
        [0, 0],
        [0, 1],
        [1, 0],
        [1, 1],
        [2, 1],
        [2, 2],
        [3, 2],
        [3, 3],
        [0, 5, 0],
        [0, 5, 1],
        [1, 5, 0],
        [1, 5, 1],
        [2**63, 0, 2**63 + 1],
        [10**100, 7, 10**100],
        [4, 4, 2, 2, 0, 0],
        [4, 4, 2, 2, 0, 1],
    ]

    exhaustive: list[list[int]] = []
    for length in range(0, 6):
        exhaustive.extend([list(x) for x in itertools.product(range(5), repeat=length)])

    rng = random.Random(880024)
    generated_cases = [
        [rng.randrange(0, 1_000_001) for _ in range(rng.randrange(0, 31))]
        for _ in range(1000)
    ]

    cases = documented + boundaries + exhaustive + generated_cases
    args.inputs_out.write_text(
        json.dumps(
            {
                "random_seed": 880024,
                "documented": documented,
                "boundaries": boundaries,
                "exhaustive_values": [0, 1, 2, 3, 4],
                "exhaustive_lengths": [0, 1, 2, 3, 4, 5],
                "all_cases_in_execution_order": cases,
            },
            separators=(",", ":"),
        )
        + "\n",
        encoding="utf-8",
    )

    branch_counts = {"empty": 0, "odd": 0, "even": 0}
    length_counts: dict[int, int] = {}
    for values in cases:
        branch, length = check_one(values, canonical, generated)
        branch_counts[branch] += 1
        length_counts[length] = length_counts.get(length, 0) + 1

    print(f"documented_cases={len(documented)}")
    print(f"boundary_cases={len(boundaries)}")
    print(f"exhaustive_cases={len(exhaustive)}")
    print(f"seeded_generated_cases={len(generated_cases)}")
    print(f"total_cases={len(cases)}")
    print(f"branch_counts={branch_counts}")
    print(f"observed_lengths={sorted(length_counts)}")
    print("mismatches=0")
    print("mutation_failures=0")
    print("copy_identity_failures=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
