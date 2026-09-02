#!/usr/bin/env python3
"""Extract the claimed program term and make concrete adequacy witnesses."""

from __future__ import annotations

import pathlib


WORK = pathlib.Path("/tmp/audit-work/reconstruction")
spec = (WORK / "spec.k").read_text()

load_start = spec.index("#loadAll(") + len("#loadAll(")
module_start = spec.index("Module(", load_start)
if spec[load_start:module_start].strip():
    raise RuntimeError("unexpected material between #loadAll( and Module(")

depth = 0
module_end = None
for offset, char in enumerate(spec[module_start:], module_start):
    if char == "(":
        depth += 1
    elif char == ")":
        depth -= 1
        if depth == 0:
            module_end = offset + 1
            break
if module_end is None:
    raise RuntimeError("unterminated Module term in spec.k")

module_term = spec[module_start:module_end]
(WORK / "spec-module-extracted.mpy").write_text(module_term + "\n")
program_syntax_module_term = module_term.replace(" .Stmts", "")
(WORK / "spec-module-extracted-program-syntax.mpy").write_text(
    program_syntax_module_term + "\n"
)

ground_program = spec
ground_program = ground_program.replace("module SPEC", "module STAGE4-GROUND-PROGRAM", 1)
ground_program = ground_program.replace("claim [solution]:", "claim [example-one-program]:", 1)
ground_program = ground_program.replace(
    "list(vCons(HEAD:Val, TAIL:ValSeq))",
    "list(vCons(5, vCons(8, vCons(7, vCons(1, .ValSeq)))))",
    1,
)
ground_program = ground_program.replace(
    "oddAtEvenSum(vCons(HEAD, TAIL), 0)",
    "12",
    1,
)
ground_program = ground_program.replace(
    "    requires allInts(vCons(HEAD, TAIL))\n",
    "",
    1,
)
ground_program = ground_program.replace("endmodule", "endmodule", 1)

summary_module = """

module STAGE4-GROUND-SUMMARIES
  imports VERIFICATION

  claim [example-one-summary]:
    <k>
      oddAtEvenSum(vCons(5, vCons(8, vCons(7, vCons(1, .ValSeq)))), 0)
      => 12
    </k>

  claim [example-two-summary]:
    <k>
      oddAtEvenSum(vCons(3, vCons(3, vCons(3, vCons(3, vCons(3, .ValSeq))))), 0)
      => 9
    </k>

  claim [example-three-summary]:
    <k>
      oddAtEvenSum(vCons(30, vCons(13, vCons(24, vCons(321, .ValSeq)))), 0)
      => 0
    </k>

  claim [negative-boundary-summary]:
    <k>
      oddAtEvenSum(vCons(-3, vCons(-2, vCons(-1, vCons(0, vCons(1, .ValSeq))))), 0)
      => -3
    </k>

  claim [precondition-witness]:
    <k>
      allInts(vCons(5, vCons(8, vCons(7, vCons(1, .ValSeq)))))
      => true
    </k>
endmodule
"""

(WORK / "stage4-ground.k").write_text(ground_program + summary_module)
print("extracted_term", WORK / "spec-module-extracted.mpy")
print(
    "program_syntax_extracted_term",
    WORK / "spec-module-extracted-program-syntax.mpy",
)
print("extracted_chars", len(module_term))
print("ground_spec", WORK / "stage4-ground.k")
