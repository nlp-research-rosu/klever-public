#!/usr/bin/env python3
"""Reviewer-owned constructor-level program-to-claim identity check."""

from __future__ import annotations

import ast
import re
from pathlib import Path


SOURCE = Path("/tmp/audit-work/98-count-upper/solution.py")
REGENERATED = Path("/tmp/audit-work/98-count-upper/solution.regenerated.mpy")
SPEC = Path("/tmp/audit-work/98-count-upper/spec.k")


def compact(text: str) -> str:
    # K/MPY strings in this artifact contain no whitespace, so whitespace
    # erasure is constructor-preserving for this exact generated program.
    return re.sub(r"\s+", "", text)


tree = ast.parse(SOURCE.read_text(encoding="utf-8"))
assert len(tree.body) == 1
function = tree.body[0]
assert isinstance(function, ast.FunctionDef)
assert function.name == "count_upper"
assert [argument.arg for argument in function.args.args] == ["s"]
assert not function.decorator_list
assert len(function.body) == 4
assert [
    type(statement).__name__ for statement in function.body
] == ["Assign", "Assign", "While", "Return"]

translated = compact(REGENERATED.read_text(encoding="utf-8"))
prefix = 'Module(FuncDef("count_upper",Params("s"),'
assert translated.startswith(prefix)
assert translated.endswith("))")
body = translated[len(prefix) : -2]

# The third FuncDef argument is the constructor sequence below. Requiring each
# material source constructor guards against a misleading balanced substring.
for required in (
    'Assign(Name("count"),Int(0))',
    'Assign(Name("remaining"),Name("s"))',
    'While(Name("remaining"),',
    'AugAssign(Name("count"),"+",',
    'Compare(Subscript(Name("remaining"),Int(0)),CmpOp("in",Str("AEIOU")))',
    'Slice(Int(2),NoBound,NoBound)',
    'Return(Name("count"))',
):
    assert required in body, required

spec = compact(SPEC.read_text(encoding="utf-8"))
expected_closure = (
    '"count_upper"|->closureVal(("s",.ParamNames),'
    + body
    + ".Stmts,0)"
)
assert spec.count(expected_closure) == 1

entry_term = (
    '<k>Call(Name("count_upper"),str(CODES:IntSeq))'
    "=>countUpperEven(CODES)</k>"
)
assert spec.count(entry_term) == 1

while_start = body.index("While(") + len("While")
while_end = body.index('Return(Name("count"))')
while_constructor = body[while_start:while_end]
expected_loop_head = "<k>#while" + while_constructor + "=>.K...</k>"
assert spec.count(expected_loop_head) == 1

print("SOURCE_AST_ENTRY=PASS")
print(f"TRANSLATED_BODY_CHARS={len(body)}")
print("ENTRY_CLOSURE_EXACT_CONSTRUCTOR_MATCH=PASS")
print("LOOP_HEAD_AND_BODY_EXACT_CONSTRUCTOR_MATCH=PASS")
print("ENTRY_RESULT_CONSTRAINT=countUpperEven(CODES)")
