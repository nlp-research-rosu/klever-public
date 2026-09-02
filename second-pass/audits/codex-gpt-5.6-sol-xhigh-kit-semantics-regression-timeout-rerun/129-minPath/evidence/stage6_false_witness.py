#!/usr/bin/env python3
"""Demonstrate that the reviewer-created postcondition mutation is false."""

import importlib.util
import json
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.minPath


grid = [[4, 3], [2, 1]]
k = 5
mutated_expected = [1, 2, 1, 2, 2]
canonical = load(Path("/reference/canonical.py"), "stage6_canonical")(grid, k)
generated = load(
    Path("/tmp/audit-work/reconstruction/solution.py"), "stage6_generated"
)(grid, k)
record = {
    "grid": grid,
    "k": k,
    "mutated_expected": mutated_expected,
    "canonical": canonical,
    "generated": generated,
    "mutation_is_false": canonical == generated and generated != mutated_expected,
}
print(json.dumps(record, sort_keys=True))
raise SystemExit(0 if record["mutation_is_false"] else 1)
