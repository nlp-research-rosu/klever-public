#!/usr/bin/env python3
"""Exhibit concrete states satisfying the universal K claim's precondition."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Any


def load(path: str, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.triangle_area


canonical = load("/reference/canonical.py", "ground_canonical")
submitted = load("/tmp/audit-work/proof/solution.py", "ground_submitted")

for a, h in [(5, 3), (0, 9), (-3, 6), (10**308, 2)]:
    print(f"A={a} H={h}")
    for label, function in (("canonical", canonical), ("submitted", submitted)):
        try:
            print(f"  {label}={function(a, h)!r}")
        except Exception as err:
            print(f"  {label}=EXCEPTION:{type(err).__name__}:{err}")
    print(f"  formal_post_term=divII({a * h},2)")
