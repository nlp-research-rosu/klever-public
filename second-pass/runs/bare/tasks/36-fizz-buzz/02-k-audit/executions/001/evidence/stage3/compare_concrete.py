#!/usr/bin/env python3
"""Print trusted-canonical and candidate Python values for one input."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.fizz_buzz


n = int(sys.argv[1])
canonical = load(Path("/reference/canonical.py"), "trusted_for_concrete")
candidate = load(Path("/tmp/audit-work/source/solution.py"), "candidate_for_concrete")
canonical_value = canonical(n)
candidate_value = candidate(n)
print(f"PYTHON_CANONICAL: {canonical_value}")
print(f"PYTHON_CANDIDATE: {candidate_value}")
if canonical_value != candidate_value:
    raise SystemExit(1)

