#!/usr/bin/env python3
"""Concrete satisfying witnesses for all eleven submitted entry claims."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load_entry(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.get_row


canonical = load_entry(Path("/reference/canonical.py"), "witness_canonical")
candidate = load_entry(
    Path("/tmp/audit-work/87-get-row/source/solution.py"), "witness_candidate"
)

examples = [
    (
        "example-prompt",
        [
            [1, 2, 3, 4, 5, 6],
            [1, 2, 3, 4, 1, 6],
            [1, 2, 3, 4, 5, 1],
        ],
        1,
        [(0, 0), (1, 4), (1, 0), (2, 5), (2, 0)],
    ),
    ("example-empty", [], 1, []),
    ("example-third", [[], [1], [1, 2, 3]], 3, [(2, 2)]),
]

failures = []

for name, matrix, x, claimed in examples:
    c_result = canonical(matrix, x)
    s_result = candidate(matrix, x)
    ok = c_result == claimed == s_result
    print(
        f"{name}: precondition=true exact_input={matrix!r}, x={x}; "
        f"claimed={claimed!r}; canonical={c_result!r}; candidate={s_result!r}; "
        f"ok={int(ok)}"
    )
    if not ok:
        failures.append(name)

for bits in range(8):
    ah = bool(bits & 4)
    bh = bool(bits & 2)
    ch = bool(bits & 1)
    x = 0
    a = x if ah else 11
    b = x if bh else 12
    c = x if ch else 13
    matrix = [[a, b], [c]]
    claimed = []
    if bh:
        claimed.append((0, 1))
    if ah:
        claimed.append((0, 0))
    if ch:
        claimed.append((1, 0))
    conditions = (
        (a == x) == ah and (b == x) == bh and (c == x) == ch
    )
    c_result = canonical(matrix, x)
    s_result = candidate(matrix, x)
    name = f"symbolic-{bits:03b}"
    ok = conditions and c_result == claimed == s_result
    print(
        f"{name}: precondition={int(conditions)} witness A={a},B={b},C={c},X={x}; "
        f"claimed={claimed!r}; canonical={c_result!r}; candidate={s_result!r}; "
        f"ok={int(ok)}"
    )
    if not ok:
        failures.append(name)

print("witness_count=11")
print(f"failure_count={len(failures)}")
if failures:
    print("failures=" + ",".join(failures))
    raise SystemExit(1)
