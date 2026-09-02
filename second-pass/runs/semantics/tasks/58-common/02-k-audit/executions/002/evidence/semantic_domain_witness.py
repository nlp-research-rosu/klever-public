#!/usr/bin/env python3
"""Print source-level outputs for the two mixed-numeric K-semantics witnesses."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.common


canonical = load("canonical_witness", Path("/reference/canonical.py"))
generated = load("generated_witness", Path("/tmp/audit-work/58-common-002/solution.py"))

for first, second in (([True], [1]), ([1], [1.0])):
    expected = canonical(first.copy(), second.copy())
    actual = generated(first.copy(), second.copy())
    print(f"FIRST={first!r} SECOND={second!r} canonical={expected!r} generated={actual!r}")
    assert expected == actual and expected

print("SOURCE_WITNESSES_OK")
