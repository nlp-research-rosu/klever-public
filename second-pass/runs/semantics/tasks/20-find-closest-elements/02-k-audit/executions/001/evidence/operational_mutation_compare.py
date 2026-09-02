#!/usr/bin/env python3
"""Concrete witness for the loop-body sensitivity mutation."""

import importlib.util
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.find_closest_elements


values = [1.0, 10.0, 2.0]
canonical = load(Path("/reference/canonical.py"), "opmut_canonical")
mutated = load(
    Path("/audit-output/evidence/operational_mutation_witness.py"),
    "opmut_program",
)
expected = canonical(list(values))
actual = mutated(list(values))
print(f"input={values!r}")
print(f"trusted_canonical={expected!r}")
print(f"mutated_fixed_execution={actual!r}")
print(f"material_divergence={actual != expected}")
raise SystemExit(0 if actual != expected else 1)
