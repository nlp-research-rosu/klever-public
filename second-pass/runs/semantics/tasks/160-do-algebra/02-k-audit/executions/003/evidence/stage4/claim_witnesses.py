#!/usr/bin/env python3
"""Ground satisfying witnesses for every submitted entry claim."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.do_algebra


canonical = load(Path("/reference/canonical.py"), "canonical_witness")
generated = load(Path("/tmp/audit-work/160-do-algebra/solution.py"), "generated_witness")

witnesses = [
    ("plus", ["+"], [4, 7], 4 + 7, "A=4, B=7; A,B >= 0"),
    ("minus", ["-"], [4, 7], 4 - 7, "A=4, B=7; A,B >= 0"),
    ("times", ["*"], [4, 7], 4 * 7, "A=4, B=7; A,B >= 0"),
    ("floor", ["//"], [20, 3], 20 // 3, "A=20 >= 0, B=3 > 0"),
    ("power", ["**"], [2, 5], 32, "ground claim"),
    ("minus-assoc", ["-", "-"], [20, 6, 2], (20 - 6) - 2, "A=20,B=6,C=2 >= 0"),
    ("floor-assoc", ["//", "//"], [20, 3, 2], (20 // 3) // 2, "ground claim"),
    ("power-assoc", ["**", "**"], [2, 3, 2], 2 ** (3**2), "ground claim"),
    (
        "prompt-precedence",
        ["+", "*", "-"],
        [2, 3, 4, 5],
        (2 + (3 * 4)) - 5,
        "A=2,B=3,C=4,D=5 >= 0",
    ),
    (
        "mixed-precedence",
        ["+", "*", "**", "//", "-"],
        [4, 3, 2, 3, 5, 1],
        (4 + ((3 * (2**3)) // 5)) - 1,
        "A=4,B=3,F=1 >= 0, E=5 > 0",
    ),
]

failures = 0
for label, operators, operands, expected, precondition in witnesses:
    canonical_result = canonical(list(operators), list(operands))
    generated_result = generated(list(operators), list(operands))
    ok = canonical_result == generated_result == expected
    print(
        f"{label}: precondition=({precondition}); operators={operators}; operands={operands}; "
        f"formal_expected={expected}; canonical={canonical_result}; generated={generated_result}; "
        f"status={'OK' if ok else 'MISMATCH'}"
    )
    failures += not ok

print(f"witness_count={len(witnesses)} mismatch_count={failures}")
raise SystemExit(1 if failures else 0)
