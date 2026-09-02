#!/usr/bin/env python3
"""Independent differential test for HumanEval 33 sort_third."""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import itertools
import json
import random
import sys
from pathlib import Path
from typing import Callable


WORK = Path("/tmp/audit-work/audit-33-sort-third")


def load_entry(path: Path, module_name: str) -> Callable[[list[int]], list[int]]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sort_third


def contract_oracle(values: list[int]) -> list[int]:
    result = list(values)
    indices = list(range(0, len(values), 3))
    sorted_thirds = sorted(values[index] for index in indices)
    for index, value in zip(indices, sorted_thirds):
        result[index] = value
    return result


def main() -> int:
    canonical = load_entry(WORK / "canonical.py", "trusted_canonical")
    generated = load_entry(WORK / "solution.py", "submitted_solution")

    explicit_cases = [
        [],
        [1],
        [2, 1],
        [1, 2, 3],
        [4, 3, 2, 1],
        [5, 6, 3, 4, 8, 9, 2],
        [9, -1, 8, 6, -2, 5, 3, -3, 2, 0],
        [3, 3, 3, 3, 3, 3, 3],
        list(range(16)),
        list(range(15, -1, -1)),
    ]
    boundary_cases = []
    for length in range(0, 14):
        boundary_cases.extend(
            [
                list(range(length)),
                list(range(length, 0, -1)),
                [((index * 7) % 9) - 4 for index in range(length)],
            ]
        )

    exhaustive_cases = (
        list(values)
        for length in range(0, 8)
        for values in itertools.product(range(-2, 3), repeat=length)
    )

    rng = random.Random(0x33A11D17)
    random_cases = [
        [rng.randint(-1000, 1000) for _ in range(rng.randint(0, 100))]
        for _ in range(2500)
    ]

    mismatch_samples: list[dict[str, object]] = []
    mutation_samples: list[dict[str, object]] = []
    input_digest = hashlib.sha256()
    total = 0
    categories: dict[str, int] = {}

    def check(category: str, case: list[int]) -> None:
        nonlocal total
        original = copy.deepcopy(case)
        expected = contract_oracle(copy.deepcopy(case))
        canonical_input = copy.deepcopy(case)
        generated_input = copy.deepcopy(case)
        try:
            canonical_result = canonical(canonical_input)
            generated_result = generated(generated_input)
            observed: dict[str, object] = {
                "canonical": canonical_result,
                "generated": generated_result,
            }
        except Exception as error:  # A divergence includes an unexpected exception.
            observed = {"exception": f"{type(error).__name__}: {error}"}
            canonical_result = object()
            generated_result = object()

        input_digest.update(
            json.dumps([category, original], separators=(",", ":")).encode("utf-8")
        )
        input_digest.update(b"\n")
        total += 1
        categories[category] = categories.get(category, 0) + 1

        if not (
            canonical_result == expected
            and generated_result == expected
            and canonical_result == generated_result
        ):
            if len(mismatch_samples) < 10:
                mismatch_samples.append(
                    {
                        "category": category,
                        "input": original,
                        "expected": expected,
                        "observed": observed,
                    }
                )
        if canonical_input != original or generated_input != original:
            if len(mutation_samples) < 10:
                mutation_samples.append(
                    {
                        "category": category,
                        "input": original,
                        "canonical_after": canonical_input,
                        "generated_after": generated_input,
                    }
                )

    for case in explicit_cases:
        check("explicit", case)
    for case in boundary_cases:
        check("boundary", case)
    for case in exhaustive_cases:
        check("exhaustive_len_0_to_7_values_-2_to_2", case)
    for case in random_cases:
        check("random_seed_0x33A11D17", case)

    result = {
        "canonical_path": str(WORK / "canonical.py"),
        "generated_path": str(WORK / "solution.py"),
        "oracle": "independent index-list assignment of sorted values at indices 0 mod 3",
        "categories": categories,
        "total_cases": total,
        "input_stream_sha256": input_digest.hexdigest(),
        "mismatch_count": len(mismatch_samples),
        "mismatch_samples": mismatch_samples,
        "input_mutation_count": len(mutation_samples),
        "input_mutation_samples": mutation_samples,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not mismatch_samples and not mutation_samples else 1


if __name__ == "__main__":
    sys.exit(main())
