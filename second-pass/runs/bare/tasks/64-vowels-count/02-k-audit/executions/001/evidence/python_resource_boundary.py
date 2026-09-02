#!/usr/bin/env python3
"""Record the implementation difference caused by CPython recursion limits."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.vowels_count


def outcome(fn, s: str):
    try:
        return ("value", fn(s))
    except Exception as exc:
        return ("exception", type(exc).__name__, str(exc))


canonical = load_function("trusted_canonical_long", Path("/reference/canonical.py"))
generated = load_function(
    "scratch_generated_long", Path("/tmp/audit-work/candidate-src/solution.py")
)

print(f"recursion_limit={sys.getrecursionlimit()}")
for length in [0, 1, 10, 500, 900, 950, 975, 990, 1000, 1100, 2000]:
    s = "b" * length
    print(
        f"length={length} canonical={outcome(canonical, s)!r} "
        f"generated={outcome(generated, s)!r}"
    )
