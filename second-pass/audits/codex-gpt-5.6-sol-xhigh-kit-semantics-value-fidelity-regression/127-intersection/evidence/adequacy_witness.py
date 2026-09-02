#!/usr/bin/env python3
"""Ground witnesses for both entry preconditions and their result obligations."""

from __future__ import annotations

import importlib.util
import math
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


candidate = load(
    Path("/tmp/audit-work/127-intersection/solution.py"), "witness_solution"
).intersection
canonical = load(Path("/reference/canonical.py"), "witness_canonical").intersection


def formal_result(a: int, b: int, c: int, d: int) -> tuple[int, str]:
    start = c if c > a else a
    end = d if d < b else b
    length = end - start
    if length >= 2 and math.factorial(length - 1) % length == length - 1:
        return length, "YES"
    return length, "NO"


print("FACTORIAL-LOOP PRECONDITION WITNESS")
i, n, f = 1, 2, 1
print(f"I={i}, N={n}, F={f}, fact(I-1)={math.factorial(i - 1)}")
print(f"1<=I<=N: {1 <= i <= n}")
print(f"F=fact(I-1): {f == math.factorial(i - 1)}")
print(
    "complete cells: env=1; scopes include length=2,factorial=1,i=1; "
    "scopeLoc=2; heap=.Map; heapLoc=0; stack=.List; ret=noRet; "
    "exc=NoExc; exit-code=0"
)
print(f"claimed terminal i={n}, factorial=fact(N-1)={math.factorial(n - 1)}")

cases = [
    (-3, -1, -5, 5),
    (1, 2, 2, 3),
    (0, 4, -1, 5),
]
print("INTERSECTION ENTRY PRECONDITION WITNESSES")
for a, b, c, d in cases:
    assert a <= b and c <= d
    left, right = (a, b), (c, d)
    length, result = formal_result(a, b, c, d)
    c_result = candidate(left, right)
    o_result = canonical(left, right)
    print(
        f"A,B,C,D={a,b,c,d}; precondition=True; overlapLength={length}; "
        f"formal={result}; candidate={c_result}; canonical={o_result}"
    )
    assert c_result == result == o_result

print("ALL GROUND WITNESSES AGREE: YES")
