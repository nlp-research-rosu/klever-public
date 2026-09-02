#!/usr/bin/env python3
"""Ground witness showing the fresh postcondition mutation is false."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.get_max_triples


candidate = load_entry("vacuity_candidate", Path("/candidate/solution.py"))
canonical = load_entry("vacuity_canonical", Path("/reference/canonical.py"))
n = 5
actual = candidate(n)
trusted = canonical(n)
mutated_target = trusted + 1
print(
    f"N={n}; precondition={n >= 1}; candidate={actual}; canonical={trusted}; "
    f"mutated_target={mutated_target}"
)
assert n >= 1
assert actual == trusted == 1
assert mutated_target == 2
assert actual != mutated_target
print("FALSE POSTCONDITION WITNESS: PASS")
