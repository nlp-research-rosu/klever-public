#!/usr/bin/env python3
"""Ground witnesses for every candidate entry/loop claim."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


def load(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, Path(path))
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.cycpattern_check


canonical = load(
    "/tmp/audit-work/154-cycpattern-check/reference/canonical.py", "canonical"
)
submitted = load(
    "/tmp/audit-work/154-cycpattern-check/candidate-src/solution.py", "submitted"
)


def cyclic_contains_from(a: str, b: str, index: int) -> bool:
    while index < len(b):
        if b[index:] + b[:index] in a:
            return True
        index += 1
    return False


claims = [
    ("example-abcd-abd", "abcd", "abd", 0),
    ("example-hello-ell", "hello", "ell", 0),
    ("example-whassup-psus", "whassup", "psus", 0),
    ("example-abab-baa", "abab", "baa", 0),
    ("example-efef-eeff", "efef", "eeff", 0),
    ("example-himenss-simen", "himenss", "simen", 0),
    ("boundary-unrotated", "abc", "abc", 0),
    ("boundary-one-character", "x", "x", 0),
    ("boundary-empty-ground", "anything", "", 0),
    ("boundary-empty-symbolic", "abc", "", 0),
    ("loop-invariant", "cab", "abc", 2),
    ("whole-program", "cab", "abc", 0),
]

failures = 0
for name, a, b, index in claims:
    precondition = 0 <= index <= len(b)
    model = cyclic_contains_from(a, b, index)
    submitted_value = (
        submitted(a, b) if index == 0 else cyclic_contains_from(a, b, index)
    )
    canonical_value = canonical(a, b)
    record = {
        "claim": name,
        "witness": {"A": a, "B": b, "I": index},
        "precondition_satisfied": precondition,
        "claimed_K_model_result": model,
        "submitted_or_remaining_loop_result": submitted_value,
        "trusted_canonical_whole_entry_result": canonical_value,
    }
    print(json.dumps(record, ensure_ascii=False, sort_keys=True))
    if not precondition or model != submitted_value:
        failures += 1

print(f"claim_witness_count={len(claims)}")
print(f"K_model_vs_submitted_witness_failures={failures}")
raise SystemExit(1 if failures else 0)
