#!/usr/bin/env python3
"""Ground witnesses for the FUNCTION-SPEC postcondition."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load_encrypt(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.encrypt


def claimed_encrypt_codes(value: str) -> str:
    return "".join(chr((ord(char) - 97 + 4) % 26 + 97) for char in value)


canonical = load_encrypt("trusted_canonical", Path("/reference/canonical.py"))
candidate = load_encrypt("candidate_solution", Path("/candidate/solution.py"))
inputs = ["", "hi", "wxyz", "abcdefghijklmnopqrstuvwxyz", "A", "aZ-9z", "\u00e9"]

candidate_mismatches = 0
for value in inputs:
    claimed = claimed_encrypt_codes(value)
    generated_result = candidate(value)
    canonical_result = canonical(value)
    print(
        f"input={value!r} codes={[ord(char) for char in value]} "
        f"claimed={claimed!r} generated={generated_result!r} "
        f"canonical={canonical_result!r} "
        f"claim_matches_generated={claimed == generated_result} "
        f"claim_matches_canonical={claimed == canonical_result}"
    )
    candidate_mismatches += claimed != generated_result

print(f"candidate_postcondition_mismatch_count={candidate_mismatches}")
if candidate_mismatches:
    raise SystemExit(1)
