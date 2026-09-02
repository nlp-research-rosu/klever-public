#!/usr/bin/env python3
"""Concrete satisfying-input comparison for arr = [1, 2]."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.smallest_change


arr = [1, 2]
canonical = load("canonical_ground", Path("/reference/canonical.py"))(list(arr))
candidate = load("candidate_ground", Path("/candidate/solution.py"))(list(arr))
claimed = 1
print(f"input={arr!r}")
print("formal_precondition=allInts(vCons(1,vCons(2,.ValSeq)))")
print("formal_precondition_satisfied=true")
print(f"claimed_ground_result={claimed}")
print(f"trusted_canonical_result={canonical}")
print(f"candidate_python_result={candidate}")
print(f"all_equal={claimed == canonical == candidate}")
raise SystemExit(0 if claimed == canonical == candidate else 1)
