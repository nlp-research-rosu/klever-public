#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


sys.dont_write_bytecode = True


def load_entry(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.car_race_collision


canonical = load_entry(
    "trusted_canonical",
    Path("/tmp/audit-work/reconstruction/trusted/canonical.py"),
)
generated = load_entry(
    "submitted_solution",
    Path("/tmp/audit-work/reconstruction/candidate-src/solution.py"),
)

for n, claimed in [(0, 0), (3, 9), (-3, 9)]:
    canonical_result = canonical(n)
    generated_result = generated(n)
    print(
        f"n={n} claimed={claimed} canonical={canonical_result} "
        f"generated={generated_result}"
    )
    if canonical_result != claimed or generated_result != claimed:
        raise SystemExit(1)
print("RESULT: all ground witnesses agree")
