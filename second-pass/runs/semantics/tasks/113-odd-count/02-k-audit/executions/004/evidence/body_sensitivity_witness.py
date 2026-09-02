#!/usr/bin/env python3
"""Independent behavior check for the constructor-level body mutation."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


root = Path("/tmp/audit-work/rebuild")
original = load("original_body", root / "solution.py")
mutated = load("mutated_body", root / "solution-body-mutated.py")
input_value = ["3"]
print("mutation=int(digit) % 2  ->  int(digit) % 1")
print(f"input={input_value!r}")
print(f"original_result={original.odd_count(input_value)!r}")
print(f"mutated_result={mutated.odd_count(input_value)!r}")
print("original_expanded_kore_sha256=4a34a58a8e7d19c4b544030f424325af31c054c17538c65418ecc9c365bc8e25")
print("mutated_expanded_kore_sha256=a08de516611f0c3fda8afdc9c41fdeba9d08afcf93539c4f7b6b5e0257881c71")
