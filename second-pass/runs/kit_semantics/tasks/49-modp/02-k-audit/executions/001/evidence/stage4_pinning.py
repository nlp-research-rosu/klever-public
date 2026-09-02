#!/usr/bin/env python3

"""Mechanical constructor-level pinning check for the target claim."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/49-modp")


def compact(path: Path) -> str:
    return re.sub(r"\s+", "", path.read_text())


solution = compact(ROOT / "regenerated-solution.mpy")
spec = compact(ROOT / "spec.k")

module_prefix = 'Module(FuncDef("modp",Params("n","p"),'
module_suffix = "))"
if not solution.startswith(module_prefix) or not solution.endswith(module_suffix):
    raise AssertionError(f"unexpected translated module shape: {solution}")

body = solution[len(module_prefix) : -len(module_suffix)]
binding = f'"modp"|->closureVal(("n","p"),{body},0)'
call = 'Call(Name("modp"),Int(N:Int),Int(P:Int))'
result = "pyMod(2^IntN,P)"

checks = {
    "single_function_definition": solution.count("FuncDef(") == 1,
    "exact_function_name": solution.count('FuncDef("modp"') == 1,
    "exact_translated_body_in_claim_binding": binding in spec,
    "claim_calls_bound_modp_with_symbolic_N_P": call in spec,
    "claim_constrains_result_to_modular_power": f"{call}=>{result}" in spec,
    "claim_uses_complete_configuration": all(
        cell in spec
        for cell in (
            "<env>0</env>",
            "<scopes>",
            "<scopeLoc>1</scopeLoc>",
            "<heap>.Map</heap>",
            "<heapLoc>0</heapLoc>",
            "<stack>.List</stack>",
            "<ret>noRet</ret>",
            "<exc>NoExc</exc>",
            "<exit-code>0</exit-code>",
        )
    ),
}

print(f"translated_module={solution}")
print(f"extracted_body={body}")
print(f"expected_claim_binding={binding}")
for name, passed in checks.items():
    print(f"{name}={passed}")
raise SystemExit(0 if all(checks.values()) else 1)
