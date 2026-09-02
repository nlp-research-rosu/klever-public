#!/usr/bin/env python3
"""Independent Python outcomes for the concrete K reconstruction cases."""

import importlib.util
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.triangle_area


canonical = load(Path("/reference/canonical.py"), "canonical_for_k_oracle")
submitted = load(
    Path("/tmp/audit-work/71-triangle-area/solution.py"),
    "submitted_for_k_oracle",
)

cases = [
    ("valid-example", (3, 4, 5)),
    ("valid-rounding", (2, 2, 2)),
    ("valid-near-boundary", (2, 2, 3)),
    ("invalid-first-equality", (1, 2, 3)),
    ("invalid-second-equality", (1, 3, 2)),
    ("invalid-third-equality", (3, 2, 1)),
    ("zero", (0, 0, 0)),
    ("precision-loss-valid", (10**16, 10**16, 1)),
    ("large-finite-inf", (10**100, 10**100, 10**100)),
    ("huge-valid-overflow", (10**400, 10**400, 10**400)),
    ("valid-float", (0.5, 0.5, 0.75)),
]

for label, args in cases:
    for implementation, fn in (("canonical", canonical), ("submitted", submitted)):
        try:
            result = ("return", fn(*args))
        except Exception as err:
            result = ("raise", type(err).__name__, str(err))
        print(f"{label} {implementation} args={args!r} outcome={result!r}")
