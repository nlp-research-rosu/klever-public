#!/usr/bin/env python3
"""Compare ground instances of the claimed summary with both Python programs."""

from __future__ import annotations

import importlib.util
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/fib-audit")


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def fib_from(a: int, b: int, n: int) -> int:
    while n > 0:
        a, b, n = b, a + b, n - 1
    return a


canonical = load_module("trusted_canonical_substitution", SCRATCH / "canonical.py")
candidate = load_module("generated_solution_substitution", SCRATCH / "solution.py")
for n in (0, 1, 2, 8, 10):
    claimed = fib_from(0, 1, n)
    trusted = canonical.fib(n)
    generated = candidate.fib(n)
    assert claimed == trusted == generated
    print(
        f"N={n} satisfies N>=0: "
        f"fibFrom(0,1,N)={claimed} canonical={trusted} candidate={generated}"
    )
