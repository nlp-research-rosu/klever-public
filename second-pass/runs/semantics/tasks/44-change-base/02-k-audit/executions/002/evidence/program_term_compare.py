#!/usr/bin/env python3
"""Mechanically compare the translated module with verification.k constructors."""

from __future__ import annotations

import re
import sys
from pathlib import Path


WORK = Path("/tmp/audit-work/44-change-base")


def compact(text: str) -> str:
    return re.sub(r"\s+", "", text)


mpy = compact((WORK / "solution.mpy").read_text())
verification = (WORK / "verification.k").read_text()

body_match = re.search(
    r"rule\s+changeBaseBody\s*=>\s*(.*?)\n\s*syntax\s+Module\s*::=",
    verification,
    re.S,
)
module_match = re.search(
    r"rule\s+solutionModule\s*=>\s*(.*?)\n\s*syntax\s+Val\s*::=",
    verification,
    re.S,
)
closure_match = re.search(
    r"rule\s+changeBaseClosure\s*=>\s*(.*?)\n\s*//\s*Big-endian",
    verification,
    re.S,
)
if body_match is None or module_match is None or closure_match is None:
    raise RuntimeError("could not locate verification constructor definitions")

# The translator prints an absent else branch as an empty constructor argument.
# In K, the same empty Stmts value is written explicitly as `.Stmts`.
body = compact(body_match.group(1)).replace(".Stmts", "")
expanded_module = f'Module(FuncDef("change_base",Params("x","base"),{body}))'
declared_module = compact(module_match.group(1))
declared_closure = compact(closure_match.group(1))

print(f"TRANSLATED_MODULE_LENGTH={len(mpy)}")
print(f"EXPANDED_CLAIM_MODULE_LENGTH={len(expanded_module)}")
print(f"BODY_EXPANSION_MATCH={str(mpy == expanded_module).lower()}")
print(
    "SOLUTION_MODULE_BINDING_MATCH=",
    str(
        declared_module
        == 'Module(FuncDef("change_base",Params("x","base"),changeBaseBody))'
    ).lower(),
    sep="",
)
print(
    "CLOSURE_BINDING_MATCH=",
    str(
        declared_closure
        == 'closureVal(("x","base",.ParamNames),changeBaseBody,0)'
    ).lower(),
    sep="",
)
if (
    mpy != expanded_module
    or declared_module
    != 'Module(FuncDef("change_base",Params("x","base"),changeBaseBody))'
    or declared_closure
    != 'closureVal(("x","base",.ParamNames),changeBaseBody,0)'
):
    print("TRANSLATED:", mpy)
    print("EXPANDED:", expanded_module)
    sys.exit(1)
