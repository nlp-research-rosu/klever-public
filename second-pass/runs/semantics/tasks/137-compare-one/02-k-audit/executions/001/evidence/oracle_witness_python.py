#!/usr/bin/env python3
"""Show the real Python outcomes contradicted by the admitted oracle models."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.compare_one


canonical = load(Path("/tmp/audit-work/trusted/canonical.py"), "oracle_canonical")
generated = load(Path("/tmp/audit-work/candidate-src/solution.py"), "oracle_generated")

for args in ((1.0, 2.0), ("2,3", 0.0)):
    print(
        f"INPUT={args!r} CANONICAL={canonical(*args)!r} "
        f"GENERATED={generated(*args)!r}"
    )
