#!/usr/bin/env python3
"""Print trusted-canonical and candidate results for Stage 3 K inputs."""

import importlib.util
from pathlib import Path


ROOT = Path("/tmp/audit-work/reconstruction-8-sum-product")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sum_product


canonical = load("stage3_canonical", ROOT / "reference/canonical.py")
candidate = load("stage3_candidate", ROOT / "candidate/solution.py")
for values in (
    [],
    [7],
    [-7],
    [1, 2, 3, 4],
    [-2, 0, 5],
    [10**12, -3, 17],
):
    print(values, canonical(list(values)), candidate(list(values)))
