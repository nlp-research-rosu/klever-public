#!/usr/bin/env python3
"""Derive a K constructor-level pinning spec from submitted solution.mpy."""

from __future__ import annotations

import re
from pathlib import Path


WORK = Path("/tmp/audit-work/125-split-words")
translated = (WORK / "solution.mpy").read_text(encoding="utf-8")
match = re.fullmatch(
    r'\s*Module\(\s*FuncDef\("split_words",\s*Params\("txt"\),\s*(.*)\)\s*\)\s*',
    translated,
    flags=re.DOTALL,
)
if match is None:
    raise SystemExit("submitted solution.mpy is not the expected single function")

body = match.group(1)
# The translator prints K collection units as an empty concrete-list slot.
# Claims use the unambiguous constructor-level unit spellings accepted by the
# K rule parser.  These are parser-normalizations only.
empty_args = 'Call(Attribute(Name("txt"), "split"), )'
if body.count(empty_args) != 1:
    raise SystemExit("unexpected no-argument Call shape")
body = body.replace(empty_args, 'Call(Attribute(Name("txt"), "split"), .Exprs)')

empty_else = ",\n      )"
if body.count(empty_else) != 2:
    raise SystemExit("unexpected empty If-else shape")
body = body.replace(empty_else, ",\n      .Stmts)")
spec = f'''requires "verification.k"

module PINNING-SPEC
  imports SPLIT-WORDS-VERIFICATION

  // RHS is mechanically extracted from the submitted translated module.
  claim [body]:
    <k> solutionBody => {body} </k>

  // This also pins the submitted function name, sole parameter, body, and
  // captured module environment used by every entry claim.
  claim [closure]:
    <k> solutionClosure => closureVal("txt", {body}, 0) </k>
endmodule
'''
(WORK / "audit-pinning.k").write_text(spec, encoding="utf-8")
print("extracted_body_bytes=", len(body.encode("utf-8")), sep="")
print("wrote=", WORK / "audit-pinning.k", sep="")
