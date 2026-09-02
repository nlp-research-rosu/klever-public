#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load(Path("/reference/canonical.py"), "canonical_ground")
generated = load(Path("/candidate/solution.py"), "generated_ground")


def val_seq(values: list[int]) -> str:
    result = ".ValSeq"
    for value in reversed(values):
        result = f"vCons({value}, {result})"
    return result


cases = [
    [],
    [1, 11, -1, -11, -12],
    [11, 20, 101, 2],
]

print("entry_precondition_witness_template:")
print("  <k> #runOrderByPoints(list(VS)) </k>")
print("  env=0; scopes=initialScopes; scopeLoc=1; heap=.Map; heapLoc=0;")
print("  stack=.List; ret=noRet; exc=NoExc")
print()
for index, values in enumerate(cases):
    canonical_result = canonical.order_by_points(list(values))
    generated_result = generated.order_by_points(list(values))
    print(f"case_{index}_input_python:", values)
    print(f"case_{index}_VS:", val_seq(values))
    print(
        f"case_{index}_claimed_heap_term:",
        f"0 |-> list(sortKeyVS({val_seq(values)}, digitSumClosure))",
    )
    print(f"case_{index}_canonical_python:", canonical_result)
    print(f"case_{index}_generated_python:", generated_result)
    print(f"case_{index}_intended_result_VS:", val_seq(canonical_result))
    print(f"case_{index}_python_agreement:", canonical_result == generated_result)
    print()
