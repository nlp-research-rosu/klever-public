#!/usr/bin/env python3
"""Run one integer case against both scratch-copied Python implementations."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


def load_entry(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_prime


n = int(sys.argv[1])
canonical = load_entry(
    "trusted_canonical_case", Path("/tmp/audit-work/trusted/canonical.py")
)
generated = load_entry(
    "submitted_generated_case", Path("/tmp/audit-work/candidate-src/solution.py")
)
left = canonical(n)
right = generated(n)
print(json.dumps({"input": n, "canonical": left, "generated": right}))
raise SystemExit(0 if left == right else 1)
