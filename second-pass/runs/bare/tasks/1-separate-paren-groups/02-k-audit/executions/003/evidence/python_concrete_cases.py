#!/usr/bin/env python3
"""Python oracle outputs corresponding to the fresh K concrete executions."""

import importlib.util
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.separate_paren_groups


canonical = load(Path("/tmp/audit-work/trusted/canonical.py"), "canonical_cases")
candidate = load(Path("/tmp/audit-work/rebuild/solution.py"), "candidate_cases")

cases = [
    "( ) (( )) (( )( ))",
    "",
    "()",
    "(((())))",
    "()(())(()())",
    "   ",
]

for text in cases:
    canonical_result = canonical(text)
    candidate_result = candidate(text)
    assert canonical_result == candidate_result
    print(f"{text!r} -> {candidate_result!r}")
