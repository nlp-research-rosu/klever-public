#!/usr/bin/env python3
"""Ground witnesses for every entry-claim shape and its claimed addMatch value."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.get_row


canonical = load_entry("trusted_canonical_witness", Path("/reference/canonical.py"))
generated = load_entry(
    "scratch_generated_witness", Path("/tmp/audit-work/87-get-row/solution.py")
)


def add_match(value: int, target: int, row: int, column: int, rest):
    if value == target:
        return [(row, column), *rest]
    return rest


def claimed_ragged_value(a: int, b: int, c: int, d: int, x: int):
    return add_match(
        a,
        x,
        1,
        0,
        add_match(
            d,
            x,
            2,
            2,
            add_match(c, x, 2, 1, add_match(b, x, 2, 0, [])),
        ),
    )


cases = [
    ("empty_claim", [], 7, []),
    (
        "ragged_claim_mixed",
        [[], [5], [9, 5, 5]],
        5,
        claimed_ragged_value(5, 9, 5, 5, 5),
    ),
    (
        "ragged_claim_no_match",
        [[], [1], [2, 3, 4]],
        9,
        claimed_ragged_value(1, 2, 3, 4, 9),
    ),
    (
        "ragged_claim_all_match",
        [[], [6], [6, 6, 6]],
        6,
        claimed_ragged_value(6, 6, 6, 6, 6),
    ),
]

for label, matrix, target, claimed in cases:
    canonical_result = canonical(matrix, target)
    generated_result = generated(matrix, target)
    print(
        f"{label}: matrix={matrix!r} target={target} claimed={claimed!r} "
        f"canonical={canonical_result!r} generated={generated_result!r}"
    )
    if not (claimed == canonical_result == generated_result):
        raise AssertionError(label)

print(f"ground_witnesses={len(cases)}")
print("mismatches=0")
