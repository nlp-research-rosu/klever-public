#!/usr/bin/env python3
"""Independent differential test for HumanEval/34.

Oracle: the trusted /reference/canonical.py entry point.
Subject: the generated /candidate/solution.py entry point.

The primary intended-domain campaign uses integer lists.  Additional compatible
Python values probe the prompt's unparameterized ``list`` annotation, and a
separate diagnostic checks unhashable values that the canonical implementation
rejects.
"""

from __future__ import annotations

import copy
import importlib.util
import itertools
import math
import random
from pathlib import Path
from typing import Any, Callable


def load_unique(path: str, module_name: str) -> Callable[[list], list]:
    spec = importlib.util.spec_from_file_location(module_name, Path(path))
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.unique


def normalize_value(value: Any) -> Any:
    if isinstance(value, float) and math.isnan(value):
        return ("nan",)
    if isinstance(value, list):
        return ("list", tuple(normalize_value(item) for item in value))
    if isinstance(value, tuple):
        return ("tuple", tuple(normalize_value(item) for item in value))
    return (type(value).__name__, value)


def outcome(function: Callable[[list], list], value: list) -> tuple:
    try:
        return ("return", normalize_value(function(copy.deepcopy(value))))
    except Exception as error:  # Compare observable exception classes.
        return ("raise", type(error).__name__)


def main() -> int:
    canonical = load_unique("/reference/canonical.py", "trusted_canonical_34")
    candidate = load_unique("/candidate/solution.py", "candidate_solution_34")
    cases: list[tuple[str, list]] = []

    cases.extend(
        [
            ("documented", [5, 3, 5, 2, 3, 3, 9, 0, 123]),
            ("empty", []),
            ("singleton", [1]),
            ("all-duplicate", [4, 4, 4]),
            ("all-distinct-sorted", [-3, -1, 0, 2, 8]),
            ("all-distinct-reverse", [8, 2, 0, -1, -3]),
            ("branch-alternation", [2, 1, 2, 3, 1, 4, 4]),
            ("integer-extremes", [-(10**100), 10**100, 0, -(10**100)]),
        ]
    )

    alphabet = (-2, -1, 0, 1, 2)
    for length in range(7):
        for values in itertools.product(alphabet, repeat=length):
            cases.append((f"exhaustive-int-length-{length}", list(values)))

    rng = random.Random(340034)
    for _ in range(1000):
        length = rng.randrange(0, 41)
        values = [rng.randrange(-10**9, 10**9 + 1) for _ in range(length)]
        cases.append(("seeded-random-int", values))

    cases.extend(
        [
            ("bool-int-equality", [True, 1, False, 0, 2]),
            ("finite-floats", [3.5, -0.0, 0.0, 2.25, 3.5]),
            ("strings", ["b", "a", "b", "", "aa"]),
            ("tuples", [(1, 2), (0,), (1, 2), ()]),
        ]
    )

    mismatches: list[tuple[str, list, tuple, tuple]] = []
    labels: dict[str, int] = {}
    for label, value in cases:
        labels[label] = labels.get(label, 0) + 1
        expected = outcome(canonical, value)
        actual = outcome(candidate, value)
        if actual != expected:
            mismatches.append((label, value, expected, actual))

    print(f"PRIMARY_CASES={len(cases)}")
    print(f"PRIMARY_LABEL_COUNTS={labels}")
    print(f"PRIMARY_MISMATCHES={len(mismatches)}")
    for mismatch in mismatches[:20]:
        print(f"MISMATCH={mismatch!r}")

    # This is reported separately because list elements are unhashable and the
    # trusted canonical implementation therefore defines an exceptional path.
    extended = [
        [[1], [1], [0]],
        [[], []],
    ]
    print(f"UNHASHABLE_DIAGNOSTICS={len(extended)}")
    for value in extended:
        print(
            "UNHASHABLE "
            f"input={value!r} "
            f"canonical={outcome(canonical, value)!r} "
            f"candidate={outcome(candidate, value)!r}"
        )
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
