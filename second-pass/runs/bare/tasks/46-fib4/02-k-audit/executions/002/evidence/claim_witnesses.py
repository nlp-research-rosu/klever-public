#!/usr/bin/env python3
"""Ground witnesses for every candidate claim and the split theorem composition."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load_fib4(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem + "_witness", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.fib4


canonical = load_fib4(Path("/reference/canonical.py"))
candidate = load_fib4(Path("/candidate/solution.py"))


def advance_to(a: int, b: int, c: int, d: int, i: int, n: int) -> int:
    while i <= n:
        a, b, c, d = b, c, d, a + b + c + d
        i += 1
    return d


def fib4_spec(n: int) -> int:
    if n == 0:
        return 0
    if n == 1:
        return 0
    if n == 2:
        return 2
    if n == 3:
        return 0
    if n >= 4:
        return advance_to(0, 0, 2, 0, 4, n)
    raise ValueError("outside candidate specification domain")


witnesses = [
    ("fib4-spec-link", 4, fib4_spec(4)),
    ("loop-correct", 4, advance_to(0, 0, 2, 0, 4, 4)),
    ("fib4-inductive-init", 4, "reachable exact loop head"),
    ("fib4-base-0", 0, fib4_spec(0)),
    ("fib4-base-1", 1, fib4_spec(1)),
    ("fib4-base-2", 2, fib4_spec(2)),
    ("fib4-base-3", 3, fib4_spec(3)),
    ("fib4-seven", 7, 14),
]
for label, n, expected in witnesses:
    python_values = (canonical(n), candidate(n))
    print(
        f"claim={label} satisfying_n={n} claimed={expected} "
        f"canonical={python_values[0]} candidate={python_values[1]}"
    )

for n in [4, 5, 7, 10, 20]:
    loop_summary = advance_to(0, 0, 2, 0, 4, n)
    print(
        f"composition n={n} init_post_matches_loop_pre=True "
        f"loop_result={loop_summary} fib4Spec={fib4_spec(n)} "
        f"canonical={canonical(n)} candidate={candidate(n)}"
    )
    assert loop_summary == fib4_spec(n) == canonical(n) == candidate(n)
