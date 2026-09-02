#!/usr/bin/env python3
"""Compare concrete satisfying witnesses with both Python entry points."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, Path(path))
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load("canonical_witness", "/reference/canonical.py")
generated = load(
    "generated_witness", "/tmp/audit-work/reconstruction/solution.py"
)

witnesses = [
    ([], []),
    (
        ["1234567"],
        ["the number of odd elements 4n the str4ng 4 of the 4nput."],
    ),
    (
        ["3", "11111111"],
        [
            "the number of odd elements 1n the str1ng 1 of the 1nput.",
            "the number of odd elements 8n the str8ng 8 of the 8nput.",
        ],
    ),
]
for value, claimed in witnesses:
    canonical_result = canonical.odd_count(value)
    generated_result = generated.odd_count(value)
    print(f"input={value!r}")
    print(f"claimed={claimed!r}")
    print(f"canonical={canonical_result!r}")
    print(f"generated={generated_result!r}")
    assert claimed == canonical_result == generated_result
print(f"witnesses={len(witnesses)} mismatches=0")
