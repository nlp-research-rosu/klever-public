#!/usr/bin/env python3
"""Concrete substitutions for the two reachability claims."""

from __future__ import annotations

import importlib.util
import math
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.greatest_common_divisor


generated = load(
    Path("/tmp/audit-work/candidate/solution.py"), "generated_witness"
)
canonical = load(
    Path("/tmp/audit-work/trusted/canonical.py"), "canonical_witness"
)

for a, b in ((25, 15), (0, -7), (-7, 0), (0, 0)):
    print(
        f"A={a} B={b} "
        f"generated={generated(a, b)} "
        f"canonical={canonical(a, b)} "
        f"math_gcd={math.gcd(a, b)}"
    )
