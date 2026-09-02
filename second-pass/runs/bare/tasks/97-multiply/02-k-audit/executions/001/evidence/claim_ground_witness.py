#!/usr/bin/env python3
"""Ground witnesses for the candidate's entry claim."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


def load_entry(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.multiply


candidate = load_entry(
    Path("/tmp/audit-work/97-multiply/candidate-source/solution.py"),
    "ground_candidate",
)
canonical = load_entry(
    Path("/tmp/audit-work/97-multiply/trusted/canonical.py"),
    "ground_canonical",
)

for a, b in [(148, 412), (-1, 1), (-14, 15)]:
    formal_result = (abs(a) % 10) * (abs(b) % 10)
    print(json.dumps({
        "satisfies_entry_precondition": True,
        "precondition_explanation": "A and B are arbitrary mathematical integers; no requires clause",
        "A": a,
        "B": b,
        "formal_claim_result": formal_result,
        "candidate_python_result": candidate(a, b),
        "trusted_canonical_result": canonical(a, b),
    }, sort_keys=True))
