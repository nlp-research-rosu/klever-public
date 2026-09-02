#!/usr/bin/env python3
"""Independent differential tests for HumanEval/42 incr_list."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path
from typing import Any, Callable


CANONICAL_PATH = Path("/reference/canonical.py")
GENERATED_PATH = Path("/tmp/audit-work/42-incr-list-audit/solution.py")
SEED = 420042


def load_entry(path: Path, module_name: str) -> Callable[[list[Any]], list[Any]]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    entry = getattr(module, "incr_list")
    assert callable(entry)
    return entry


def same_value(left: Any, right: Any) -> bool:
    return type(left) is type(right) and left == right


def check_case(
    case_id: str,
    original: list[Any],
    canonical: Callable[[list[Any]], list[Any]],
    generated: Callable[[list[Any]], list[Any]],
) -> None:
    canonical_input = list(original)
    generated_input = list(original)
    canonical_result = canonical(canonical_input)
    generated_result = generated(generated_input)
    assert canonical_input == original, f"canonical mutated input: {case_id}"
    assert generated_input == original, f"generated mutated input: {case_id}"
    assert canonical_result is not canonical_input, f"canonical aliased input: {case_id}"
    assert generated_result is not generated_input, f"generated aliased input: {case_id}"
    assert len(canonical_result) == len(generated_result), f"length mismatch: {case_id}"
    assert all(
        same_value(left, right)
        for left, right in zip(canonical_result, generated_result, strict=True)
    ), f"value/type mismatch: {case_id}: {canonical_result!r} != {generated_result!r}"


def exception_kind(function: Callable[[list[Any]], list[Any]], value: list[Any]) -> type[BaseException] | None:
    try:
        function(value)
    except BaseException as err:  # Test exception parity, do not suppress the kind.
        return type(err)
    return None


def main() -> None:
    canonical = load_entry(CANONICAL_PATH, "trusted_canonical_42")
    generated = load_entry(GENERATED_PATH, "candidate_solution_42")

    documented = [
        [1, 2, 3],
        [5, 3, 5, 2, 3, 3, 9, 0, 123],
    ]
    boundaries = [
        [],
        [0],
        [-1],
        [1],
        [-(10**100), 10**100],
        [-2, -1],
        [0, 1],
        [0, 1, 2],
    ]

    cases: list[tuple[str, list[Any]]] = []
    cases.extend((f"documented-{index}", value) for index, value in enumerate(documented))
    cases.extend((f"boundary-{index}", value) for index, value in enumerate(boundaries))

    exhaustive_count = 0
    for length in range(0, 6):
        for values in itertools.product(range(-2, 3), repeat=length):
            cases.append((f"exhaustive-{length}-{exhaustive_count}", list(values)))
            exhaustive_count += 1

    rng = random.Random(SEED)
    generated_count = 1000
    for index in range(generated_count):
        length = rng.randrange(0, 65)
        value = [rng.randrange(-(10**80), 10**80) for _ in range(length)]
        cases.append((f"generated-{index}", value))

    extended_numeric = [
        [True, False],
        [0.0, -1.5, 2.25],
        [True, 3, -0.5, False],
    ]
    cases.extend((f"extended-numeric-{index}", value) for index, value in enumerate(extended_numeric))

    for case_id, value in cases:
        check_case(case_id, value, canonical, generated)

    invalid_inputs = [["x"], [None], [1, object()]]
    for index, invalid in enumerate(invalid_inputs):
        canonical_exc = exception_kind(canonical, list(invalid))
        generated_exc = exception_kind(generated, list(invalid))
        assert canonical_exc is generated_exc is TypeError, (
            f"exception mismatch invalid-{index}: {canonical_exc} != {generated_exc}"
        )

    print(f"documented_cases={len(documented)}")
    print(f"boundary_cases={len(boundaries)}")
    print(f"exhaustive_integer_cases={exhaustive_count}")
    print(f"generated_integer_cases={generated_count} seed={SEED} max_length=64")
    print(f"extended_numeric_cases={len(extended_numeric)}")
    print(f"invalid_exception_parity_cases={len(invalid_inputs)}")
    print(f"total_value_cases={len(cases)}")
    print("mismatches=0")
    print("STAGE2_DIFFERENTIAL_OK")


if __name__ == "__main__":
    main()
