#!/usr/bin/env python3
"""Print and check trusted/candidate Python results for one concrete K run."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


x, y, expected = map(int, sys.argv[1:4])
canonical = load_module("trusted_humaneval_102_concrete", Path("/reference/canonical.py"))
generated = load_module("generated_solution_102_concrete", Path("/tmp/audit-work/solution.py"))
canonical_result = canonical.choose_num(x, y)
generated_result = generated.choose_num(x, y)
print(
    f"x={x} y={y} expected={expected} "
    f"canonical={canonical_result} generated={generated_result}"
)
if canonical_result != expected or generated_result != expected:
    raise SystemExit(1)
