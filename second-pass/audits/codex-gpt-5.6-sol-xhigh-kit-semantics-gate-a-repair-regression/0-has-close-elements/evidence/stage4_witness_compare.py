#!/usr/bin/env python3
"""Ground witness for every claim precondition and result."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load_entry(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.has_close_elements


numbers = [1.0, 1.25]
threshold = 0.5
distance = abs(numbers[0] - numbers[1])
precondition = distance < threshold
canonical = load_entry("trusted_canonical_witness", Path("/reference/canonical.py"))
generated = load_entry(
    "audited_generated_witness",
    Path("/tmp/audit-work/reconstruction/solution.py"),
)

canonical_result = canonical(list(numbers), threshold)
generated_result = generated(list(numbers), threshold)
print(f"numbers={numbers!r}")
print(f"threshold={threshold!r}")
print(f"abs(A-B)={distance!r}")
print(f"precondition={precondition!r}")
print(f"canonical_result={canonical_result!r}")
print(f"generated_result={generated_result!r}")
if not precondition or canonical_result is not True or generated_result is not True:
    raise SystemExit(1)
