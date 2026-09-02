#!/usr/bin/env python3
"""Mechanically extract the submitted function body and proof-rule RHS."""

from pathlib import Path
import sys


if len(sys.argv) != 6:
    raise SystemExit(
        f"usage: {sys.argv[0]} SOLUTION.mpy VERIFICATION.k "
        "OUT_SOLUTION_BODY OUT_RULE_BODY_RAW OUT_RULE_BODY_PROGRAM"
    )

(
    solution_path,
    verification_path,
    solution_out,
    verification_raw_out,
    verification_program_out,
) = map(Path, sys.argv[1:])
solution = solution_path.read_text()
verification = verification_path.read_text()

needle = 'FuncDef("right_angle_triangle", Params("a", "b", "c"),'
needle_at = solution.index(needle)
open_at = solution.rfind("(", 0, needle_at + len('FuncDef("right_angle_triangle"'))
body_at = needle_at + len(needle)

depth = 0
in_string = False
escaped = False
close_at = None
for index in range(open_at, len(solution)):
    char = solution[index]
    if in_string:
        if escaped:
            escaped = False
        elif char == "\\":
            escaped = True
        elif char == '"':
            in_string = False
        continue
    if char == '"':
        in_string = True
    elif char == "(":
        depth += 1
    elif char == ")":
        depth -= 1
        if depth == 0:
            close_at = index
            break

if close_at is None:
    raise RuntimeError("unbalanced FuncDef constructor")

solution_body = solution[body_at:close_at].strip()

rule_marker = "rule #rightAngleTriangleBody"
rule_at = verification.index(rule_marker)
arrow_at = verification.index("=>", rule_at) + len("=>")
next_decl = verification.index("\n  syntax Val ::=", arrow_at)
rule_body = verification[arrow_at:next_decl].strip()

Path(solution_out).write_text(solution_body + "\n")
Path(verification_raw_out).write_text(rule_body + "\n")
# `.Stmts` is the rule-language spelling of the empty Stmts production.  The
# external program parser spells that same production as an omitted argument.
Path(verification_program_out).write_text(rule_body.replace(".Stmts", "") + "\n")
print(f"solution_body_chars={len(solution_body)}")
print(f"verification_rule_rhs_chars={len(rule_body)}")
