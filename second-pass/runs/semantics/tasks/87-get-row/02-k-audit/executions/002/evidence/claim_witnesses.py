#!/usr/bin/env python3
"""Ground witnesses for both submitted entry-claim preconditions."""

from __future__ import annotations

import importlib.util


def load(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.get_row


canonical = load("/reference/canonical.py", "canonical_witness")
generated = load("/candidate/solution.py", "candidate_witness")


def add_match(value: int, target: int, row: int, column: int, rest):
    return [(row, column), *rest] if value == target else rest


empty_lst: list[list[int]] = []
empty_x = 7
empty_claim_expected = []

a, b, c, d, x = 5, 5, 6, 5, 5
shape_lst = [[], [a], [b, c, d]]
shape_claim_expected = add_match(
    a,
    x,
    1,
    0,
    add_match(d, x, 2, 2, add_match(c, x, 2, 1, add_match(b, x, 2, 0, []))),
)

for label, lst, target, claimed in (
    ("empty", empty_lst, empty_x, empty_claim_expected),
    ("shape-0-1-3", shape_lst, x, shape_claim_expected),
):
    canonical_result = canonical(lst, target)
    generated_result = generated(lst, target)
    print(
        f"{label}: input={lst!r} x={target} "
        f"claimed={claimed!r} canonical={canonical_result!r} generated={generated_result!r}"
    )
    assert claimed == canonical_result == generated_result

print("claim_witness_mismatches=0")
