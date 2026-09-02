#!/usr/bin/env python3
"""Make a claim whose RHS is the exact parsed candidate solution.mpy term."""

from __future__ import annotations

import sys
from pathlib import Path


if len(sys.argv) != 3:
    raise SystemExit("usage: make_pinning_spec.py SOLUTION_MPY OUTPUT_SPEC")

module_term = Path(sys.argv[1]).read_text().strip()
# The translator prints an omitted empty If-else sequence as a blank list item.
# Rule parsing is stricter than program parsing, so spell the same unit term
# explicitly. This is constructor-preserving normalization, not a body change.
old_empty_else = '      Return(UnaryOp("-", Int(1))),\n      )'
explicit_empty_else = '      Return(UnaryOp("-", Int(1))),\n      .Stmts)'
assert module_term.count(old_empty_else) == 1
module_term = module_term.replace(old_empty_else, explicit_empty_else)
spec = f'''requires "verification.k"

module AUDIT-PINNING-SPEC
  imports TRIANGLE-VERIFICATION

  // The module below is inserted from solution.mpy by this reviewer script.
  // Loading it must bind the same exact closure/body used by the call claims.
  claim
    <k> #loadAll({module_term}) => .K </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        .Map
        => "triangle_area" |-> triangleAreaClosure,
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
endmodule
'''
Path(sys.argv[2]).write_text(spec)
