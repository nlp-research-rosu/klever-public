#!/usr/bin/env python3
"""Independent canonical-vs-candidate differential test for HumanEval/37."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path
from typing import Any, Callable


SCRATCH = Path("/tmp/audit-work/37-sort-even")


def load_entry(path: Path, module_name: str) -> Callable[[list[Any]], list[Any]]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sort_even


canonical = load_entry(SCRATCH / "canonical.py", "trusted_canonical")
candidate = load_entry(SCRATCH / "solution.py", "candidate_solution")


def contract_oracle(values: list[Any]) -> list[Any]:
    result = values.copy()
    result[::2] = sorted(values[::2])
    return result


def check_case(label: str, values: list[Any]) -> None:
    canonical_input = values.copy()
    candidate_input = values.copy()
    expected = contract_oracle(values)
    canonical_result = canonical(canonical_input)
    candidate_result = candidate(candidate_input)
    assert canonical_result == expected, (
        label,
        "canonical-contract mismatch",
        values,
        canonical_result,
        expected,
    )
    assert candidate_result == canonical_result, (
        label,
        "candidate-canonical mismatch",
        values,
        candidate_result,
        canonical_result,
    )
    assert canonical_input == values, (label, "canonical mutated input")
    assert candidate_input == values, (label, "candidate mutated input")
    assert canonical_result is not canonical_input, (label, "canonical returned input")
    assert candidate_result is not candidate_input, (label, "candidate returned input")
    assert candidate_result[1::2] == values[1::2], (
        label,
        "odd positions changed",
    )
    assert candidate_result[::2] == sorted(values[::2]), (
        label,
        "even projection not sorted",
    )


def main() -> None:
    documented_and_boundaries: list[tuple[str, list[Any]]] = [
        ("example-odd", [1, 2, 3]),
        ("example-even", [5, 6, 3, 4]),
        ("empty", []),
        ("singleton", [7]),
        ("length-2", [2, 1]),
        ("length-3-reverse-even", [9, 8, 3]),
        ("length-4-duplicates", [2, 4, 2, 1]),
        ("length-5-negatives", [5, -9, -1, 8, 0]),
        ("already-sorted-even-projection", [-4, 7, 0, 2, 3, 1]),
        ("strings", ["z", "odd-a", "a", "odd-b", "m"]),
        ("floats", [3.5, -1.25, -2.0, 8.0]),
        (
            "odd-positions-need-not-be-comparable",
            [3, {"odd": 1}, 1, {"odd": 2}],
        ),
    ]
    total = 0
    for label, values in documented_and_boundaries:
        check_case(label, values)
        print(
            f"BOUNDARY {label}: input={values!r} "
            f"output={candidate(values.copy())!r}"
        )
        total += 1

    exhaustive_domain = (-2, -1, 0, 1, 2)
    exhaustive_count = 0
    for length in range(0, 7):
        for values_tuple in itertools.product(exhaustive_domain, repeat=length):
            check_case(f"exhaustive-len-{length}", list(values_tuple))
            exhaustive_count += 1
    total += exhaustive_count

    seed = 0x37E
    rng = random.Random(seed)
    generated_count = 5000
    for index in range(generated_count):
        length = rng.randrange(0, 41)
        values = [rng.randrange(-10_000, 10_001) for _ in range(length)]
        check_case(f"generated-{index}", values)
    total += generated_count

    print(f"EXHAUSTIVE domain={exhaustive_domain} lengths=0..6 cases={exhaustive_count}")
    print(
        f"GENERATED seed={seed} lengths=0..40 values=-10000..10000 "
        f"cases={generated_count}"
    )
    print(f"DIFFERENTIAL PASS total_cases={total} mismatches=0")


if __name__ == "__main__":
    main()
