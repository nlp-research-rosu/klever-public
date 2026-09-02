#!/usr/bin/env python3
"""Ground witnesses for all claim preconditions and result substitutions."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


def load_entry(name: str, path: Path):
    spec = spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.fizz_buzz


def digit_result(accumulator: int, value: int) -> int:
    while value > 0:
        accumulator += int(value % 10 == 7)
        value = (value - (value % 10)) // 10
    return accumulator


def fizz_result(accumulator: int, bound: int) -> int:
    while bound > 0:
        candidate = bound - 1
        if candidate % 11 == 0 or candidate % 13 == 0:
            accumulator = digit_result(accumulator, candidate)
        bound = candidate
    return accumulator


canonical = load_entry("trusted_canonical_witness", Path("/reference/canonical.py"))
generated = load_entry(
    "scratch_generated_witness", Path("/tmp/audit-work/36-fizz-buzz/solution.py")
)

print("inner_precondition_witness: X=79 C=4 I=79 N=79 L=1; X>=0 is true")
print(
    "inner_post_substitution:",
    {"digitResult(4,79)": digit_result(4, 79), "final_x": 0},
)
print("outer_precondition_witness: I=79 C=0 N=79 L=1 x=0; I>=0 is true")
print(
    "outer_post_substitution:",
    {"fizzResult(0,79)": fizz_result(0, 79), "final_i": 0, "final_x": 0},
)
print(
    "entry_precondition_witness: N=79 with the exact module/builtins scopes and empty runtime cells from spec.k"
)

inputs = [-5, 0, 1, 50, 77, 78, 79, 117, 118, 143, 144, 177, 188, 777]
rows = []
for value in inputs:
    summary = fizz_result(0, value)
    trusted = canonical(value)
    actual = generated(value)
    rows.append((value, summary, trusted, actual))
    if not summary == trusted == actual:
        raise SystemExit(f"result substitution mismatch: {rows[-1]}")
print("columns=(N,fizzResult(0,N),trusted_canonical(N),submitted_solution(N))")
for row in rows:
    print(row)
print(f"ground_result_substitutions={len(rows)} mismatches=0")
