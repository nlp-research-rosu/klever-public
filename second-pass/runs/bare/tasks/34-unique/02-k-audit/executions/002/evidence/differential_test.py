#!/usr/bin/env python3
"""Independent differential test for trusted canonical.py and solution.py."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import random
from typing import Any, Callable


def load_entry(path: Path, module_name: str) -> Callable[[list[Any]], list[Any]]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.unique


def outcome(function: Callable[[list[Any]], list[Any]], value: list[Any]) -> tuple:
    try:
        return ("return", function(list(value)))
    except Exception as error:
        return ("raise", type(error).__name__, str(error))


def main() -> None:
    canonical = load_entry(
        Path("/tmp/audit-work/trusted/canonical.py"), "trusted_canonical"
    )
    candidate = load_entry(
        Path("/tmp/audit-work/candidate/solution.py"), "generated_solution"
    )

    named_cases: list[tuple[str, list[Any]]] = [
        ("documented-example", [5, 3, 5, 2, 3, 3, 9, 0, 123]),
        ("empty", []),
        ("singleton", [7]),
        ("all-equal", [4, 4, 4, 4]),
        ("equality-boundaries", [2, 1, 2, 1, 0, 0]),
        ("ordering-boundaries", [1, 0, -1, 2, -2]),
        ("already-sorted", [-3, -1, 0, 2, 8]),
        ("reverse-sorted", [8, 2, 0, -1, -3]),
        ("extreme-integers", [10**100, -(10**100), 0, 10**100]),
        ("strings", ["pear", "apple", "pear", "banana"]),
        ("tuples", [(2, 0), (1, 9), (2, 0), (1, 2)]),
        ("floats", [2.5, -1.25, 2.5, 0.0]),
        ("booleans", [True, False, True]),
        ("mixed-bool-int", [True, 2, False, 1, 0]),
        ("unhashable-element", [[1], [1]]),
        ("incomparable-elements", [1, "1"]),
    ]

    generator = random.Random(340034)
    generated_cases: list[tuple[str, list[int]]] = []
    for index in range(250):
        length = generator.randrange(0, 65)
        values = [generator.randrange(-40, 41) for _ in range(length)]
        generated_cases.append((f"generated-int-{index:03d}", values))

    cases = named_cases + generated_cases
    mismatches = 0
    return_cases = 0
    exception_cases = 0
    for name, value in cases:
        expected = outcome(canonical, value)
        actual = outcome(candidate, value)
        if expected[0] == "return":
            return_cases += 1
        else:
            exception_cases += 1
        if expected != actual:
            mismatches += 1
            print(
                f"MISMATCH name={name} input={value!r} "
                f"canonical={expected!r} candidate={actual!r}"
            )
        elif name in {case_name for case_name, _ in named_cases}:
            print(
                f"MATCH name={name} input={value!r} outcome={actual!r}"
            )

    print("RANDOM_SEED 340034")
    print("GENERATED_INTEGER_CASES 250")
    print(f"TOTAL_CASES {len(cases)}")
    print(f"RETURN_CASES {return_cases}")
    print(f"EXCEPTION_CASES {exception_cases}")
    print(f"MISMATCHES {mismatches}")
    if mismatches:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
