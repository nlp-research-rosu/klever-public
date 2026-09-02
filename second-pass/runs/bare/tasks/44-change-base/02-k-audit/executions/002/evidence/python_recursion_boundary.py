#!/usr/bin/env python3
"""Probe the submitted recursive Python at CPython's recursion boundary."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys


ROOT = Path("/tmp/audit-work/change-base-audit-20260726")


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.change_base


canonical = load(ROOT / "reference/canonical.py", "recursion_canonical")
submitted = load(ROOT / "candidate/solution.py", "recursion_submitted")

print(f"python_version={sys.version.split()[0]}")
print(f"recursion_limit={sys.getrecursionlimit()}")

failures = 0
for exponent in [980, 990, 995, 996, 997, 998, 999, 1000, 1001, 1010]:
    x = 2**exponent
    expected = canonical(x, 2)
    try:
        actual = submitted(x, 2)
        outcome = f"return length={len(actual)} match={actual == expected}"
        if actual != expected:
            failures += 1
    except Exception as err:
        outcome = f"raised {type(err).__name__}: {err}"
        failures += 1
    print(
        f"exponent={exponent} x_bit_length={x.bit_length()} "
        f"canonical_length={len(expected)} submitted_outcome={outcome}"
    )

print(f"nonmatching_or_exception_count={failures}")
sys.exit(1 if failures else 0)
