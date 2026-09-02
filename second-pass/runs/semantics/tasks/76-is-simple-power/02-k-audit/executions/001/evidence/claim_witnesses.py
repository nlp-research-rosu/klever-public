#!/usr/bin/env python3
"""Ground witnesses for every claim precondition.

`formal_summary` is a direct executable reading of verification.k lines 11–23.
It is used only to instantiate the claimed right-hand side, not as an oracle for
the program.  The trusted canonical and generated implementations are imported
independently.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/76-is-simple-power")


def load_function(module_name: str, source: Path):
    spec = importlib.util.spec_from_file_location(module_name, source)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {source}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_simple_power


canonical = load_function("witness_canonical", SCRATCH / "trusted/canonical.py")
generated = load_function(
    "witness_generated", SCRATCH / "candidate-source/solution.py"
)


def positive_power_loop(x: int, n: int) -> bool:
    assert n > 1
    while x % n == 0:
        x //= n
    return x == 1


def formal_summary(x: int, n: int) -> bool:
    if x == 1:
        return True
    if x < 1:
        return False
    if n <= 1:
        return False
    return positive_power_loop(x, n)


entry_witnesses = [
    ("function-one", 1, 4, "X fixed to 1; N unrestricted"),
    ("function-below-one", 0, 2, "X < 1"),
    (
        "function-degenerate-base",
        4,
        -2,
        "X > 1 and N <= 1; also exposes the negative-base intent boundary",
    ),
    ("function-positive-domain", 8, 2, "X > 1 and N > 1"),
]

for label, x, n, reason in entry_witnesses:
    print(
        f"{label}: witness=(x={x},n={n}); precondition={reason}; "
        f"claimed={formal_summary(x,n)}; generated={generated(x,n)}; "
        f"canonical={canonical(x,n)}"
    )

loop_x, loop_n = 8, 2
print(
    "loop-correct: witness current scope={x:8,n:2}, N>1, "
    "BASE=.Map, parent=0, stack=[frame(.K,0,1)]; "
    f"claimed={positive_power_loop(loop_x,loop_n)}; "
    f"generated_entry={generated(loop_x,loop_n)}; "
    f"canonical_entry={canonical(loop_x,loop_n)}"
)
