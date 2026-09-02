#!/usr/bin/env python3
"""Reviewer-authored differential test of trusted canonical vs candidate."""

from __future__ import annotations

import importlib.util
from itertools import product
from pathlib import Path
from random import Random


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.smallest_change


canonical = load_function("trusted_canonical", Path("/reference/canonical.py"))
candidate = load_function("candidate_solution", Path("/candidate/solution.py"))


def check(case: list[int], label: str) -> None:
    expected = canonical(list(case))
    actual = candidate(list(case))
    if actual != expected:
        raise AssertionError(
            f"{label}: input={case!r} canonical={expected!r} candidate={actual!r}"
        )


def main() -> int:
    examples = [
        [1, 2, 3, 5, 4, 7, 9, 6],
        [1, 2, 3, 4, 3, 2, 2],
        [1, 2, 3, 2, 1],
    ]
    boundaries = [
        [],
        [0],
        [1, 1],
        [1, 2],
        [1, 2, 1],
        [1, 2, 2],
        [1, 2, 2, 1],
        [1, 2, 3, 1],
        [-10**100, 0, 10**100],
        [10**100, -10**100, -10**100, 10**100],
    ]
    cases = 0
    for index, case in enumerate(examples):
        check(case, f"example-{index}")
        cases += 1
    for index, case in enumerate(boundaries):
        check(case, f"boundary-{index}")
        cases += 1

    alphabet = (-2, 0, 3)
    exhaustive = 0
    for length in range(9):
        for values in product(alphabet, repeat=length):
            check(list(values), f"exhaustive-length-{length}")
            exhaustive += 1
            cases += 1

    rng = Random(730029)
    random_cases = 2_000
    for index in range(random_cases):
        length = rng.randrange(0, 65)
        case = [
            rng.choice(
                (
                    rng.randrange(-10**9, 10**9 + 1),
                    -10**100,
                    0,
                    10**100,
                )
            )
            for _ in range(length)
        ]
        check(case, f"random-{index}")
        cases += 1

    print("oracle=/reference/canonical.py::smallest_change")
    print("implementation=/candidate/solution.py::smallest_change")
    print(f"documented_examples={len(examples)}")
    print(f"boundary_cases={len(boundaries)}")
    print(
        f"exhaustive_cases={exhaustive} lengths=0..8 alphabet={alphabet!r}"
    )
    print(
        "random_cases="
        f"{random_cases} seed=730029 lengths=0..64 "
        "values=mixed[-1e9..1e9,-1e100,0,1e100]"
    )
    print(f"total_cases={cases}")
    print("mismatches=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
