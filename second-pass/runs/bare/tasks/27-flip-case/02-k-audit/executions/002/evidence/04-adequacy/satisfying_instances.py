#!/usr/bin/env python3
"""Exhibit concrete states satisfying each entry claim and compare results."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


def load_function(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.flip_case


canonical = load_function(
    Path("/tmp/audit-work/trusted/canonical.py"), "adequacy_canonical"
)
candidate = load_function(
    Path("/tmp/audit-work/candidate/solution.py"), "adequacy_candidate"
)

instances = [
    ("symbolic-entry-empty", "", ""),
    ("symbolic-entry-ascii", "Hello", "hELLO"),
    ("symbolic-entry-expansion", "ß", "SS"),
    ("concrete-example-claim", "Hello", "hELLO"),
    ("concrete-unicode-claim", "Straße Δelta", "sTRASSE δELTA"),
]
for label, argument, claimed_result in instances:
    canonical_result = canonical(argument)
    candidate_result = candidate(argument)
    print(
        label,
        "initial_state",
        {
            "k": "exact submitted Module/FuncDef body",
            "arg": json.dumps(argument, ensure_ascii=True),
            "functions": ".Map",
            "env": ".Map",
        },
        "claimed",
        json.dumps(claimed_result, ensure_ascii=True),
        "canonical",
        json.dumps(canonical_result, ensure_ascii=True),
        "candidate",
        json.dumps(candidate_result, ensure_ascii=True),
        "all_equal",
        claimed_result == canonical_result == candidate_result,
    )
    if claimed_result != canonical_result or canonical_result != candidate_result:
        raise SystemExit(1)
print("instance_count", len(instances))
print("all_instances_satisfiable_and_equal", True)
