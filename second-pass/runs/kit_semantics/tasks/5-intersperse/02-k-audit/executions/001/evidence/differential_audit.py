#!/usr/bin/env python3
"""Independent differential audit for HumanEval/5 intersperse."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/intersperse-audit")
CANONICAL_PATH = SCRATCH / "canonical.py"
GENERATED_PATH = SCRATCH / "solution.py"


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.intersperse


def check_case(canonical, generated, numbers: list[int], delimiter: int, label: str):
    canonical_input = list(numbers)
    generated_input = list(numbers)
    expected = canonical(canonical_input, delimiter)
    actual = generated(generated_input, delimiter)
    mismatch = actual != expected
    mutation = canonical_input != numbers or generated_input != numbers
    if mismatch or mutation:
        raise AssertionError(
            f"{label}: numbers={numbers!r}, delimiter={delimiter!r}, "
            f"canonical={expected!r}, generated={actual!r}, "
            f"canonical_input_after={canonical_input!r}, "
            f"generated_input_after={generated_input!r}"
        )
    return expected


def main() -> None:
    canonical = load_entry(CANONICAL_PATH, "trusted_canonical")
    generated = load_entry(GENERATED_PATH, "audited_generated")

    hand_cases = [
        ([], 4, "documented-empty"),
        ([1, 2, 3], 4, "documented-example"),
        ([7], -2, "singleton-loop-first-branch"),
        ([7, 8], -2, "two-elements-both-if-boundaries"),
        ([1, 2], 4, "formal-entry-ground-witness"),
        ([0, 0, 0], 0, "zero-values-and-equal-delimiter"),
        ([-3, -1, 2], -3, "negative-and-delimiter-equals-element"),
        ([10**100, -(10**100)], 10**100, "unbounded-integer-boundary"),
    ]
    print("HAND_CASES")
    for numbers, delimiter, label in hand_cases:
        result = check_case(canonical, generated, numbers, delimiter, label)
        print(
            f"{label}: numbers={numbers!r} delimiter={delimiter!r} "
            f"result={result!r}"
        )

    values = (-3, -1, 0, 1, 2, 7)
    delimiters = (-4, 0, 3)
    exhaustive_cases = 0
    for length in range(7):
        for numbers_tuple in itertools.product(values, repeat=length):
            for delimiter in delimiters:
                check_case(
                    canonical,
                    generated,
                    list(numbers_tuple),
                    delimiter,
                    "exhaustive",
                )
                exhaustive_cases += 1
    print(
        "EXHAUSTIVE_SCOPE "
        f"lengths=0..6 values={values!r} delimiters={delimiters!r} "
        f"cases={exhaustive_cases}"
    )

    rng = random.Random(0x5EED)
    random_cases = 2000
    for index in range(random_cases):
        length = rng.randrange(0, 51)
        numbers = [rng.randrange(-(10**9), 10**9 + 1) for _ in range(length)]
        delimiter = rng.randrange(-(10**9), 10**9 + 1)
        check_case(canonical, generated, numbers, delimiter, f"random-{index}")
    print(
        "RANDOM_SCOPE seed=0x5EED cases=2000 lengths=0..50 "
        "values_and_delimiters=[-1000000000,1000000000]"
    )
    print(
        f"TOTAL_CASES={len(hand_cases) + exhaustive_cases + random_cases} "
        "MISMATCHES=0 INPUT_MUTATIONS=0"
    )


if __name__ == "__main__":
    main()
