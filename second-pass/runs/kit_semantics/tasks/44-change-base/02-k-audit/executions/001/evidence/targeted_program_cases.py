#!/usr/bin/env python3
import importlib.util
from pathlib import Path


def load(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.change_base


canonical = load("trusted_canonical_targeted", Path("/reference/canonical.py"))
generated = load(
    "generated_solution_targeted",
    Path("/tmp/audit-work/44-change-base/solution.py"),
)

cases = [
    (8, 3),
    (8, 2),
    (7, 2),
    (0, 2),
    (0, 9),
    (-1, 2),
    (-8, 3),
    (1, 2),
    (2, 2),
    (3, 2),
    (8, 9),
    (9, 9),
    (10, 9),
]
for x, base in cases:
    expected = canonical(x, base)
    actual = generated(x, base)
    print(
        f"x={x} base={base} canonical={expected!r} "
        f"generated={actual!r} equal={expected == actual}"
    )
