#!/usr/bin/env python3
"""Concrete witness showing the fresh postcondition mutation is false."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


def load(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.flip_case


canonical = load(
    "mutation_canonical",
    Path("/tmp/audit-work/27-flip-case/trusted/canonical.py"),
)
submitted = load(
    "mutation_submitted",
    Path("/tmp/audit-work/27-flip-case/candidate/solution.py"),
)

value = ""
mutated_required = "!" + value.swapcase()
result = {
    "input": value,
    "precondition_satisfied": True,
    "canonical_result": canonical(value),
    "submitted_result": submitted(value),
    "mutated_required_result": mutated_required,
    "mutation_is_false": (
        canonical(value) == submitted(value) and submitted(value) != mutated_required
    ),
}
print(json.dumps(result, indent=2, sort_keys=True))
raise SystemExit(0 if result["mutation_is_false"] else 1)
