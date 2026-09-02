#!/usr/bin/env python3
"""Document behavior excluded by the formal A < 100 precondition."""

import importlib.util
from pathlib import Path


def load_entry(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_multiply_prime


generated = load_entry(
    "outside_generated", Path("/tmp/audit-work/rebuild/solution.py")
)
canonical = load_entry("outside_canonical", Path("/reference/canonical.py"))

for value in (100, 101, 105, 125):
    print(
        f"A={value} generated={generated(value)} canonical={canonical(value)} "
        "formal_domain=false"
    )
