#!/usr/bin/env python3
"""Concrete satisfying witness for the target claim's source-domain precondition."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


root = Path("/tmp/audit-work/rebuild")
canonical = load("canonical_witness", root / "reference" / "canonical.py")
candidate = load("candidate_witness", root / "solution.py")
input_value = ["3"]
print(f"input={input_value!r}")
print("K encoding=list(vCons(str(iCons(51, .IntSeq)), .ValSeq))")
print("validDigitStrings=true (51 is ASCII '3', and 48 <= 51 <= 57)")
print(f"canonical_result={canonical.odd_count(input_value)!r}")
print(f"candidate_result={candidate.odd_count(input_value)!r}")
