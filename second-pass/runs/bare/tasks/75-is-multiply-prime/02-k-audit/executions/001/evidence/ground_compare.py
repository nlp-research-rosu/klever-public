#!/usr/bin/env python3
"""Compare the concrete witness substitutions in the entry postcondition."""

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
    "ground_generated", Path("/tmp/audit-work/rebuild/solution.py")
)
canonical = load_entry("ground_canonical", Path("/reference/canonical.py"))

for value, claimed_result in ((30, True), (10, False)):
    generated_result = generated(value)
    canonical_result = canonical(value)
    print(
        f"A={value} claimed={claimed_result} generated={generated_result} "
        f"canonical={canonical_result}"
    )
    if not (claimed_result == generated_result == canonical_result):
        raise SystemExit(1)
