#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.monotonic


canonical = load(Path("/reference/canonical.py"), "canonical_witness")
generated = load(
    Path("/tmp/audit-work/57-monotonic/solution.py"), "generated_witness"
)


def nondecreasing(values):
    return all(a <= b for a, b in zip(values, values[1:]))


def nonincreasing(values):
    return all(a >= b for a, b in zip(values, values[1:]))


witnesses = [
    ("claim-1", [1, 2, 2]),
    ("claim-2-false-result", [1, 0, 1]),
    ("claim-2-true-result", [2, 1]),
]
for claim, values in witnesses:
    nd = nondecreasing(values)
    ni = nonincreasing(values)
    record = {
        "claim": claim,
        "input": values,
        "nondecreasing": nd,
        "not_nondecreasing": not nd,
        "nonincreasing": ni,
        "formal_claimed_result": True if claim == "claim-1" else ni,
        "canonical_result": canonical(values.copy()),
        "generated_result": generated(values.copy()),
    }
    print(json.dumps(record, sort_keys=True))
