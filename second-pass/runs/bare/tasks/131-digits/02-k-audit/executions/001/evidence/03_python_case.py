#!/usr/bin/env python3
"""Run both independently loaded Python entry points for one integer."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.digits


n = int(sys.argv[1])
canonical = load(Path("/reference/canonical.py"), "oracle_case")
generated = load(
    Path("/tmp/audit-work/131-digits/solution.py"), "generated_case"
)
expected = canonical(n)
actual = generated(n)
print(f"input={n}")
print(f"canonical={expected}")
print(f"generated_python={actual}")
print(f"expected={expected}")
if actual != expected:
    raise SystemExit(1)
