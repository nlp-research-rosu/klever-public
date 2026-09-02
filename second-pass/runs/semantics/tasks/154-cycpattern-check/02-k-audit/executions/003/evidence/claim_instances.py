#!/usr/bin/env python3
"""Ground instances of the candidate's rotationsLoop result equations."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.cycpattern_check


def rotations_loop(a: str, pattern: str, remaining: str) -> bool:
    """Direct executable reading of verification.k's three equations."""
    while remaining:
        if pattern in a:
            return True
        char, remaining = remaining[0], remaining[1:]
        pattern = pattern[1:] + char
    return False


canonical = load_function(Path("/reference/canonical.py"), "claim_canonical")
generated = load_function(Path("/tmp/audit-work/fresh/solution.py"), "claim_solution")

instances = [
    ("hello", "ell"),
    ("abcd", "abd"),
    ("abab", "baa"),
    ("anything", ""),
    ("", ""),
]

mismatches = 0
for a, b in instances:
    claimed = rotations_loop(a, b, b)
    canonical_result = canonical(a, b)
    generated_result = generated(a, b)
    print(
        f"INSTANCE a={a!r} b={b!r} claimed={claimed!r} "
        f"generated={generated_result!r} canonical={canonical_result!r}"
    )
    if claimed != generated_result:
        mismatches += 1

print(f"CLAIM_VS_GENERATED_MISMATCH_COUNT={mismatches}")
raise SystemExit(0 if mismatches == 0 else 1)
