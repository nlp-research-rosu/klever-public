#!/usr/bin/env python3
"""Ground the formal fibFrom result and compare both Python implementations."""

from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path("/tmp/audit-work/rebuild")


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.fibfib


def formal_fib_from(a: int, b: int, c: int, n: int) -> int:
    # Direct evaluator for verification.k:9-13.
    while n > 0:
        a, b, c, n = b, c, a + b + c, n - 1
    return a


canonical = load("canonical_for_substitution", ROOT / "canonical.py")
generated = load("generated_for_substitution", ROOT / "solution.py")
witnesses = [0, 1, 2, 3, 5, 8, 12, 20, 25]
print(f"satisfying_entry_inputs={witnesses} (each satisfies N >= 0)")
for n in witnesses:
    claimed = formal_fib_from(0, 0, 1, n)
    trusted = canonical(n)
    submitted = generated(n)
    equal = claimed == trusted == submitted
    print(
        f"N={n} claimed_fibFrom={claimed} canonical={trusted} "
        f"generated={submitted} all_equal={equal}"
    )
    if not equal:
        raise SystemExit(1)

print(
    "loop_precondition_witness="
    "L=1,A=0,B=0,C=1,D=0,I=0,N=5,P=parent(0); 0<=I<=N"
)
