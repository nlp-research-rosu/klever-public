#!/usr/bin/env python3
"""Constructor-level identity and concrete claim-substitution checks."""

from __future__ import annotations

import hashlib
import importlib.util
import re
from pathlib import Path


def compact_k(text: str) -> str:
    text = re.sub(r"//[^\n]*", "", text)
    return re.sub(r"\s+", "", text)


def load(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    mpy_path = Path("/tmp/audit-work/task/solution.mpy")
    verification_path = Path("/tmp/audit-work/task/verification.k")
    spec_path = Path("/tmp/audit-work/task/spec.k")
    mpy = compact_k(mpy_path.read_text())
    verification = compact_k(verification_path.read_text())
    spec = compact_k(spec_path.read_text())

    prefix = 'Module(FuncDef("decimal_to_binary",Params("decimal"),'
    assert mpy.startswith(prefix) and mpy.endswith("))")
    body = mpy[len(prefix):-2]
    assert body.startswith("Return(")

    exact_direct_call = (
        'rule#runDecimalToBinary(N:Int)=>Call(closureVal("decimal",'
        + body
        + ".Stmts,0),N)"
    )
    assert exact_direct_call in verification
    assert verification.count("#runDecimalToBinary") == 2  # declaration and rule LHS
    assert '#runDecimalToBinary(N)=>str(' in spec
    assert "requiresN>=Int0" in spec

    canonical = load("/reference/canonical.py", "pinning_canonical")
    candidate = load("/tmp/audit-work/task/solution.py", "pinning_candidate")
    witnesses = [0, 1, 15, 32, 103, 256]
    print(f"solution_mpy_sha256={hashlib.sha256(mpy_path.read_bytes()).hexdigest()}")
    print(f"verification_sha256={hashlib.sha256(verification_path.read_bytes()).hexdigest()}")
    print(f"normalized_body_sha256={hashlib.sha256(body.encode()).hexdigest()}")
    print('function_binding=decimal_to_binary("decimal")')
    print("constructor_body_match=YES")
    print("singleton_Stmts_normalization=translator body versus body .Stmts")
    print("claim_precondition=N >=Int 0")
    print("satisfying_initial_state=N=0 plus the fully concrete cells in spec.k")
    for value in witnesses:
        canonical_result = canonical.decimal_to_binary(value)
        candidate_result = candidate.decimal_to_binary(value)
        claimed_result = "db" + bin(value)[2:] + "db"
        claimed_codes = [ord(char) for char in claimed_result]
        assert canonical_result == candidate_result == claimed_result
        print(
            f"witness N={value} canonical={canonical_result!r} "
            f"candidate={candidate_result!r} claimed={claimed_result!r} "
            f"codes={claimed_codes}"
        )
    print("PROGRAM_PINNING_OK")


if __name__ == "__main__":
    main()
