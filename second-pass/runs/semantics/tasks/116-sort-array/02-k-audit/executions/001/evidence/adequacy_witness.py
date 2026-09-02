#!/usr/bin/env python3
"""Concrete witnesses for every positive claim precondition."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


def load(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def val_seq(values: list[int]) -> str:
    term = ".ValSeq"
    for value in reversed(values):
        term = f"vCons({value}, {term})"
    return term


canonical = load("adequacy_canonical", "/reference/canonical.py")
candidate = load("adequacy_candidate", "/tmp/audit-work/rebuild/solution.py")

entry_input = [1, 5, 2, 3, 4]
canonical_result = canonical.sort_array(list(entry_input))
candidate_result = candidate.sort_array(list(entry_input))
assert canonical_result == candidate_result == [1, 2, 4, 3, 5]

vs = val_seq(entry_input)
witnesses = {
    "load_claim": {
        "precondition": "none beyond the fully pinned initial configuration",
        "satisfying_state": {
            "k": "#loadAll(sortArrayModule)",
            "env": 0,
            "scopes": "0 |-> scope(.Map,parent(-1)); -1 |-> builtinsScope",
            "heap": ".Map",
            "heapLoc": 0,
            "stack": ".List",
            "ret": "noRet",
            "exc": "NoExc",
            "exit_code": 0,
        },
    },
    "entry_claim": {
        "input": entry_input,
        "k_val_seq": vs,
        "precondition": f"allNonNegativeInts({vs}) = true",
        "substituted_formal_result": (
            f"ref(1), with heap[0]=list(sortVS({vs})) and "
            f"heap[1]=list(sortKeyVS(sortVS({vs}),popcountKeyClosure))"
        ),
        "supplied_sort_contract_interpretation": [1, 2, 4, 3, 5],
        "trusted_canonical_python": canonical_result,
        "candidate_python": candidate_result,
    },
    "nonnegative_key_claim": {
        "N": 5,
        "precondition": "5 >= 0",
        "substituted_formal_result": (
            "cntSub(iCons(48,iCons(98,binCodes(5))),iCons(49,.IntSeq))"
        ),
        "ordinary_value": bin(5).count("1"),
    },
    "negative_key_claim": {
        "N": -1,
        "precondition": "-1 < 0",
        "substituted_formal_result": 0,
        "candidate_branch_value": 0 if -1 < 0 else bin(-1).count("1"),
        "domain_note": "outside the stated non-negative input domain",
    },
}
print(json.dumps(witnesses, indent=2))
