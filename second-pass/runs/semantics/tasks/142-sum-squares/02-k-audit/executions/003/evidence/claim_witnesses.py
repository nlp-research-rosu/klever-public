#!/usr/bin/env python3
"""Ground witnesses for all three reachability-claim preconditions."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Callable


def load_function(name: str, path: Path) -> Callable[[list[int]], int]:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sum_squares


canonical = load_function("canonical_witness", Path("/reference/canonical.py"))
candidate = load_function(
    "candidate_witness", Path("/tmp/audit-work/reconstruction/solution.py")
)


def contribution(index: int, value: int) -> int:
    if index % 3 == 0:
        return value * value
    if index % 4 == 0:
        return value * value * value
    return value


def summary(values: list[int], index: int, accumulator: int) -> int:
    for value in values:
        accumulator += contribution(index, value)
        index += 1
    return accumulator


def ints_term(values: list[int]) -> str:
    result = ".Ints"
    for value in reversed(values):
        result = f"intCons({value}, {result})"
    return result


# main and body witnesses.
entry_values = [1, 2, 3]
entry_expected = summary(entry_values, 0, 0)
print("MAIN_WITNESS:")
print(f"  IS={ints_term(entry_values)}")
print(
    '  exact binding=closureVal(("lst", .ParamNames), '
    "sumSquaresFunctionBody, 0)"
)
print(
    "  env=0 scopes=(-1 |-> builtinsScope, 0 |-> function scope) "
    "scopeLoc=1 heap=.Map heapLoc=0 stack=.List ret=noRet "
    "exc=NoExc exit-code=0"
)
print(f"  claimed sumSquares(IS,0,0)={entry_expected}")
print(f"  candidate_python={candidate(entry_values)}")
print(f"  canonical_python={canonical(entry_values)}")

print("BODY_WITNESS:")
print(f"  IS={ints_term(entry_values)}")
print(
    "  env=1; local scope 1 has lst, total=0, index=0; "
    "scopeLoc=2; stack=ListItem(frame(.K,0,1)); other cells as in claim"
)
print(f"  claimed sumSquares(IS,0,0)={entry_expected}")
print(f"  candidate_python={candidate(entry_values)}")
print(f"  canonical_python={canonical(entry_values)}")

# Loop witness corresponds to a real state after the prefix [1,2,3,2].
prefix = [1, 2, 3, 2]
remaining = [2, -3, 4]
full_values = prefix + remaining
prefix_accumulator = summary(prefix, 0, 0)
loop_expected = summary(remaining, len(prefix), prefix_accumulator)
print("LOOP_WITNESS:")
print(f"  IS={ints_term(remaining)}")
print(f"  ORIG={ints_term(full_values)}")
print(
    "  L=1 SC=.Map P=parent(0) KONT=.K OLD=2 "
    f"ACC={prefix_accumulator} I={len(prefix)}"
)
print(f"  claimed total={loop_expected}")
print(f"  claimed endIndex={len(full_values)}")
print(f"  claimed endValue={remaining[-1]}")
print(f"  candidate_python_full_list={candidate(full_values)}")
print(f"  canonical_python_full_list={canonical(full_values)}")

all_equal = (
    entry_expected
    == candidate(entry_values)
    == canonical(entry_values)
    and loop_expected
    == candidate(full_values)
    == canonical(full_values)
    and prefix_accumulator == 10
)
print(f"all_claim_witness_results_agree={all_equal}")
raise SystemExit(0 if all_equal else 1)
