#!/usr/bin/env python3
"""Compare concrete formal-summary witnesses with both Python functions."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load(Path("/reference/canonical.py"), "trusted_canonical_ground")
generated = load(
    Path("/tmp/audit-work/128-prod-signs/solution.py"),
    "candidate_generated_ground",
)

witnesses = [
    ([], None),
    ([1, 2, 2, -4], -9),
    ([0, 1], 0),
    ([-1, -2, -3], -6),
    (
        [
            10_000_000_000_000_000_000_000_000_000_000_000_000_000,
            -10_000_000_000_000_000_000_000_000_000_000_000_000_000,
            1,
        ],
        -20_000_000_000_000_000_000_000_000_000_000_000_000_001,
    ),
]

for values, formal_result in witnesses:
    canonical_result = canonical.prod_signs(values)
    generated_result = generated.prod_signs(values)
    print(
        f"INPUT={values!r} FORMAL={formal_result!r} "
        f"CANONICAL={canonical_result!r} GENERATED={generated_result!r}"
    )
    assert formal_result == canonical_result == generated_result

print(f"GROUND_WITNESSES={len(witnesses)} MISMATCHES=0")
