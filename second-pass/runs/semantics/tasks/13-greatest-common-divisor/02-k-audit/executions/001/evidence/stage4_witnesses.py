#!/usr/bin/env python3
"""Concrete satisfiability/result witnesses for every submitted claim."""

from __future__ import annotations

import importlib.util
import json
import math
from pathlib import Path


ROOT = Path("/tmp/audit-work/source")


def load_entry(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.greatest_common_divisor


canonical = load_entry("canonical_witness", ROOT / "canonical.py")
submitted = load_entry("submitted_witness", ROOT / "solution.py")

# euclid-step: A>=0 and B>0, scope consists of the two local integer bindings.
A, B = 25, 15
euclid_after = (B, A % B)

witnesses = {
    "euclid-step": {
        "precondition": {"A": A, "B": B, "A>=0": A >= 0, "B>0": B > 0},
        "state": {
            "env": 1,
            "scope_1": {"a": A, "b": B, "parent": 0},
            "heap": {},
        },
        "post_scope_bindings": {"a": euclid_after[0], "b": euclid_after[1]},
    },
    "program-correct": {
        "arguments": [25, 15],
        "formal_rhs_ground_value": math.gcd(abs(25), abs(15)),
        "canonical": canonical(25, 15),
        "submitted": submitted(25, 15),
    },
    "example-3-5": {
        "arguments": [3, 5],
        "claimed": 1,
        "canonical": canonical(3, 5),
        "submitted": submitted(3, 5),
    },
    "example-25-15": {
        "arguments": [25, 15],
        "claimed": 5,
        "canonical": canonical(25, 15),
        "submitted": submitted(25, 15),
    },
}

assert euclid_after == (15, 10)
for label in ("program-correct", "example-3-5", "example-25-15"):
    values = witnesses[label]
    expected = values.get("claimed", values.get("formal_rhs_ground_value"))
    assert values["canonical"] == expected
    assert values["submitted"] == expected

print(json.dumps(witnesses, indent=2))
