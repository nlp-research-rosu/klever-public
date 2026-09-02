#!/usr/bin/env python3
"""Print trusted-canonical and candidate outputs for K concrete-run cases."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


def load(name: str, path: Path):
    module_spec = spec_from_file_location(name, path)
    if module_spec is None or module_spec.loader is None:
        raise RuntimeError(path)
    module = module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    return module.get_odd_collatz


canonical = load("trusted_canonical", Path("/tmp/audit-work/reference/canonical.py"))
candidate = load("candidate_solution", Path("/tmp/audit-work/candidate-src/solution.py"))

for n in (1, 2, 3, 5, 27):
    print(f"n={n} canonical={canonical(n)!r} candidate={candidate(n)!r}")
