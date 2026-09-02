#!/usr/bin/env python3
"""Concrete satisfying states and substitutions for the two K entry claims."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


def load_maximum(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.maximum


def formal_rhs(arr: list[int], k: int) -> dict[str, object]:
    if k == 0:
        return {
            "returned_ref": 0,
            "heap": {"0": []},
            "heapLoc": 1,
        }
    sorted_values = sorted(arr)
    return {
        "returned_ref": 1,
        "heap": {
            "0": sorted_values,
            "1": sorted_values[len(arr) - k : len(arr) : 1],
        },
        "heapLoc": 2,
    }


def main() -> int:
    canonical = load_maximum(
        Path("/tmp/audit-work/120-maximum/trusted/canonical.py"), "canonical_witness"
    )
    candidate = load_maximum(
        Path("/tmp/audit-work/120-maximum/candidate-source/solution.py"),
        "candidate_witness",
    )
    witnesses = [
        {
            "claim": "k-zero",
            "arr": [7, -2],
            "k": 0,
            "precondition": "true (no requires clause)",
            "formal_input": "Call(Name(\"maximum\"), list(vCons(7,vCons(-2,.ValSeq))), 0, .Exprs)",
        },
        {
            "claim": "k-positive",
            "arr": [-3, -4, 5],
            "k": 2,
            "precondition": "0 < 2 and 2 <= vsLen([-3,-4,5]) = 3",
            "formal_input": "Call(Name(\"maximum\"), list(vCons(-3,vCons(-4,vCons(5,.ValSeq)))), 2, .Exprs)",
        },
    ]
    failed = False
    for witness in witnesses:
        arr = witness["arr"]
        k = witness["k"]
        assert isinstance(arr, list)
        assert isinstance(k, int)
        canonical_value = canonical(list(arr), k)
        candidate_value = candidate(list(arr), k)
        rhs = formal_rhs(arr, k)
        returned = rhs["heap"][str(rhs["returned_ref"])]
        record = dict(witness)
        record.update(
            {
                "shared_cells": {
                    "env": 0,
                    "scopeLoc": 1,
                    "stack": [],
                    "ret": "noRet",
                    "exc": "NoExc",
                    "heap_initial": {},
                    "heapLoc_initial": 0,
                },
                "formal_rhs": rhs,
                "canonical_result": canonical_value,
                "candidate_result": candidate_value,
                "formal_returned_list": returned,
                "all_equal": canonical_value == candidate_value == returned,
            }
        )
        failed |= not record["all_equal"]
        print(json.dumps(record, sort_keys=True))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
