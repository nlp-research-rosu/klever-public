#!/usr/bin/env python3
"""Independent differential test for HumanEval 22 and the submitted source."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path
from typing import Any, Callable


class IntSubclass(int):
    pass


def load_entry(path: Path, module_name: str) -> Callable[[list[Any]], list[int]]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.filter_integers


def identical_selection(left: list[Any], right: list[Any]) -> bool:
    return len(left) == len(right) and all(a is b for a, b in zip(left, right))


def show(values: list[Any]) -> str:
    return "[" + ", ".join(f"{type(v).__name__}({v!r})" for v in values) + "]"


def main() -> int:
    canonical = load_entry(Path("/reference/canonical.py"), "trusted_canonical")
    generated = load_entry(Path("/candidate/solution.py"), "submitted_solution")

    named_cases: list[tuple[str, list[Any]]] = [
        ("prompt-one", ["a", 3.14, 5]),
        ("prompt-two", [1, 2, 3, "abc", {}, []]),
        ("empty", []),
        ("all-non-int", ["", 0.0, None, {}, [], ()]),
        ("all-int", [-1, 0, 1, 2**63, -(2**63)]),
        ("alternating", ["left", -1, 2.5, 0, None, 9, {}]),
        ("bool-boundary", [False, True, 0, 1]),
        ("int-subclass", [IntSubclass(7), 7.0, IntSubclass(-3)]),
        ("very-large", [10**200, -(10**200), float("inf"), float("nan")]),
        ("nested-values", [[1], {"x": 2}, (3,), {4}, 5]),
    ]

    mismatches = 0
    total = 0
    print("NAMED_CASES")
    for name, values in named_cases:
        expected = canonical(values)
        actual = generated(values)
        ok = identical_selection(expected, actual)
        total += 1
        mismatches += not ok
        print(
            f"{name}: match={ok} input={show(values)} "
            f"canonical={show(expected)} submitted={show(actual)}"
        )

    atoms: tuple[Any, ...] = (-1, 0, 1, False, True, 1.5, "", None, [], {})
    exhaustive_count = 0
    for length in range(5):
        for product in itertools.product(atoms, repeat=length):
            values = list(product)
            expected = canonical(values)
            actual = generated(values)
            ok = identical_selection(expected, actual)
            exhaustive_count += 1
            total += 1
            if not ok:
                mismatches += 1
                if mismatches <= 20:
                    print(
                        "EXHAUSTIVE_MISMATCH "
                        f"input={show(values)} canonical={show(expected)} "
                        f"submitted={show(actual)}"
                    )

    random_generator = random.Random(220726)
    random_atoms: tuple[Any, ...] = atoms + (
        2**63,
        -(2**63),
        IntSubclass(11),
        "abc",
        {"k": []},
    )
    random_count = 500
    for index in range(random_count):
        values = [
            random_generator.choice(random_atoms)
            for _ in range(random_generator.randrange(0, 21))
        ]
        expected = canonical(values)
        actual = generated(values)
        ok = identical_selection(expected, actual)
        total += 1
        if not ok:
            mismatches += 1
            if mismatches <= 20:
                print(
                    f"RANDOM_MISMATCH index={index} input={show(values)} "
                    f"canonical={show(expected)} submitted={show(actual)}"
                )

    print(
        f"SUMMARY named={len(named_cases)} exhaustive={exhaustive_count} "
        f"random_seed=220726 random={random_count} total={total} "
        f"mismatches={mismatches}"
    )
    return 0 if mismatches == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
