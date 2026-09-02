#!/usr/bin/env python3
"""Differentially compare trusted canonical.py with the submitted solution.py."""

from __future__ import annotations

import importlib.util
import json
import math
import random
from pathlib import Path
from types import ModuleType
from typing import Any


ROOT = Path("/tmp/audit-work")
INPUTS = Path("/audit-output/evidence/differential_inputs.json")


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def outcome(function: Any, args: tuple[Any, Any]) -> tuple[str, Any, str]:
    try:
        value = function(*args)
    except Exception as error:  # noqa: BLE001 - exceptions are compared as outputs.
        return ("exception", type(error).__name__, str(error))
    return ("value", value, type(value).__name__)


def equal_outcomes(left: tuple[str, Any, str], right: tuple[str, Any, str]) -> bool:
    if left[0] != right[0] or left[2] != right[2]:
        return False
    if left[0] == "exception":
        return left[1] == right[1]
    if isinstance(left[1], float) and isinstance(right[1], float):
        if math.isnan(left[1]) and math.isnan(right[1]):
            return True
    return left[1] == right[1]


def main() -> None:
    canonical = load_module("trusted_canonical", ROOT / "canonical.py")
    candidate = load_module("submitted_solution", ROOT / "candidate" / "solution.py")
    inputs = json.loads(INPUTS.read_text())

    cases: list[tuple[str, tuple[Any, Any]]] = []
    for group in ("documented", "zero_and_boundary", "ordinary_float"):
        cases.extend((group, tuple(args)) for args in inputs[group])

    grid = inputs["generated_scope"]["integer_grid"]
    cases.extend(("integer_grid", (a, h)) for a in grid["a"] for h in grid["h"])

    random_scope = inputs["generated_scope"]
    integer_rng = random.Random(random_scope["random_integer_seed"])
    low, high = random_scope["random_integer_range_inclusive"]
    for _ in range(random_scope["random_integer_count"]):
        cases.append(
            (
                "random_integer",
                (integer_rng.randint(low, high), integer_rng.randint(low, high)),
            )
        )

    float_rng = random.Random(random_scope["random_float_seed"])
    low_float, high_float = random_scope["random_float_range"]
    for _ in range(random_scope["random_float_count"]):
        cases.append(
            (
                "random_float",
                (
                    float_rng.uniform(low_float, high_float),
                    float_rng.uniform(low_float, high_float),
                ),
            )
        )

    mismatches: list[tuple[str, tuple[Any, Any], Any, Any]] = []
    counts: dict[str, int] = {}
    for group, args in cases:
        counts[group] = counts.get(group, 0) + 1
        canonical_outcome = outcome(canonical.triangle_area, args)
        candidate_outcome = outcome(candidate.triangle_area, args)
        if not equal_outcomes(canonical_outcome, candidate_outcome):
            mismatches.append((group, args, canonical_outcome, candidate_outcome))

    print(f"oracle: {ROOT / 'canonical.py'}::triangle_area")
    print(f"candidate: {ROOT / 'candidate' / 'solution.py'}::triangle_area")
    print(f"input artifact: {INPUTS}")
    print(f"group counts: {json.dumps(counts, sort_keys=True)}")
    print(f"total cases: {len(cases)}")
    print(f"mismatch count: {len(mismatches)}")
    for mismatch in mismatches[:20]:
        print(f"MISMATCH {mismatch!r}")
    if mismatches:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
