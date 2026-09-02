#!/usr/bin/env python3
"""Exhibit satisfying entry/loop states and evaluate their ground summaries."""

from __future__ import annotations

import importlib.util
import json
import math
from pathlib import Path
from types import ModuleType


def load(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def summary(accumulator: int, values: list[int | float]) -> int:
    for value in values:
        accumulator += math.ceil(value) ** 2
    return accumulator


def main() -> int:
    values: list[int | float] = [1.4, 4.2, 0]
    canonical = load("canonical_witness", Path("/reference/canonical.py"))
    candidate = load(
        "candidate_witness",
        Path("/tmp/audit-work/133-sum-squares-audit/solution.py"),
    )
    record = {
        "function_claim_precondition": {
            "k": "Call(closureVal(EXACT_SUBMITTED_BODY, 0), list(vCons(1.4, vCons(4.2, vCons(0, .ValSeq))))) ~> CONT",
            "env": 0,
            "scopes": "0 |-> scope(.Map,parent(-1))  -1 |-> builtinsScope",
            "scopeLoc": 1,
            "stack": ".List",
            "ret": "noRet",
            "requires": "true (the function claim has no requires clause)",
        },
        "function_claim_postcondition": {
            "term": "sumSquaresFrom(0, vCons(1.4, vCons(4.2, vCons(0, .ValSeq))))",
            "ground_value": summary(0, values),
            "canonical_python": canonical.sum_squares(values),
            "candidate_python": candidate.sum_squares(values),
        },
        "reachable_loop_claim_precondition_after_first_iteration": {
            "remaining_VS": [4.2, 0],
            "L": 1,
            "GLOBAL_keys": [-1, 0],
            "requires_not_L_in_GLOBAL": True,
            "INPUT": values,
            "CURRENT": 1.4,
            "ACC": 4,
            "PARENT": "parent(0)",
            "CONT": "Return(Name(\"result\")) ~> #endcall",
        },
        "loop_claim_postcondition": {
            "sumSquaresFrom(4,[4.2,0])": summary(4, [4.2, 0]),
            "lastFrom(1.4,[4.2,0])": 0,
        },
    }
    print(json.dumps(record, indent=2, sort_keys=True))
    values_to_check = [
        record["function_claim_postcondition"]["ground_value"],
        record["function_claim_postcondition"]["canonical_python"],
        record["function_claim_postcondition"]["candidate_python"],
        record["loop_claim_postcondition"]["sumSquaresFrom(4,[4.2,0])"],
    ]
    return 0 if values_to_check == [29, 29, 29, 29] else 1


if __name__ == "__main__":
    raise SystemExit(main())
