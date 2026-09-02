#!/usr/bin/env python3
"""Concrete realizability and result substitutions for the three claims."""

from __future__ import annotations

import importlib.util
import json
import math
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sum_product


canonical = load(Path("/reference/canonical.py"), "canonical_ground")
candidate = load(
    Path("/tmp/audit-work/reconstruction/solution.py"), "candidate_ground"
)

witnesses = [
    {
        "claim": "SPEC.sum-product",
        "input": [1, 2, 3, 4],
        "reason": "exactly four K Int values satisfy the entry pattern",
    },
    {
        "claim": "LOOP-SPEC.sum-product-loop",
        "input": [],
        "reason": "allIntVals(.ValSeq) is true; accumulators are 0 and 1",
    },
    {
        "claim": "FOR-SPEC.sum-product-for",
        "input": [2, 3],
        "reason": "allIntVals([2,3]) is true; accumulators are 0 and 1",
    },
]

for witness in witnesses:
    values = witness["input"]
    expected = (sum(values), math.prod(values))
    witness["fold_summary"] = list(expected)
    witness["trusted_canonical"] = list(canonical(list(values)))
    witness["candidate_python"] = list(candidate(list(values)))
    witness["all_equal"] = (
        tuple(witness["trusted_canonical"])
        == tuple(witness["candidate_python"])
        == expected
    )

print(json.dumps(witnesses, indent=2, sort_keys=True))
raise SystemExit(0 if all(item["all_equal"] for item in witnesses) else 1)
