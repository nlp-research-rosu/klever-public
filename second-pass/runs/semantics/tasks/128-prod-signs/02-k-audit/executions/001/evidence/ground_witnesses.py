#!/usr/bin/env python3
"""Instantiate both entry claims with satisfying integer-list witnesses."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.prod_signs


def magnitude_sum(values: list[int]) -> int:
    return sum(abs(value) for value in values)


def sign_product(values: list[int]) -> int:
    sign = 1
    for value in values:
        if value < 0:
            sign = -sign
        elif value == 0:
            sign = 0
    return sign


def main() -> int:
    canonical = load_entry(Path("/reference/canonical.py"), "ground_canonical")
    generated = load_entry(
        Path("/tmp/audit-work/128-prod-signs.HMXf22/solution.py"),
        "ground_generated",
    )
    witnesses = []
    for label, values in [
        ("empty-entry", []),
        ("nonempty-negative-result", [1, 2, 2, -4]),
        ("nonempty-zero-result", [0, 1]),
        ("nonempty-positive-result", [-2, -3]),
        ("nonempty-off-by-one-mutation-witness", [1]),
    ]:
        formal_result = (
            None
            if not values
            else magnitude_sum(values) * sign_product(values)
        )
        witnesses.append(
            {
                "label": label,
                "input": values,
                "formal_precondition": (
                    "empty entry has no requires clause"
                    if not values
                    else "first element has sort Int and allInts(tail) = true"
                ),
                "magnitudeSum": None if not values else magnitude_sum(values),
                "signProduct": None if not values else sign_product(values),
                "claimed_result": formal_result,
                "canonical_result": canonical(list(values)),
                "generated_result": generated(list(values)),
            }
        )

    ok = all(
        row["claimed_result"]
        == row["canonical_result"]
        == row["generated_result"]
        for row in witnesses
    )
    print(json.dumps({"all_equal": ok, "witnesses": witnesses}, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
