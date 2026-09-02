#!/usr/bin/env python3
"""Compare the macro-expanded claim function with submitted solution.mpy."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


WORK = Path("/tmp/audit-work/111-histogram")


def sha(term: object) -> str:
    encoded = json.dumps(term, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


solution = json.loads((WORK / "solution-kast.json").read_text())["term"]
wrapper = json.loads((WORK / "wrapper-kast.json").read_text())["term"]

module_label = "Module(_)_MPY-SYNTAX_Module_Stmts"
cons_label = "___MPY-SYNTAX_Stmts_Stmt_Stmts"
empty_label = '.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}_Stmts'

assert solution["label"]["name"] == module_label
assert wrapper["label"]["name"] == module_label
solution_stmts = solution["args"][0]
wrapper_stmts = wrapper["args"][0]
assert solution_stmts["label"]["name"] == cons_label
assert wrapper_stmts["label"]["name"] == cons_label

solution_function = solution_stmts["args"][0]
wrapper_function = wrapper_stmts["args"][0]
assert solution_stmts["args"][1]["label"]["name"] == empty_label

wrapper_tail = wrapper_stmts["args"][1]
assert wrapper_tail["label"]["name"] == cons_label
assert wrapper_tail["args"][0]["label"]["name"].startswith("Assert(")
assert wrapper_tail["args"][1]["label"]["name"] == empty_label

same = solution_function == wrapper_function
print(f"SOLUTION_FUNCTION_CONSTRUCTOR_SHA256={sha(solution_function)}")
print(f"WRAPPER_FUNCTION_CONSTRUCTOR_SHA256={sha(wrapper_function)}")
print(f"FUNCTION_BINDING_AND_BODY_IDENTICAL={same}")
print("WRAPPER_ADDS_EXACTLY_ONE_TRAILING_ASSERT=True")
if not same:
    raise SystemExit(1)
