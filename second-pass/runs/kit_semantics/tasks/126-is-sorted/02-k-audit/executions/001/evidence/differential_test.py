#!/usr/bin/env python3
"""Independent differential test for HumanEval 126 on its intended domain."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import random
from collections import Counter
from pathlib import Path
from types import ModuleType
from typing import Callable


CANONICAL = Path("/reference/canonical.py")
CANDIDATE = Path("/tmp/audit-work/126-is-sorted/solution.py")


def load(path: Path, name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def independent_oracle(values: list[int]) -> bool:
    return (
        all(values[index - 1] <= values[index]
            for index in range(1, len(values)))
        and all(count <= 2 for count in Counter(values).values())
    )


def branch_observations(values: list[int]) -> set[str]:
    observations = {
        "initial-sorted-true"
        if values == sorted(values)
        else "initial-sorted-false"
    }
    previous: tuple[int, ...] = (-1,)
    repeated = 0
    for value in values:
        if (value,) == previous:
            observations.add("same-as-previous")
            repeated += 1
        else:
            observations.add("different-from-previous")
            repeated = 1
        observations.add(
            "repeated-greater-than-2"
            if repeated > 2
            else "repeated-not-greater-than-2"
        )
        previous = (value,)
    return observations


def main() -> int:
    canonical: Callable[[list[int]], bool] = load(
        CANONICAL, "trusted_canonical"
    ).is_sorted
    candidate: Callable[[list[int]], bool] = load(
        CANDIDATE, "candidate_solution"
    ).is_sorted

    documented: list[tuple[list[int], bool]] = [
        ([5], True),
        ([1, 2, 3, 4, 5], True),
        ([1, 3, 2, 4, 5], False),
        ([1, 2, 3, 4, 5, 6], True),
        ([1, 2, 3, 4, 5, 6, 7], True),
        ([1, 3, 2, 4, 5, 6, 7], False),
        ([1, 2, 2, 3, 3, 4], True),
        ([1, 2, 2, 2, 3, 4], False),
    ]
    boundary: list[list[int]] = [
        [],
        [0],
        [0, 0],
        [0, 0, 0],
        [0, 0, 0, 0],
        [0, 1],
        [1, 0],
        [0, 1, 1, 2],
        [0, 1, 1, 1, 2],
        [1, 2, 1],
        [1, 1, 0],
        [0, 2, 0, 2],
        [10**100],
        [0, 10**100],
        [10**100, 10**100],
        [10**100, 10**100, 10**100],
    ]

    inputs: list[list[int]] = [values for values, _ in documented]
    inputs.extend(boundary)
    for length in range(8):
        inputs.extend(
            list(values)
            for values in itertools.product(range(5), repeat=length)
        )
    random_source = random.Random(126)
    for _ in range(2000):
        length = random_source.randrange(0, 31)
        inputs.append(
            [random_source.randrange(0, 101) for _ in range(length)]
        )

    digest = hashlib.sha256()
    mismatches: list[dict[str, object]] = []
    observed: set[str] = set()
    for index, values in enumerate(inputs):
        encoded = json.dumps(values, separators=(",", ":")).encode()
        digest.update(len(encoded).to_bytes(8, "big"))
        digest.update(encoded)
        expected = canonical(list(values))
        actual = candidate(list(values))
        oracle = independent_oracle(list(values))
        observed.update(branch_observations(values))
        if (
            type(expected) is not bool
            or type(actual) is not bool
            or expected != actual
            or expected != oracle
        ):
            mismatches.append(
                {
                    "index": index,
                    "input": values,
                    "canonical": expected,
                    "candidate": actual,
                    "independent_oracle": oracle,
                }
            )
            if len(mismatches) >= 20:
                break

    documented_failures = []
    for values, stated in documented:
        pair = (canonical(list(values)), candidate(list(values)))
        if pair != (stated, stated):
            documented_failures.append((values, stated, pair))

    required_observations = {
        "initial-sorted-true",
        "initial-sorted-false",
        "same-as-previous",
        "different-from-previous",
        "repeated-not-greater-than-2",
        "repeated-greater-than-2",
    }
    missing_observations = required_observations - observed
    print(f"canonical_path={CANONICAL}")
    print(f"candidate_path={CANDIDATE}")
    print(f"documented_examples={len(documented)}")
    print(f"boundary_cases={len(boundary)}")
    print("exhaustive_scope=lengths 0..7 over values 0..4")
    print("generated_scope=2000 seeded lists, lengths 0..30, values 0..100")
    print(f"total_inputs={len(inputs)}")
    print(f"ordered_input_sha256={digest.hexdigest()}")
    print(f"observed_branch_classes={sorted(observed)}")
    print(f"missing_branch_classes={sorted(missing_observations)}")
    print(f"documented_failures={documented_failures}")
    print(f"mismatch_count={len(mismatches)}")
    for mismatch in mismatches:
        print(f"MISMATCH {json.dumps(mismatch, sort_keys=True)}")
    return 1 if mismatches or documented_failures or missing_observations else 0


if __name__ == "__main__":
    raise SystemExit(main())
