#!/usr/bin/env python3
"""Independent differential test for HumanEval/69 search."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path
from typing import Any, Callable


def load_entry(path: Path, module_name: str) -> Callable[[list[int]], int]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.search


def observe(function: Callable[[list[int]], int], value: list[int]) -> tuple[Any, ...]:
    try:
        return ("return", function(list(value)))
    except Exception as error:  # Deliberately records out-of-domain behavior.
        return ("raise", type(error).__name__, str(error))


def main() -> None:
    canonical = load_entry(
        Path("/tmp/audit-work/trusted/canonical.py"), "trusted_canonical_69"
    )
    generated = load_entry(
        Path("/tmp/audit-work/candidate-src/solution.py"), "candidate_solution_69"
    )

    directed: list[tuple[str, list[int], int]] = [
        ("example_one", [4, 1, 2, 2, 3, 1], 2),
        ("example_two", [1, 2, 2, 3, 3, 3, 4, 4, 4], 3),
        ("example_three", [5, 5, 4, 4, 4], -1),
        ("singleton_qualifies", [1], 1),
        ("singleton_fails_outer_if", [2], -1),
        ("frequency_just_below_value", [3, 3], -1),
        ("frequency_equals_value", [3, 3, 3], 3),
        ("frequency_above_value", [2, 2, 2], 2),
        ("inner_if_false_after_larger_answer", [2, 2, 1], 2),
        ("multiple_qualifiers_choose_greatest", [1, 2, 2, 3, 3, 3], 3),
        ("large_value_absent_frequency", [1000], -1),
        ("all_ones", [1, 1, 1, 1], 1),
    ]
    for label, values, expected in directed:
        canonical_observation = observe(canonical, values)
        generated_observation = observe(generated, values)
        print(
            f"DIRECTED {label} input={values} "
            f"canonical={canonical_observation} generated={generated_observation}"
        )
        assert canonical_observation == ("return", expected)
        assert generated_observation == canonical_observation

    empty_canonical = observe(canonical, [])
    empty_generated = observe(generated, [])
    print(
        "OUT_OF_DOMAIN_EMPTY "
        f"canonical={empty_canonical} generated={empty_generated}"
    )
    assert empty_canonical[0] == "raise"
    assert empty_generated == ("return", -1)

    exhaustive_cases = 0
    exhaustive_mismatches = 0
    for length in range(1, 7):
        for values_tuple in itertools.product(range(1, 6), repeat=length):
            values = list(values_tuple)
            exhaustive_cases += 1
            if observe(canonical, values) != observe(generated, values):
                exhaustive_mismatches += 1
                if exhaustive_mismatches <= 10:
                    print(f"EXHAUSTIVE_MISMATCH input={values}")

    rng = random.Random(690069)
    random_cases = 2000
    random_mismatches = 0
    for _ in range(random_cases):
        length = rng.randint(1, 80)
        values = [rng.randint(1, 1000) for _ in range(length)]
        if observe(canonical, values) != observe(generated, values):
            random_mismatches += 1
            if random_mismatches <= 10:
                print(f"RANDOM_MISMATCH input={values}")

    print(
        "EXHAUSTIVE_SCOPE lengths=1..6 values=1..5 "
        f"cases={exhaustive_cases} mismatches={exhaustive_mismatches}"
    )
    print(
        "RANDOM_SCOPE seed=690069 lengths=1..80 values=1..1000 "
        f"cases={random_cases} mismatches={random_mismatches}"
    )
    assert exhaustive_cases == sum(5**length for length in range(1, 7))
    assert exhaustive_mismatches == 0
    assert random_mismatches == 0
    print("INTENDED_DOMAIN_DIFFERENTIAL_PASS")


if __name__ == "__main__":
    main()
