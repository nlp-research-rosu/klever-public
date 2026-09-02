#!/usr/bin/env python3
"""Ground witnesses for the entry and auxiliary claim preconditions/results."""

from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path("/tmp/audit-work/reconstruction")


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.below_zero


canonical = load("canonical_witness", ROOT / "canonical.py")
candidate = load("candidate_witness", ROOT / "solution.py")


def mathematical_contract(operations: list[int], initial: int = 0) -> bool:
    balance = initial
    for operation in operations:
        balance += operation
        if balance < 0:
            return True
    return False


print("MAIN satisfying state:")
print("  IS=intCons(1,intCons(-2,.IntVals)); env=0; scopeLoc=1;")
print("  scopes={0:scope(.Map,parent(-1)),-1:builtinsScope};")
print("  heap=.Map; heapLoc=0; stack=.List; ret=noRet; exc=NoExc; exit=0")
print("AUX satisfying state:")
print("  IS=intCons(-2,.IntVals); B=1; INPUT=intCons(1,intCons(-2,.IntVals));")
print("  OLD=1; MODULE=.Map; BUILTINS=builtinsScope; HEAP=.Map; NEXT=0;")
print("  env=1; scopeLoc=2; stack=[frame(.K,0,1)]; ret=noRet; exc=NoExc; exit=0")

cases = [[], [-1], [1, -1], [1, -2], [2, -1, -1], [2, -1, -2]]
for operations in cases:
    formal = mathematical_contract(operations)
    trusted = canonical(list(operations))
    generated = candidate(list(operations))
    print(
        f"input={operations!r} prefixBelow(0,IS)={formal} "
        f"canonical={trusted} generated={generated}"
    )
    if not (formal == trusted == generated):
        raise SystemExit(1)
