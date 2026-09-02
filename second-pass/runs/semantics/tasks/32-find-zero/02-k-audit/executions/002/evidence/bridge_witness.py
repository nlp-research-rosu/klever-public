#!/usr/bin/env python3
"""Concrete and opposite-interpretation witnesses for proof-local bridges."""

from __future__ import annotations

import importlib.util
from pathlib import Path


SOLUTION = Path("/tmp/audit-work/candidate/solution.py")


def load_solution():
    spec = importlib.util.spec_from_file_location("candidate_bridge_witness", SOLUTION)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def concrete_phases(module, xs: list[int | float]):
    begin: int | float = -1
    end: int | float = 1
    bracket_iterations = 0
    while module.poly(xs, begin) * module.poly(xs, end) > 0:
        begin *= 2
        end *= 2
        bracket_iterations += 1
    bracket = (begin, end)
    bisect_iterations = 0
    while end - begin > 1e-10:
        center = (begin + end) / 2
        if module.poly(xs, center) * module.poly(xs, begin) > 0:
            begin = center
        else:
            end = center
        bisect_iterations += 1
    return bracket, begin, bracket_iterations, bisect_iterations


def main() -> int:
    module = load_solution()
    for xs in ([1, 2], [-6, 11, -6, 1], [3, 2]):
        bracket, result, bracket_count, bisect_count = concrete_phases(module, xs)
        print(
            f"xs={xs} source_contract_valid=True "
            f"fixed_bracket={bracket} bracket_iterations={bracket_count} "
            f"fixed_result={result!r} bisect_iterations={bisect_count} "
            f"poly(result)={module.poly(xs, result)!r}"
        )
        print(
            "  bridge result terms: "
            f"bracketLow({xs}), bracketHigh({xs}), "
            f"bisectLow({xs}, bracketLow(...), bracketHigh(...))"
        )

    xs = [1, 2]
    opposite_result = 0
    print("\nOpposite ground interpretation admitted by the proof extensions:")
    print("  interpret bracketLow([1,2]) = -1 and bracketHigh([1,2]) = 1")
    print("  interpret bisectLow([1,2], -1, 1) = 0")
    print(
        "  verification.k still rewrites approximatesZero(..., bisectLow(...)) "
        "to true solely by constructor shape"
    )
    print(
        f"  but poly([1,2], 0) = {module.poly(xs, opposite_result)!r}, "
        "so 0 is not a zero and differs from the fixed result"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
