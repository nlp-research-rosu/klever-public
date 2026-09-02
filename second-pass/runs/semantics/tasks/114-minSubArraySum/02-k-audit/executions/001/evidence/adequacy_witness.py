#!/usr/bin/env python3
"""Concrete witnesses for each formal entry shape and claimed recurrence."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


def load_entry(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.minSubArraySum


def choose_smaller(first: int, second: int) -> int:
    return first if first < second else second


def fold_loop(sequence: list[int], current: int, smallest: int):
    value = None
    for value in sequence:
        current = choose_smaller(value, current + value)
        smallest = choose_smaller(current, smallest)
    return {"smallest": smallest, "current": current, "value": value}


def k_spec(sequence: list[int]) -> int:
    head, *tail = sequence
    return fold_loop(tail, head, head)["smallest"]


canonical = load_entry("adequacy_canonical", Path("/reference/canonical.py"))
generated = load_entry(
    "adequacy_generated",
    Path("/tmp/audit-work/review-114.pELioR/candidate-src/solution.py"),
)

function_inputs = [
    [3, -4, 2, -3, -1, 7, -5],
    [5],
    [-1, -2, -3],
]
function_results = []
for nums in function_inputs:
    result = {
        "input": nums,
        "k_minSubArraySumSpec": k_spec(nums),
        "trusted_canonical": canonical(list(nums)),
        "generated_solution": generated(list(nums)),
    }
    result["all_equal"] = (
        result["k_minSubArraySumSpec"]
        == result["trusted_canonical"]
        == result["generated_solution"]
    )
    function_results.append(result)

loop_sequence = [-2, 3, -5]
loop_witness = {
    "I": -2,
    "R": [3, -5],
    "C": 4,
    "B": -1,
    "INPUT": [99],
    "OLD": 123,
    "L": 1,
    "lhs_scope": {
        "nums": [99],
        "smallest": -1,
        "current": 4,
        "value": 123,
        "parent": 0,
    },
    "rhs_scope": {
        "nums": [99],
        **fold_loop(loop_sequence, 4, -1),
        "parent": 0,
    },
}

load_witness = {
    "k": "#loadAll(Module(minSubArraySumDef .Stmts))",
    "env": 0,
    "scopes": {
        "0": "scope(.Map, parent(-1))",
        "-1": "builtinsScope",
    },
    "scopeLoc": 1,
    "heap": ".Map",
    "heapLoc": 0,
    "stack": ".List",
    "ret": "noRet",
    "exc": "NoExc",
    "exit_code": 0,
}

function_witness = {
    "H": 3,
    "T": [-4, 2, -3, -1, 7, -5],
    "argument": "list(intVals(iCons(3, ...)))",
    "env": 0,
    "scopes": {
        "0": "scope(.Map, parent(-1))",
        "-1": "builtinsScope",
    },
    "scopeLoc": 1,
    "heap": ".Map",
    "heapLoc": 0,
    "stack": ".List",
    "ret": "noRet",
    "exc": "NoExc",
    "exit_code": 0,
    "claimed_result": k_spec(function_inputs[0]),
}

record = {
    "loop_entry_satisfying_state": loop_witness,
    "load_entry_satisfying_state": load_witness,
    "function_entry_satisfying_state": function_witness,
    "function_substitutions": function_results,
}
output = Path("/audit-output/evidence/adequacy-witness.json")
output.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
print(json.dumps(record, indent=2))

if not all(item["all_equal"] for item in function_results):
    raise SystemExit(1)
