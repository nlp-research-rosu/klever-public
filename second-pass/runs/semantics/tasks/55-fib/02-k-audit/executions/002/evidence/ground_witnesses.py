#!/usr/bin/env python3
"""Ground witnesses for the entry and loop claim preconditions/results."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, Path(path))
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def fib_run(a: int, b: int, i: int, n: int) -> int:
    while i < n:
        a, b, i = b, a + b, i + 1
    return a


canonical = load("canonical_ground", "/reference/canonical.py")
candidate = load("candidate_ground", "/candidate/solution.py")

for n in (0, 1, 2, 8, 10, 30):
    assert n >= 0
    formal = fib_run(0, 1, 0, n)
    trusted_python = canonical.fib(n)
    generated_python = candidate.fib(n)
    print(
        f"entry_witness N={n} precondition={n >= 0} "
        f"fibSpec={formal} canonical={trusted_python} candidate={generated_python}"
    )
    assert formal == trusted_python == generated_python

print(
    "loop_witness="
    "L=1,REST=(0|->module,-1|->builtins),N=3,I=0,A=0,B=1,_=0,"
    "scopeLoc=2,heap=.Map,heapLoc=0,stack=callee-frame,ret=noRet,exc=NoExc,exit=0"
)
print("loop_witness_fibRun_result=", fib_run(0, 1, 0, 3), sep="")
