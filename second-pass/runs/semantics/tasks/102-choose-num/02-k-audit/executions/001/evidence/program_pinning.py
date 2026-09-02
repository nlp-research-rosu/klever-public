#!/usr/bin/env python3
"""Check that the proof wrapper embeds the submitted translated function body."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path


scratch = Path("/tmp/audit-work/102-choose-num")
solution_text = (scratch / "solution.mpy").read_text()
verification_text = (scratch / "verification.k").read_text()


def compact(text: str) -> str:
    uncommented = "\n".join(line.split("//", 1)[0] for line in text.splitlines())
    return re.sub(r"\s+", "", uncommented)


solution = compact(solution_text)
verification = compact(verification_text)
prefix = 'Module(FuncDef("choose_num",Params("x","y"),'
if not solution.startswith(prefix) or not solution.endswith("))"):
    raise SystemExit("unexpected submitted solution.mpy shape")

# Remove only the outer Module( FuncDef(..., BODY) ) constructors.
body = solution[len(prefix) : -2]
# The translator prints an empty Stmts list as an omitted list argument (`,)`),
# while verification.k spells the same K list unit explicitly as `,.Stmts)`.
body = body.replace(",)", ",.Stmts)")
expected_wrapper_rule = (
    'rule<k>#chooseNum(X:Int,Y:Int)=>Call(closureVal(("x","y"),'
    + body
    + ",0),X,Y)...</k>"
)

wrapper_count = verification.count("rule<k>#chooseNum(")
exact_body_present = expected_wrapper_rule in verification
print(f"submitted_function_body_sha256={hashlib.sha256(body.encode()).hexdigest()}")
print(f"chooseNum_operational_rule_count={wrapper_count}")
print(f"exact_submitted_body_in_wrapper={exact_body_present}")
print("normalization=omitted empty Stmts list is the K unit .Stmts")
print("wrapper_parent_scope=0")
print("wrapper_arguments=(X,Y) bound to submitted parameters=(x,y)")

raise SystemExit(0 if wrapper_count == 1 and exact_body_present else 1)
