#!/usr/bin/env python3
"""Demonstrate the satisfying input and false postcondition for stage 6."""

import importlib.util
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sum_squares


values = [1, 2, 3]
canonical = load(Path("/reference/canonical.py"), "canonical_vacuity")
generated = load(
    Path("/tmp/audit-work/reconstruction/solution.py"), "generated_vacuity"
)
assert canonical(values) == generated(values) == 14
assert 14 != 15
print("satisfying_input=[1, 2, 3]")
print("canonical_result=14 generated_result=14 mutated_destination=15")
