#!/usr/bin/env python3
"""Ground witnesses for every candidate entry claim."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.choose_num


def py_mod(value: int, divisor: int) -> int:
    return ((value % divisor) + divisor) % divisor


def largest_even_in_range(x: int, y: int) -> int:
    candidate = y - py_mod(y, 2)
    return candidate if x <= candidate else -1


scratch = Path("/tmp/audit-work/102-choose-num")
canonical = load_entry(scratch / "trusted" / "canonical.py", "witness_canonical")
generated = load_entry(scratch / "solution.py", "witness_generated")

witnesses = [
    ("all-positive-inputs", 12, 15, lambda x, y: largest_even_in_range(x, y)),
    ("even-upper-in-range", 12, 14, lambda _x, y: y),
    ("even-upper-before-range", 15, 14, lambda _x, _y: -1),
    ("odd-upper-predecessor-in-range", 14, 15, lambda _x, y: y - 1),
    ("odd-upper-no-even-in-range", 15, 15, lambda _x, _y: -1),
]

print("shared initial K state: env=0; scopes={0: empty parent(-1), -1: builtins};")
print("scopeLoc=1; heap=empty; heapLoc=0; stack=empty; ret=noRet; exc=NoExc; exit-code=0")
failures = 0
for label, x, y, claimed_result in witnesses:
    pre_positive = x > 0 and y > 0
    result = claimed_result(x, y)
    canonical_result = canonical(x, y)
    generated_result = generated(x, y)
    ok = pre_positive and result == canonical_result == generated_result
    failures += not ok
    print(
        f"{label}: X={x} Y={y} positive={pre_positive} "
        f"pyMod(Y,2)={py_mod(y, 2)} claimed={result} "
        f"canonical={canonical_result} generated={generated_result} ok={ok}"
    )

print(f"witness_failures={failures}")
raise SystemExit(1 if failures else 0)
