#!/usr/bin/env python3
"""Differentially compare the trusted and candidate Python entry points."""

from __future__ import annotations

import importlib.util
import random
from pathlib import Path
from typing import Any, Callable


def load_entry(path: Path, module_name: str) -> Callable[[list[Any]], list[int]]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.filter_integers


class IntSubclass(int):
    pass


class NonInt:
    def __repr__(self) -> str:
        return "NonInt()"


def main() -> None:
    canonical = load_entry(
        Path("/tmp/audit-work/reference/canonical.py"), "trusted_canonical"
    )
    candidate = load_entry(
        Path("/tmp/audit-work/candidate-src/solution.py"), "candidate_solution"
    )

    documented_and_boundary_cases: list[list[Any]] = [
        ["a", 3.14, 5],
        [1, 2, 3, "abc", {}, []],
        [],
        [0],
        [-1],
        [True, False],
        [0.0, -0.0, float("inf"), float("-inf"), float("nan")],
        [-(2**200), 2**200],
        [IntSubclass(-7), IntSubclass(0), IntSubclass(11)],
        [None, "", b"", (), set(), {}, [], complex(2, 3), NonInt()],
        [1, "x", 1, True, 2.0, IntSubclass(3), False, -4],
    ]

    pool: list[Any] = [
        None,
        False,
        True,
        -10**40,
        -2,
        -1,
        0,
        1,
        2,
        10**40,
        IntSubclass(-3),
        IntSubclass(8),
        -2.5,
        0.0,
        4.5,
        "",
        "abc",
        b"bytes",
        (),
        (1,),
        [],
        [1],
        {},
        {"x": 1},
        set(),
        {1},
        complex(0, 1),
        NonInt(),
    ]
    rng = random.Random(2200260726)
    generated_cases = [
        [rng.choice(pool) for _ in range(rng.randrange(0, 31))]
        for _ in range(1000)
    ]
    cases = documented_and_boundary_cases + generated_cases

    mismatches: list[tuple[int, list[Any], list[int], list[int]]] = []
    for index, values in enumerate(cases):
        expected = canonical(values)
        actual = candidate(values)
        if actual != expected:
            mismatches.append((index, values, expected, actual))
        # Both implementations must be stable and return original objects.
        oracle = [value for value in values if isinstance(value, int)]
        if expected != oracle or actual != oracle:
            mismatches.append((index, values, oracle, actual))

    print(
        "DIFFERENTIAL_SCOPE "
        f"documented_boundary={len(documented_and_boundary_cases)} "
        f"seed=2200260726 generated={len(generated_cases)} "
        f"total={len(cases)}"
    )
    print(
        "BRANCH_WITNESSES "
        f"exact_int={candidate([5])!r} "
        f"bool={candidate([True, False])!r} "
        f"int_subclass={candidate([IntSubclass(9)])!r} "
        f"non_int={candidate(['x', 2.0, NonInt()])!r}"
    )
    print(f"MISMATCHES={len(mismatches)}")
    for mismatch in mismatches[:10]:
        print(f"MISMATCH={mismatch!r}")
    if mismatches:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
