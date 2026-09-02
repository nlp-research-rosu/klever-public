#!/usr/bin/env python3
"""Independent canonical-versus-candidate differential for HumanEval 57."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path
from typing import Any, Callable


def load_entry(path: Path, module_name: str) -> Callable[[list[Any]], bool]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.monotonic


def outcome(function: Callable[[list[Any]], bool], values: list[Any]) -> tuple:
    try:
        return ("return", function(values.copy()))
    except Exception as error:  # Compare exception behavior as an observable.
        return ("raise", type(error).__name__, str(error))


def main() -> None:
    canonical = load_entry(Path("/reference/canonical.py"), "trusted_canonical")
    generated = load_entry(Path("/candidate/solution.py"), "candidate_solution")

    named_cases: list[tuple[str, list[Any]]] = [
        ("prompt-ascending", [1, 2, 4, 20]),
        ("prompt-neither", [1, 20, 4, 10]),
        ("prompt-descending", [4, 1, 0, -10]),
        ("empty", []),
        ("singleton", [7]),
        ("two-ascending", [1, 2]),
        ("two-descending", [2, 1]),
        ("all-equal", [3, 3, 3]),
        ("ascending-duplicates", [-2, -2, 0, 0, 4]),
        ("descending-duplicates", [4, 4, 0, -2, -2]),
        ("up-then-down-boundary", [0, 1, 0]),
        ("down-then-up-boundary", [1, 0, 1]),
        ("late-ascending-break", [0, 1, 2, 1]),
        ("late-descending-break", [3, 2, 1, 2]),
        ("large-integers", [-(10**100), 0, 10**100]),
        ("floats", [-3.5, -0.0, 2.25, 2.25]),
        ("strings", ["a", "aa", "b"]),
        ("tuples", [(0, 2), (1, 0), (1, 0)]),
        ("mixed-incomparable-exception", [0, "0"]),
    ]

    checked = 0
    mismatches: list[tuple[str, list[Any], tuple, tuple]] = []

    def check(label: str, values: list[Any]) -> None:
        nonlocal checked
        expected = outcome(canonical, values)
        actual = outcome(generated, values)
        checked += 1
        if expected != actual:
            mismatches.append((label, values, expected, actual))

    for label, values in named_cases:
        check(label, values)

    generated_exhaustive = 0
    for length in range(6):
        for values in itertools.product(range(-2, 3), repeat=length):
            check(f"exhaustive-{length}", list(values))
            generated_exhaustive += 1

    rng = random.Random(570057)
    generated_random = 0
    for index in range(2000):
        length = rng.randrange(0, 26)
        values = [rng.randrange(-10**6, 10**6 + 1) for _ in range(length)]
        check(f"random-{index}", values)
        generated_random += 1

    print(f"named_cases={len(named_cases)}")
    print(f"exhaustive_integer_lists={generated_exhaustive}")
    print(f"random_integer_lists={generated_random}")
    print(f"checked={checked} mismatches={len(mismatches)}")
    for mismatch in mismatches[:20]:
        print("MISMATCH", repr(mismatch))
    if mismatches:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
