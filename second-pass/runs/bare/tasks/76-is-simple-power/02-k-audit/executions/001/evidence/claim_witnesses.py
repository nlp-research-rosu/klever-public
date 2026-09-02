#!/usr/bin/env python3
"""Ground witnesses for every positive claim's precondition/postcondition."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_simple_power


canonical = load("/tmp/audit-work/reference/canonical.py", "canonical_witness")
generated = load("/tmp/audit-work/source/solution.py", "generated_witness")


def power_ceiling(p: int, x: int, n: int) -> int:
    assert p > 0 and n >= 2
    while p < x:
        p *= n
    return p


def simple_power_spec(x: int, n: int) -> bool:
    return x == 1 or (
        x > 1 and n >= 2 and power_ceiling(n, x, n) == x
    )


rows = [
    # claim, x, n, formal result, generated result, canonical result, note
    (
        "emitted-tree-is-shared-tree",
        2,
        2,
        "term identity (no result postcondition)",
        generated(2, 2),
        canonical(2, 2),
        "unconditional configuration witness",
    ),
    (
        "returns-on-one",
        1,
        4,
        simple_power_spec(1, 4),
        generated(1, 4),
        canonical(1, 4),
        "X=1",
    ),
    (
        "rejects-below-one",
        0,
        2,
        simple_power_spec(0, 2),
        generated(0, 2),
        canonical(0, 2),
        "X<1",
    ),
    (
        "rejects-small-base",
        3,
        1,
        simple_power_spec(3, 1),
        generated(3, 1),
        canonical(3, 1),
        "1<X and N<2, positive-base boundary",
    ),
    (
        "rejects-small-base-negative-base",
        4,
        -2,
        simple_power_spec(4, -2),
        generated(4, -2),
        canonical(4, -2),
        "1<X and N<2; exposes prompt/canonical mismatch",
    ),
    (
        "active-path-enters-loop",
        8,
        2,
        "reaches power=N=2 with noResult",
        generated(8, 2),
        canonical(8, 2),
        "1<X and 2<=N",
    ),
    (
        "loop-correct-true",
        8,
        2,
        power_ceiling(2, 8, 2) == 8,
        generated(8, 2),
        canonical(8, 2),
        "X=8,N=2,P=N=2",
    ),
    (
        "loop-correct-false",
        5,
        3,
        power_ceiling(3, 5, 3) == 5,
        generated(5, 3),
        canonical(5, 3),
        "X=5,N=3,P=N=3",
    ),
]

print(
    "columns=(claim,x,n,formal_postcondition,generated_python,"
    "trusted_canonical,note)"
)
for row in rows:
    print(row)

assert rows[1][4] == rows[1][5] == rows[1][3]
assert rows[2][4] == rows[2][5] == rows[2][3]
assert rows[3][4] == rows[3][5] == rows[3][3]
assert rows[4][4] == rows[4][3] and rows[4][5] != rows[4][3]
assert rows[6][4] == rows[6][5] == rows[6][3]
assert rows[7][4] == rows[7][5] == rows[7][3]
print("assertions=PASS")
