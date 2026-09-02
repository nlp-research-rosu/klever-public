#!/usr/bin/env python3
"""Concrete witnesses for the three reachability-claim preconditions."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.digitSum


canonical = load_function(
    Path("/tmp/audit-work/66-digitsum.dlRQYF/trusted/canonical.py"),
    "trusted_canonical_witness",
)
candidate = load_function(
    Path("/tmp/audit-work/66-digitsum.dlRQYF/candidate/solution.py"),
    "candidate_solution_witness",
)


def formal_spec(value: str) -> int:
    return sum(
        code if 65 <= code <= 90 else 0
        for code in map(ord, value)
    )


claim_witnesses = {
    "entry-point": {
        "S": [65, 90, 97],
        "k": 'Call(closureVal(("s", .ParamNames), digitSumBody, 0), '
        "(str(iCons(65, iCons(90, iCons(97, .IntSeq)))), .Exprs))",
        "env": 0,
        "scopeLoc": 1,
        "heap": ".Map",
        "heapLoc": 0,
        "stack": ".List",
        "ret": "noRet",
        "exc": "NoExc",
        "exit-code": 0,
    },
    "initialization": {
        "S": [65, 90, 97],
        "same_initial_cells_as_entry": True,
    },
    "loop-invariant": {
        "S": [65, 122, 90],
        "A": 7,
        "INPUT": "str(iCons(1, .IntSeq))",
        "OLDCHAR": "str(.IntSeq)",
        "OLDCODE": 0,
        "env": 1,
        "scopeLoc": 2,
        "stack": "ListItem(frame(.K, 0, 1))",
        "claimed_result": 7 + formal_spec("AzZ"),
    },
}

comparisons = []
for value in ("", "@AZ[", "AZa", "É", "aΩZ"):
    comparisons.append(
        {
            "input": value,
            "codepoints": list(map(ord, value)),
            "formal_digitSumSpec": formal_spec(value),
            "candidate_python": candidate(value),
            "trusted_canonical_python": canonical(value),
        }
    )

print(
    json.dumps(
        {
            "claim_precondition_witnesses": claim_witnesses,
            "ground_result_substitutions": comparisons,
        },
        indent=2,
        ensure_ascii=True,
    )
)
