#!/usr/bin/env python3
"""Ground witnesses for both candidate claims and the source contract."""

from __future__ import annotations

import importlib.util
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/reconstruction")


def load(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.largest_smallest_integers


canonical = load(SCRATCH / "canonical.py", "witness_canonical")
candidate = load(SCRATCH / "solution.py", "witness_candidate")


def neg_step(accumulator: int, value: int) -> int:
    if value < 0 and (accumulator == 0 or value > accumulator):
        return value
    return accumulator


def pos_step(accumulator: int, value: int) -> int:
    if value > 0 and (accumulator == 0 or value < accumulator):
        return value
    return accumulator


def neg_fold(values: list[int], accumulator: int) -> int:
    for value in values:
        accumulator = neg_step(accumulator, value)
    return accumulator


def pos_fold(values: list[int], accumulator: int) -> int:
    for value in values:
        accumulator = pos_step(accumulator, value)
    return accumulator


def optional(value: int):
    return None if value == 0 else value


entry_values = [-5, -2, 0, 7, 3]
entry_model = (
    optional(neg_fold(entry_values, 0)),
    optional(pos_fold(entry_values, 0)),
)
entry_canonical = canonical(entry_values.copy())
entry_candidate = candidate(entry_values.copy())
print("ENTRY WITNESS")
print(f"VS={entry_values!r}")
print("precondition allInts(VS)=true")
print("initial cells: env=0 scopeLoc=1 heap={} heapLoc=0 stack=[] ret=noRet exc=NoExc exit-code=0")
print(f"K postcondition model={entry_model!r}")
print(f"trusted canonical={entry_canonical!r}")
print(f"generated Python={entry_candidate!r}")

loop_values = [-5, -2, 0, 7, 3]
loop_a = -9
loop_b = 10
loop_old = 42
loop_post = (
    neg_fold(loop_values, loop_a),
    pos_fold(loop_values, loop_b),
    loop_values[-1] if loop_values else loop_old,
)
print("LOOP WITNESS")
print(f"VS={loop_values!r} A={loop_a} B={loop_b} OLD={loop_old}")
print("preconditions allInts(VS)=true, A<=0=true, B>=0=true")
print(f"post bindings largest_negative, smallest_positive, value={loop_post!r}")

empty_model = (optional(neg_fold([], 0)), optional(pos_fold([], 0)))
print("EMPTY ENTRY WITNESS")
print(f"K postcondition model={empty_model!r}")
print(f"trusted canonical={canonical([])!r}")
print(f"generated Python={candidate([])!r}")

assert entry_model == entry_canonical == entry_candidate
assert empty_model == canonical([]) == candidate([])
