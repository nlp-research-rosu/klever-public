#!/usr/bin/env python3
"""Ground witnesses for the entry claim's precondition and result formula."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.even_odd_count


canonical = load_entry(
    "claim_canonical", Path("/tmp/audit-work/trusted/canonical.py")
)
candidate = load_entry(
    "claim_candidate", Path("/tmp/audit-work/candidate-src/solution.py")
)


def k_postcondition_model(number: int) -> tuple[int, int]:
    codes = [ord(character) for character in str(abs(number))]
    even = sum(1 for code in codes if code % 2 == 0)
    odd = sum(1 for code in codes if code % 2 != 0)
    return even, odd


rows = []
for number in [0, -12, 123, -24680, 102030405, 10**50]:
    formal = k_postcondition_model(number)
    expected = canonical(number)
    actual = candidate(number)
    if not (formal == expected == actual):
        raise AssertionError((number, formal, expected, actual))
    rows.append(
        {
            "N": number,
            "precondition_witness": (
                "env=0; exact loaded module+builtins scopes; scopeLoc=1; "
                "empty heap/stack; no return/exception; exit-code=0"
            ),
            "formal_postcondition": formal,
            "canonical": expected,
            "candidate": actual,
        }
    )

print(json.dumps({"witness_count": len(rows), "witnesses": rows}, indent=2))
