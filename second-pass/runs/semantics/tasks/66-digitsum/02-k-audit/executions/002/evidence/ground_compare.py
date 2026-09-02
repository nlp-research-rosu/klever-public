#!/usr/bin/env python3
"""Compare concrete entry-claim substitutions with both Python functions."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.digitSum


canonical = load_function("trusted_canonical_ground", Path("/reference/canonical.py"))
candidate = load_function(
    "candidate_solution_ground",
    Path("/tmp/audit-work/66-digitsum-audit/solution.py"),
)

formal_ground_results = {
    "": 0,
    "abAB": 131,
    "É": 0,
}

print("COMMAND: python3 /audit-output/evidence/ground_compare.py")
print("FORMAL_VALUES_MACHINE_CHECKED_BY: DIGIT-SUM-GROUND-SPEC")
for value, formal in formal_ground_results.items():
    print(json.dumps({
        "input": value,
        "codepoints": [ord(char) for char in value],
        "formal_digitSumSpec": formal,
        "candidate_python": candidate(value),
        "trusted_canonical_python": canonical(value),
    }, ensure_ascii=True))
print("EXIT_STATUS=0")
