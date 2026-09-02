#!/usr/bin/env python3
"""Mechanical constructor-stream comparison for the submitted function and macros."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path("/tmp/audit-work/126-is-sorted-audit-003")


def compact(text: str) -> str:
    return re.sub(r"\s+", "", text)


solution = compact((ROOT / "solution.mpy").read_text(encoding="utf-8"))
verification_text = (ROOT / "verification.k").read_text(encoding="utf-8")

solution_prefix = 'Module(FuncDef("is_sorted",Params("lst"),'
assert solution.startswith(solution_prefix), solution[:120]
assert solution.endswith("))")
translated_body = solution[len(solution_prefix) : -2]

closure_match = re.search(
    r"rule\s+isSortedClosure\s*=>\s*closureVal\(\s*"
    r'\("lst",\s*\.ParamNames\),\s*'
    r"(?P<body>.*?)"
    r",\s*0\s*\)\s*\n",
    verification_text,
    flags=re.DOTALL,
)
assert closure_match is not None
closure_body = compact(closure_match.group("body"))


def normalize_stmts(body: str) -> str:
    # The translator prints empty statement-list arguments as whitespace between
    # a comma and ')'; the macro spells them `.Stmts`.  A trailing empty Stmts
    # is likewise explicit only in the macro.  Erase that identity constructor
    # everywhere before comparing the remaining constructor stream.
    return body.replace(".Stmts", "")


translated_normal = normalize_stmts(translated_body)
closure_normal = normalize_stmts(closure_body)

for_prefix = 'For(Name("number"),Name("lst"),'
for_start = translated_normal.index(for_prefix) + len(for_prefix)
depth = 1
cursor = for_start
while depth:
    char = translated_normal[cursor]
    if char == "(":
        depth += 1
    elif char == ")":
        depth -= 1
    cursor += 1
translated_loop_body = translated_normal[for_start : cursor - 1]

loop_match = re.search(
    r"rule\s+isSortedLoopBody\s*=>\s*(?P<body>.*?)"
    r"\n\s*// The exact translated entry point",
    verification_text,
    flags=re.DOTALL,
)
assert loop_match is not None
translated_loop_body = normalize_stmts(translated_loop_body)
macro_loop_body = normalize_stmts(compact(loop_match.group("body")))

# The closure macro intentionally refers to the separately declared loop-body
# macro.  Expand that one macro mechanically before comparing constructors.
closure_expanded = closure_normal.replace("isSortedLoopBody", macro_loop_body)

print("entry_name: is_sorted")
print("parameter_constructor_match:", 'Params("lst")' in solution)
print("closure_parameter_constructor_match:", '("lst",.ParamNames)' in compact(closure_match.group(0)))
print("function_body_token_count:", len(translated_normal))
print("closure_body_token_count_after_macro_expansion:", len(closure_expanded))
print("function_body_constructor_identity:", translated_normal == closure_expanded)
print("loop_body_token_count:", len(translated_loop_body))
print("loop_macro_token_count:", len(macro_loop_body))
print("loop_body_constructor_identity:", translated_loop_body == macro_loop_body)

if translated_normal != closure_expanded:
    for index, (left, right) in enumerate(zip(translated_normal, closure_expanded)):
        if left != right:
            print("first_function_body_difference:", index, left, right)
            break
if translated_loop_body != macro_loop_body:
    for index, (left, right) in enumerate(zip(translated_loop_body, macro_loop_body)):
        if left != right:
            print("first_loop_body_difference:", index, left, right)
            break

raise SystemExit(
    0
    if translated_normal == closure_expanded
    and translated_loop_body == macro_loop_body
    else 1
)
