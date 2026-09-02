#!/usr/bin/env python3
"""Independent differential test for HumanEval 26 remove_duplicates."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


CANONICAL_PATH = Path("/tmp/audit-work/trusted/canonical.py")
CANDIDATE_PATH = Path("/tmp/audit-work/candidate-scratch/solution.py")


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.remove_duplicates


canonical = load_entry(CANONICAL_PATH, "trusted_canonical")
candidate = load_entry(CANDIDATE_PATH, "generated_candidate")


def independent_spec(numbers: list[int]) -> list[int]:
    return [
        number
        for number in numbers
        if sum(1 for other in numbers if other == number) == 1
    ]


def check(numbers: list[int]) -> None:
    expected = canonical(list(numbers))
    actual = candidate(list(numbers))
    mathematical = independent_spec(list(numbers))
    if actual != expected or expected != mathematical:
        raise AssertionError(
            f"mismatch input={numbers!r} candidate={actual!r} "
            f"canonical={expected!r} mathematical={mathematical!r}"
        )


def main() -> None:
    directed = [
        [],
        [1],
        [1, 2, 3, 2, 4],
        [1, 1],
        [1, 1, 1],
        [1, 2],
        [2, 1, 2],
        [2, 1, 1],
        [1, 2, 1, 3, 2, 4, 3, 5],
        [0, -1, 0, 2, -1, 3],
        [-(2**200), 0, 2**200, -(2**200)],
        [2**1000, -(2**1000), 2**1000, 7],
        list(range(100)),
        list(range(50)) + list(range(50)),
    ]
    for case in directed:
        check(case)

    alphabet = (-2, -1, 0, 1, 2)
    exhaustive_count = 0
    for length in range(8):
        for values in itertools.product(alphabet, repeat=length):
            check(list(values))
            exhaustive_count += 1

    randomizer = random.Random(0x26D0)
    random_count = 2000
    for _ in range(random_count):
        length = randomizer.randrange(0, 41)
        values = [
            randomizer.choice(
                (
                    randomizer.randrange(-20, 21),
                    randomizer.randrange(-(2**130), 2**130),
                )
            )
            for _ in range(length)
        ]
        check(values)

    print("oracle: trusted canonical.py remove_duplicates")
    print("cross_check: independently coded singleton-occurrence filter")
    print("directed_cases:", len(directed))
    print(
        "exhaustive_cases:",
        exhaustive_count,
        "all lists of lengths 0..7 over",
        alphabet,
    )
    print(
        "seeded_random_cases:",
        random_count,
        "lengths 0..40 with small and 130-bit integers, seed=0x26D0",
    )
    print("mismatches: 0")


if __name__ == "__main__":
    main()
