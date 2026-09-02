#!/usr/bin/env python3
"""Witness that exact decimal rationals do not model CPython float subtraction."""

import importlib.util
from pathlib import Path


def load_entry(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.has_close_elements


canonical = load_entry("trusted_canonical_rounding", Path("/reference/canonical.py"))
candidate = load_entry("submitted_solution_rounding", Path("/tmp/audit-work/source/solution.py"))

numbers = [0.1, 0.3]
threshold = 0.2
distance = abs(numbers[0] - numbers[1])

print(f"numbers={numbers!r}")
print(f"threshold={threshold!r}")
print(f"binary_float_distance={distance!r}")
print(f"distance_less_than_threshold={distance < threshold}")
print(f"canonical={canonical(numbers, threshold)}")
print(f"candidate={candidate(numbers, threshold)}")
