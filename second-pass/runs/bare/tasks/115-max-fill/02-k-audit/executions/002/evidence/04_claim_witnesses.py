#!/usr/bin/env python3
"""Ground witnesses for each symbolic claim and the source-contract result."""

from __future__ import annotations

import importlib.util
from pathlib import Path


WORK = Path("/tmp/audit-work/reconstruction")


def load_module(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load_module(WORK / "reference/canonical.py", "claim_canonical")
candidate = load_module(WORK / "solution.py", "claim_candidate")

row = [1, 0, 1]
grid = [row, [0, 1, 1]]
capacity = 2

water_result = sum(row)
required_result = sum(
    (sum(current_row) + capacity - 1) // capacity
    for current_row in grid
)
canonical_result = canonical.max_fill(grid, capacity)
candidate_result = candidate.max_fill(grid, capacity)

print("CLAIM 1 SATISFYING GROUND STATE")
print(
    '<k> invoke("_water_in", arg(rowVal(1,0,1), noArgs)) ~> .K </k>'
)
print("<functions> solutionFunctions </functions>")
print("<args> .Vals </args> <env> .Map </env> <result> noneVal </result>")
print(f"claimed water(1,0,1)={water_result}")
print(f"candidate _water_in={candidate._water_in(row)}")
print(
    "cross-check at capacity 1: "
    f"canonical max_fill={[canonical.max_fill([row], 1)]} "
    f"candidate max_fill={[candidate.max_fill([row], 1)]}"
)

print("CLAIM 2 SATISFYING GROUND STATE")
print(
    '<k> invoke("_buckets_for", '
    "arg(gridVal(rowVal(1,0,1),rowVal(0,1,1)), "
    "arg(intVal(2), noArgs))) ~> .K </k>"
)
print("<functions> solutionFunctions </functions>")
print("<args> .Vals </args> <env> .Map </env> <result> noneVal </result>")
print(f"precondition C >Int 0: {capacity} > 0")
print(f"claimed requiredBuckets={required_result}")
print(f"candidate _buckets_for={candidate._buckets_for(grid, capacity)}")
print(f"canonical max_fill={canonical_result}")
print(f"candidate max_fill={candidate_result}")

print("CLAIM 3 SATISFYING GROUND STATE")
print("<k> solutionProgram </k>")
print(
    "<args> gridVal(rowVal(1,0,1),rowVal(0,1,1)), intVal(2) </args>"
)
print("<functions> .Map </functions> <env> .Map </env> <result> noneVal </result>")
print(f"precondition C >Int 0: {capacity} > 0")
print(f"claimed final result={required_result}")
print(f"canonical max_fill={canonical_result}")
print(f"candidate max_fill={candidate_result}")

if not (
    water_result == candidate._water_in(row)
    and required_result == candidate._buckets_for(grid, capacity)
    and required_result == canonical_result == candidate_result
):
    raise SystemExit(1)
