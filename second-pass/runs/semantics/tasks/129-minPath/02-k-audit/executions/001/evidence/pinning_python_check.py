#!/usr/bin/env python3
"""Print concrete satisfying instances for every entry claim."""

from __future__ import annotations

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


generated = load(Path("/tmp/audit-work/129-minPath-audit/solution.py"), "pin_generated")
canonical = load(
    Path("/tmp/audit-work/129-minPath-audit/trusted/canonical.py"), "pin_canonical"
)

instances = [
    {
        "claim": "example-top-left",
        "grid": [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
        "k": 3,
        "claimed": [1, 2, 1],
    },
    {
        "claim": "example-interior",
        "grid": [[5, 9, 3], [4, 1, 6], [7, 8, 2]],
        "k": 1,
        "claimed": [1],
    },
    {
        "claim": "symbolic-2x2",
        "substitution": {"A": 1, "B": 2, "C": 3, "D": 4},
        "grid": [[1, 2], [3, 4]],
        "k": 4,
        "claimed": [1, 2, 1, 2],
    },
]

for instance in instances:
    grid = instance["grid"]
    k = instance["k"]
    instance["generated"] = generated(grid, k)
    instance["canonical"] = canonical(grid, k)
    instance["all_equal"] = (
        instance["claimed"] == instance["generated"] == instance["canonical"]
    )

print(json.dumps(instances, indent=2, sort_keys=True))
raise SystemExit(0 if all(instance["all_equal"] for instance in instances) else 1)
