#!/usr/bin/env python3
"""Independent differential test for HumanEval 142.

The trusted canonical implementation and the submitted implementation are
loaded from distinct paths.  The locally written contract oracle is used as a
second oracle and does not reuse either implementation.
"""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import random
import sys
from pathlib import Path
from types import ModuleType
from typing import Callable


CANONICAL_PATH = Path("/reference/canonical.py")
CANDIDATE_PATH = Path("/tmp/audit-work/reconstruction/solution.py")


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def contract_oracle(values: list[int]) -> int:
    total = 0
    for index, value in enumerate(values):
        if index % 3 == 0:
            total += value**2
        elif index % 4 == 0:
            total += value**3
        else:
            total += value
    return total


def main() -> int:
    canonical_module = load_module("trusted_humaneval_142", CANONICAL_PATH)
    candidate_module = load_module("submitted_humaneval_142", CANDIDATE_PATH)
    canonical: Callable[[list[int]], int] = canonical_module.sum_squares
    candidate: Callable[[list[int]], int] = candidate_module.sum_squares

    categorized_cases: list[tuple[str, list[int]]] = []

    documented = [
        [1, 2, 3],
        [],
        [-1, -5, 2, -1, -5],
    ]
    categorized_cases.extend(("documented", case) for case in documented)

    # Lengths straddling every relevant branch boundary through index 12.
    for length in range(0, 15):
        case = [(-1 if i % 2 else 1) * (i + 2) for i in range(length)]
        categorized_cases.append(("boundary-length", case))

    # Isolate each index classification (multiple of 3, only multiple of 4,
    # or neither) with both signed and zero values.
    for index in range(0, 14):
        for value in [-4, -1, 0, 1, 2, 5]:
            case = [0] * (index + 1)
            case[index] = value
            categorized_cases.append(("branch-isolation", case))

    # Complete finite product for short lists.
    product_values = [-3, -1, 0, 1, 2, 4]
    for length in range(0, 7):
        for values in itertools.product(product_values, repeat=length):
            categorized_cases.append(("cartesian-short", list(values)))

    # Deterministic broader generated sample.
    rng = random.Random(142_20260726)
    for _ in range(1000):
        length = rng.randrange(0, 51)
        case = [rng.randint(-1_000_000, 1_000_000) for _ in range(length)]
        categorized_cases.append(("seeded-random", case))

    categorized_cases.extend(
        [
            ("large-integer", [10**50, -(10**50), 10**75, -(10**75), 7]),
            ("large-integer", [-(10**100)] * 13),
            ("large-integer", [0] * 101),
        ]
    )

    corpus_digest = hashlib.sha256()
    mismatches: list[
        tuple[str, list[int], int, int, int, list[int], list[int]]
    ] = []
    category_counts: dict[str, int] = {}
    for category, original in categorized_cases:
        category_counts[category] = category_counts.get(category, 0) + 1
        corpus_digest.update(category.encode("utf-8"))
        corpus_digest.update(b"\0")
        corpus_digest.update(repr(original).encode("utf-8"))
        corpus_digest.update(b"\n")

        canonical_input = list(original)
        candidate_input = list(original)
        expected = contract_oracle(original)
        canonical_result = canonical(canonical_input)
        candidate_result = candidate(candidate_input)
        if (
            canonical_result != expected
            or candidate_result != expected
            or canonical_input != original
            or candidate_input != original
        ):
            mismatches.append(
                (
                    category,
                    original,
                    expected,
                    canonical_result,
                    candidate_result,
                    canonical_input,
                    candidate_input,
                )
            )
            if len(mismatches) >= 20:
                break

    print(f"canonical_path={CANONICAL_PATH}")
    print(f"candidate_path={CANDIDATE_PATH}")
    print(f"category_counts={category_counts}")
    print(f"total_cases={len(categorized_cases)}")
    print(f"input_corpus_sha256={corpus_digest.hexdigest()}")
    print(f"mismatch_count={len(mismatches)}")
    print(f"sample_empty={candidate([])}")
    print(f"sample_three={candidate([1, 2, 3])}")
    print(f"sample_negative={candidate([-1, -5, 2, -1, -5])}")
    for mismatch in mismatches:
        print(f"MISMATCH={mismatch!r}")
    return 1 if mismatches else 0


if __name__ == "__main__":
    sys.exit(main())
