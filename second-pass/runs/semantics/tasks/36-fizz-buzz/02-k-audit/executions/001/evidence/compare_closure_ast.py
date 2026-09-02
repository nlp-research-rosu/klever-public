#!/usr/bin/env python3
"""Check whether the manually declared proof closure currently duplicates solution.mpy."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path


def compact(path: Path) -> str:
    return re.sub(r"\s+", "", path.read_text())


solution = compact(Path("/tmp/audit-work/fizz-buzz-audit/solution.mpy"))
verification = compact(Path("/tmp/audit-work/fizz-buzz-audit/verification.k"))

solution_match = re.fullmatch(
    r'Module\(FuncDef\("fizz_buzz",Params\("n"\),(.*)\)\)', solution
)
closure_match = re.search(
    r'ruleFIZZ-BUZZ-CLOSURE=>closureVal\("n",(.*),0\)endmodule$',
    verification,
)
inner_match = re.search(
    r'ruleINNER-BODY=>(.*?)syntaxStmts::="OUTER-BODY"\[macro\]',
    verification,
)
outer_match = re.search(
    r'ruleOUTER-BODY=>(.*?)syntaxStmt::="FIZZ-BUZZ-DEF"\[macro\]',
    verification,
)
if (
    solution_match is None
    or closure_match is None
    or inner_match is None
    or outer_match is None
):
    print("parse_match=False")
    raise SystemExit(2)

solution_body = solution_match.group(1)
closure_body = closure_match.group(1)
inner_body = inner_match.group(1)
outer_body = outer_match.group(1).replace("INNER-BODY", inner_body)
expanded_closure_body = closure_body.replace("OUTER-BODY", outer_body)
# The submitted pretty-printed MPY omits empty list units, whereas the macro
# spells `.Stmts` explicitly to make macro parsing unambiguous.
expanded_closure_body = expanded_closure_body.replace(".Stmts", "")
print(f"solution_body_sha256={hashlib.sha256(solution_body.encode()).hexdigest()}")
print(
    "expanded_closure_body_sha256="
    f"{hashlib.sha256(expanded_closure_body.encode()).hexdigest()}"
)
print(f"current_body_identity={solution_body == expanded_closure_body}")
print("dependency_link=none (comparison is reviewer-side only)")
raise SystemExit(0 if solution_body == expanded_closure_body else 1)
