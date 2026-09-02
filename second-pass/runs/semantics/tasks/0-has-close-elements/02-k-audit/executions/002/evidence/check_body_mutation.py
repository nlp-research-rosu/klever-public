#!/usr/bin/env python3
"""Show the concrete false conclusion exposed by the body-sensitivity mutation."""
from __future__ import annotations

import importlib.util


def load(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.has_close_elements


canonical = load("/tmp/audit-work/case/canonical.py", "canonical_for_mutation")
original = load("/tmp/audit-work/case/solution.py", "original_for_mutation")
mutated = load(
    "/tmp/audit-work/case/solution-body-mutated.py", "mutated_for_mutation"
)

numbers = [0.0, 0.0]
threshold = 1.0
print(f"witness numbers={numbers!r} threshold={threshold!r}")
print(f"canonical={canonical(numbers, threshold)!r}")
print(f"original={original(numbers, threshold)!r}")
print(f"mutated={mutated(numbers, threshold)!r}")
raise SystemExit(
    0
    if canonical(numbers, threshold) is True
    and original(numbers, threshold) is True
    and mutated(numbers, threshold) is False
    else 1
)
