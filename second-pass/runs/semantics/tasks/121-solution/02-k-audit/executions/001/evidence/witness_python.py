#!/usr/bin/env python3
"""Print both Python results for the concrete satisfying K witness."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load_solution(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.solution


values = [5, 8, 7, 1]
canonical = load_solution("witness_canonical", Path("/reference/canonical.py"))
candidate = load_solution(
    "witness_candidate", Path("/tmp/audit-work/121-audit/solution.py")
)
print(f"input={values}")
print(f"canonical_result={canonical(values)}")
print(f"candidate_result={candidate(values)}")
