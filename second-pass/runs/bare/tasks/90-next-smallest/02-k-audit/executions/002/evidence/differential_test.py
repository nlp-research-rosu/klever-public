#!/usr/bin/env python3
"""Independent differential and branch-boundary tests for next_smallest."""

from __future__ import annotations

import importlib.util
import itertools
from pathlib import Path
import random


ROOT = Path("/tmp/audit-work/90-next-smallest")


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.next_smallest


def independent_oracle(values: list[int]):
    """Two-minimum scan, intentionally not implemented with set/sorted."""
    least = None
    second = None
    for value in values:
        if least is None or value < least:
            if least is None or value != least:
                second = least
            least = value
        elif value != least and (second is None or value < second):
            second = value
    return second


def main() -> int:
    canonical = load_function(
        "trusted_canonical", ROOT / "reference" / "canonical.py"
    )
    generated = load_function(
        "generated_solution", ROOT / "candidate-src" / "solution.py"
    )

    named_cases = [
        ("documented_sorted", [1, 2, 3, 4, 5]),
        ("documented_permuted", [5, 1, 4, 3, 2]),
        ("documented_empty", []),
        ("documented_duplicate_pair", [1, 1]),
        ("one_element", [0]),
        ("two_distinct_ascending", [-1, 4]),
        ("two_distinct_descending", [4, -1]),
        ("two_values_many_duplicates", [9, 9, -8, 9, -8]),
        ("negative_boundary", [-5, -5, -4]),
        ("all_equal_long", [7] * 30),
        ("large_python_ints", [10**100, -(10**100), 0, 10**100]),
        ("second_is_repeated", [3, 1, 2, 2, 8, 1]),
    ]

    checked = 0
    for label, values in named_cases:
        expected = independent_oracle(values)
        actual_canonical = canonical(list(values))
        actual_generated = generated(list(values))
        print(
            f"NAMED {label}: input={values!r} expected={expected!r} "
            f"canonical={actual_canonical!r} generated={actual_generated!r}"
        )
        assert actual_canonical == expected
        assert actual_generated == expected
        checked += 1

    alphabet = (-3, -1, 0, 2, 5)
    exhaustive = 0
    for length in range(7):
        for values_tuple in itertools.product(alphabet, repeat=length):
            values = list(values_tuple)
            expected = independent_oracle(values)
            assert canonical(list(values)) == expected
            assert generated(list(values)) == expected
            exhaustive += 1
            checked += 1

    random_generator = random.Random(90090)
    random_count = 1000
    for _ in range(random_count):
        length = random_generator.randrange(0, 61)
        values = [
            random_generator.randrange(-(10**12), 10**12 + 1)
            for _ in range(length)
        ]
        # Deliberately create duplicates in about half the cases.
        if values and random_generator.randrange(2) == 0:
            values.extend(values[: random_generator.randrange(0, len(values) + 1)])
        expected = independent_oracle(values)
        assert canonical(list(values)) == expected
        assert generated(list(values)) == expected
        checked += 1

    print(
        "DIFFERENTIAL_STATUS OK "
        f"named={len(named_cases)} "
        f"exhaustive={exhaustive} alphabet={alphabet} lengths=0..6 "
        f"random={random_count} seed=90090 total={checked} mismatches=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
