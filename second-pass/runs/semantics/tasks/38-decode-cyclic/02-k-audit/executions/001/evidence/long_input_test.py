#!/usr/bin/env python3
"""Probe CPython recursion-limit fidelity for the recursive submitted decoder."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path("/tmp/audit-work/38-decode-cyclic")


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load("canonical_long", ROOT / "trusted/canonical.py")
candidate = load("candidate_long", ROOT / "candidate/solution.py")

print(f"python_recursion_limit={sys.getrecursionlimit()}")
divergences = 0
for length in [2800, 2900, 2950, 2980, 2990, 3000, 3010, 3100, 6000]:
    source = "".join(chr(65 + (i % 26)) for i in range(length))
    encoded = canonical.encode_cyclic(source)
    expected = canonical.decode_cyclic(encoded)
    try:
        actual = candidate.decode_cyclic(encoded)
        outcome = f"value(len={len(actual)},matches={actual == expected})"
        if actual != expected:
            divergences += 1
    except Exception as err:  # exact exception is part of the observed behavior
        outcome = f"exception({type(err).__name__}: {err})"
        divergences += 1
    print(
        f"length={length} canonical=value(len={len(expected)}) "
        f"candidate={outcome}"
    )

print(f"material_divergences={divergences}")
sys.exit(1 if divergences else 0)
