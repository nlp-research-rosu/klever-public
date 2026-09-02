#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
from pathlib import Path


def load_entry(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.move_one_ball


canonical = load_entry("canonical_for_witness", Path("/reference/canonical.py"))
generated = load_entry("generated_for_witness", Path("/candidate/solution.py"))


def scan(values: list[int], previous: int, drops: int) -> tuple[int, int]:
    for current in values:
        drops += int(current < previous)
        previous = current
    return drops, previous


def summary(values: list[int]) -> bool:
    if not values:
        return True
    drops, last = scan(values, values[0], 0)
    drops += int(values[0] < last)
    return drops < 2


tail = [4, 1]
drops, last = scan(tail, previous=5, drops=0)
print("loop_induction_precondition_witness:")
print("  C=4, IS=iCons(1,.IntSeq), KONT=.K")
print("  env=1; local arr=[5,4,1], drops=0, first=5, previous=5, current=99")
print("  parent(0); arbitrary well-sorted BUILTINS and MODSCOPE values")
print(f"  expected post local drops={drops}, previous={last}, current={last}")
assert (drops, last) == (2, 1)

print("loop_entry_precondition_witness:")
print("  C=4, IS=iCons(1,.IntSeq), KONT=.K")
print("  env=1; local arr=[5,4,1], drops=0, first=5, previous=5; current absent")
print("  parent(0); arbitrary well-sorted BUILTINS and MODSCOPE values")
print(f"  expected post local drops={drops}, previous={last}, current={last}")

cases = [
    [],
    [3, 4, 5, 1, 2],
    [3, 5, 4, 1, 2],
    [2, 3, 1],
]
print("functional_entry_precondition_witnesses:")
for values in cases:
    k_summary = summary(values)
    canonical_result = canonical(list(values))
    generated_result = generated(list(values))
    print(
        f"  input={values} moveOneBallSpec={k_summary} "
        f"canonical={canonical_result} generated={generated_result}"
    )
    assert k_summary == canonical_result == generated_result

print("functional_entry_exact_initial_cells:")
print("  env=0; scopes={0: move_one_ball closure, -1: builtinsScope}")
print("  scopeLoc=1; heap={}; heapLoc=0; stack=[]; ret=noRet; exc=NoExc; exit=0")
print("CLAIM_WITNESSES=PASS")
