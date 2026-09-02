#!/usr/bin/env python3
"""Independent differential test of trusted canonical.py and submitted solution.py."""

from __future__ import annotations

import importlib.util
import math
import pathlib
import random
from typing import Any


CANONICAL_PATH = pathlib.Path("/reference/canonical.py")
GENERATED_PATH = pathlib.Path("/tmp/audit-work/45-triangle-area/solution.py")


def load_function(path: pathlib.Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.triangle_area


def outcome(function, a: Any, h: Any) -> tuple[str, Any]:
    try:
        return ("value", function(a, h))
    except Exception as error:  # The exception type is observable behavior here.
        return ("exception", type(error).__name__)


def equivalent(left: tuple[str, Any], right: tuple[str, Any]) -> bool:
    if left[0] != right[0]:
        return False
    if left[0] == "exception":
        return left == right
    a, b = left[1], right[1]
    if type(a) is not type(b):
        return False
    if isinstance(a, float):
        if math.isnan(a) and math.isnan(b):
            return True
        return a == b
    return a == b


def main() -> None:
    canonical = load_function(CANONICAL_PATH, "trusted_canonical")
    generated = load_function(GENERATED_PATH, "submitted_solution")

    documented_and_boundaries: list[tuple[Any, Any]] = [
        (5, 3),  # documented example
        (0, 0),  # zero/empty magnitude
        (0, 99),
        (99, 0),
        (1, 1),
        (-1, 1),
        (1, -1),
        (-1, -1),
        (2, 1),
        (1, 2),
        (2**53 - 1, 1),
        (2**53, 1),
        (2**53 + 1, 1),
        (10**308, 1),
        (10**309, 1),  # both implementations reach the same overflow boundary
        (0.0, 0.0),
        (-0.0, 1.0),
        (5.5, 3.25),
        (1e-300, 1e300),
        (1e308, 1e308),
    ]

    exhaustive_integers = [(a, h) for a in range(-25, 26) for h in range(-25, 26)]
    randomizer = random.Random(450045)
    generated_integers = [
        (randomizer.randint(-(10**100), 10**100), randomizer.randint(-10**6, 10**6))
        for _ in range(500)
    ]
    generated_floats = [
        (randomizer.uniform(-1e150, 1e150), randomizer.uniform(-1e150, 1e150))
        for _ in range(500)
    ]
    cases = (
        documented_and_boundaries
        + exhaustive_integers
        + generated_integers
        + generated_floats
    )

    mismatches: list[tuple[Any, Any, tuple[str, Any], tuple[str, Any]]] = []
    for a, h in cases:
        canonical_result = outcome(canonical, a, h)
        generated_result = outcome(generated, a, h)
        if not equivalent(canonical_result, generated_result):
            mismatches.append((a, h, canonical_result, generated_result))

    print(f"oracle={CANONICAL_PATH}")
    print(f"generated={GENERATED_PATH}")
    print(
        "scope="
        f"{len(documented_and_boundaries)} documented/boundary + "
        f"{len(exhaustive_integers)} exhaustive integer + "
        f"{len(generated_integers)} seeded integer + "
        f"{len(generated_floats)} seeded float"
    )
    print(f"total_cases={len(cases)}")
    print(f"mismatches={len(mismatches)}")
    for mismatch in mismatches[:20]:
        print(f"MISMATCH {mismatch!r}")

    if mismatches:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
