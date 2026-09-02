#!/usr/bin/env python3
"""Check each ground K claim against both trusted and submitted Python."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.parse_nested_parens


canonical = load_entry(
    Path("/tmp/audit-work/6-parse-nested-parens/trusted/canonical.py"),
    "claim_canonical",
)
candidate = load_entry(
    Path("/tmp/audit-work/6-parse-nested-parens/candidate-src/solution.py"),
    "claim_candidate",
)

claims = [
    ("(()()) ((())) () ((())()())", [2, 3, 1, 3]),
    ("() (()) ((())) (((())))", [1, 2, 3, 4]),
    ("(()(())((())))", [4]),
]

failures = 0
for index, (value, claimed) in enumerate(claims, start=1):
    canonical_result = canonical(value)
    candidate_result = candidate(value)
    agrees = canonical_result == candidate_result == claimed
    failures += not agrees
    print(
        json.dumps(
            {
                "claim": index,
                "satisfying_input": value,
                "claimed_result": claimed,
                "canonical_result": canonical_result,
                "candidate_result": candidate_result,
                "all_equal": agrees,
            },
            sort_keys=True,
        )
    )

print(json.dumps({"failures": failures}, sort_keys=True))
raise SystemExit(0 if failures == 0 else 1)
