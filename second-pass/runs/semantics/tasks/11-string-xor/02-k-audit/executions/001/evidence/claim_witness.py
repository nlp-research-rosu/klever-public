#!/usr/bin/env python3
"""Ground witnesses for the two K claim preconditions and entry result."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.string_xor


canonical = load_function("trusted_canonical_witness", Path("/reference/canonical.py"))
candidate = load_function(
    "candidate_solution_witness", Path("/tmp/audit-work/reconstruction/solution.py")
)


def k_codes(value: str) -> list[int]:
    return [ord(character) for character in value]


def xor_acc(prefix: list[int], left: list[int], right: list[int]) -> list[int]:
    result = list(prefix)
    for a, b in zip(left, right):
        if a not in (48, 49) or b not in (48, 49):
            raise ValueError("binaryCodes precondition is false")
        result.append(48 if a == b else 49)
    return result


print("loop_claim_witness:")
print("  L=1, SC=.Map, PAR=parent(0)")
print("  ORIGA=iCons(48,.IntSeq), ORIGB=iCons(49,.IntSeq)")
print("  A=iCons(48,.IntSeq), B=iCons(49,.IntSeq)")
print("  P=.IntSeq, X=.IntSeq, Y=.IntSeq")
print("  notBool(L in_keys(SC))=true")
print("  binaryCodes(A)=true, binaryCodes(B)=true")

entry_cases = [("010", "110"), ("", ""), ("10", "1"), ("1", "10")]
for a, b in entry_cases:
    summary_codes = xor_acc([], k_codes(a), k_codes(b))
    summary = "".join(chr(code) for code in summary_codes)
    canonical_result = canonical(a, b)
    candidate_result = candidate(a, b)
    print(
        f"entry a={a!r} b={b!r} "
        f"A_codes={k_codes(a)!r} B_codes={k_codes(b)!r} "
        f"xorAcc_codes={summary_codes!r} xorAcc_string={summary!r} "
        f"canonical={canonical_result!r} candidate={candidate_result!r}"
    )
    assert summary == canonical_result == candidate_result

print("entry_precondition_witness=A=.IntSeq, B=.IntSeq")
print("entry_precondition_binaryCodes=true")
print("all_witness_comparisons_match=true")
