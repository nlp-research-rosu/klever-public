#!/usr/bin/env python3
"""Print trusted and independent-oracle results for one JSON integer list."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.move_one_ball


def oracle(values: list[int]) -> bool:
    if not values:
        return True
    return any(
        all(
            (values[-shift:] + values[:-shift])[index]
            <= (values[-shift:] + values[:-shift])[index + 1]
            for index in range(len(values) - 1)
        )
        for shift in range(len(values))
    )


values = json.loads(sys.argv[1])
canonical = load(Path("/reference/canonical.py"), "concrete_canonical")
generated = load(Path("/candidate/solution.py"), "concrete_generated")
print(
    json.dumps(
        {
            "input": values,
            "canonical": canonical(values[:]),
            "generated_python": generated(values[:]),
            "rotation_oracle": oracle(values),
        },
        sort_keys=True,
    )
)
