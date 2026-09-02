#!/usr/bin/env python3
"""Independent candidate-versus-trusted-canonical differential test."""

from __future__ import annotations

import importlib.util
import math
import random
from pathlib import Path
from typing import Any


def load_module(name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CANONICAL = load_module("trusted_canonical", Path("/reference/canonical.py"))
GENERATED = load_module("candidate_solution", Path("/candidate/solution.py"))


def profile(xs: list[int | float]) -> tuple[int, int, int]:
    """Count the algorithm's bracket, positive-product, and else branches."""
    begin: int | float = -1
    end: int | float = 1
    bracket_iterations = 0
    while CANONICAL.poly(xs, begin) * CANONICAL.poly(xs, end) > 0:
        begin *= 2
        end *= 2
        bracket_iterations += 1
        if bracket_iterations > 128:
            raise RuntimeError(f"unexpected nontermination while profiling {xs!r}")
    positive_product = 0
    else_branch = 0
    bisect_iterations = 0
    while end - begin > 1e-10:
        center = (begin + end) / 2
        if CANONICAL.poly(xs, center) * CANONICAL.poly(xs, begin) > 0:
            begin = center
            positive_product += 1
        else:
            end = center
            else_branch += 1
        bisect_iterations += 1
        if bisect_iterations > 256:
            raise RuntimeError(f"unexpected nontermination while profiling {xs!r}")
    return bracket_iterations, positive_product, else_branch


def outcome(function: Any, xs: list[int | float]) -> tuple[str, Any]:
    try:
        return ("value", function(list(xs)))
    except Exception as err:  # Boundary inputs may be outside the stated domain.
        return ("exception", (type(err).__name__, str(err)))


def main() -> None:
    fixed_cases: list[tuple[str, list[int | float]]] = [
        ("documented-linear", [1, 2]),
        ("documented-cubic", [-6, 11, -6, 1]),
        ("empty-outside-domain", []),
        ("minimum-linear-root-at-left-endpoint", [1, 1]),
        ("minimum-linear-root-at-right-endpoint", [-1, 1]),
        ("minimum-linear-bracket-expands-left", [3, 2]),
        ("minimum-linear-bracket-expands-right", [-3, 2]),
        ("constant-term-zero", [0, 5]),
        ("leading-zero-outside-domain-but-terminating", [1, 1, 0, 0]),
        ("float-coefficients", [0.125, -0.5]),
        ("cubic-repeated-root", [-1, 3, -3, 1]),
        ("six-coefficient-odd-degree", [2, -1, 3, 0, -2, 1]),
    ]

    rng = random.Random(320032)
    generated_cases: list[tuple[str, list[int]]] = []
    for index in range(72):
        length = (2, 4, 6)[index % 3]
        xs = [rng.randint(-4, 4) for _ in range(length)]
        while xs[-1] == 0:
            xs[-1] = rng.randint(-4, 4)
        generated_cases.append((f"generated-{index:02d}", xs))

    mismatches: list[tuple[str, list[int | float], Any, Any]] = []
    covered = {"bracket_zero": False, "bracket_positive": False,
               "bisect_positive": False, "bisect_else": False}
    max_abs_delta = 0.0

    all_cases = fixed_cases + generated_cases
    for label, xs in all_cases:
        expected = outcome(CANONICAL.find_zero, xs)
        actual = outcome(GENERATED.find_zero, xs)
        if expected != actual:
            mismatches.append((label, xs, expected, actual))
        if expected[0] == "value" and actual[0] == "value":
            max_abs_delta = max(max_abs_delta, abs(expected[1] - actual[1]))
        bracket, positive, otherwise = profile(xs)
        covered["bracket_zero"] |= bracket == 0
        covered["bracket_positive"] |= bracket > 0
        covered["bisect_positive"] |= positive > 0
        covered["bisect_else"] |= otherwise > 0
        if label in {
            "documented-linear",
            "documented-cubic",
            "empty-outside-domain",
            "minimum-linear-root-at-left-endpoint",
            "minimum-linear-root-at-right-endpoint",
            "minimum-linear-bracket-expands-left",
            "minimum-linear-bracket-expands-right",
            "constant-term-zero",
            "leading-zero-outside-domain-but-terminating",
            "float-coefficients",
            "cubic-repeated-root",
            "six-coefficient-odd-degree",
        }:
            residual = (
                abs(CANONICAL.poly(xs, actual[1]))
                if actual[0] == "value" and xs
                else None
            )
            print(
                f"{label}: xs={xs!r} canonical={expected!r} "
                f"generated={actual!r} branches={(bracket, positive, otherwise)!r} "
                f"candidate_abs_poly={residual!r}"
            )

    print(f"fixed_cases={len(fixed_cases)}")
    print(f"generated_valid_domain_cases={len(generated_cases)}")
    print(f"branch_boundary_coverage={covered!r}")
    print(f"max_abs_output_delta={max_abs_delta!r}")
    print(f"mismatch_count={len(mismatches)}")
    if mismatches:
        for item in mismatches:
            print(f"MISMATCH {item!r}")
        raise SystemExit(1)
    if not all(covered.values()):
        raise SystemExit(f"branch boundary not covered: {covered!r}")


if __name__ == "__main__":
    main()
