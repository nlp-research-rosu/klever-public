#!/usr/bin/env python3
"""Print both Python outputs for the concrete K-summary witnesses."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

sys.dont_write_bytecode = True


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.factorize


canonical = load(Path("/reference/canonical.py"), "canonical_ground")
generated = load(
    Path("/tmp/audit-work/25-factorize-audit/solution.py"), "generated_ground"
)

for value in (1, 2, 25, 70):
    print(
        f"N={value} PRECONDITION={value >= 1} "
        f"CANONICAL={canonical(value)} GENERATED={generated(value)}"
    )
