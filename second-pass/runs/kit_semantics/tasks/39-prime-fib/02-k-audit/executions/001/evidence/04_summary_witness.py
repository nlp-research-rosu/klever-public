#!/usr/bin/env python3
"""Ground witnesses for the mathematical reading of the two K summaries."""

from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path("/tmp/audit-work/39-prime-fib-audit")


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def prime_scan(a: int, divisor: int, flag: bool) -> bool:
    while divisor * divisor <= a:
        if a % divisor == 0:
            flag = False
        divisor += 1
    return flag


def prime_fib_search(n: int, count: int, a: int, b: int) -> int:
    states = [(count, a, b)]
    while count < n:
        bit = prime_scan(b, 2, b >= 2)
        count, a, b = count + int(bit), b, a + b
        states.append((count, a, b))
    return a, states


canonical = load("trusted_canonical_witness", ROOT / "trusted_canonical.py")
generated = load("generated_witness", ROOT / "solution.py")

print("inner witness A=8,D=2,P=true:", prime_scan(8, 2, True))
assert prime_scan(8, 2, True) is False

for n in (1, 5):
    summary, states = prime_fib_search(n, 0, 0, 1)
    canonical_value = canonical.prime_fib(n)
    generated_value = generated.prime_fib(n)
    print(
        f"N={n}: summary={summary}, canonical={canonical_value}, "
        f"generated={generated_value}, transitions={len(states) - 1}"
    )
    assert summary == canonical_value == generated_value

print("outer/entry satisfying witness: N=5,C=0,A=0,B=1 -> 89")
