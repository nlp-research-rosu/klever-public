#!/usr/bin/env python3
"""Generate a K equality claim from the exact scratch `solution.mpy` bytes."""

from __future__ import annotations

from pathlib import Path


SOURCE = Path("/tmp/audit-work/152-compare/solution.mpy")
SCRATCH_OUTPUT = Path("/tmp/audit-work/152-compare/pinning-spec.k")
EVIDENCE_OUTPUT = Path("/audit-output/evidence/pinning-spec.k")

program = SOURCE.read_text()
# The external program parser accepts empty concrete lists as `()`. Inside a K
# claim, the same parsed list terms are written with their generated units.
program = program.replace("ListExpr()", "ListExpr(.Exprs)")
program = program.replace(",\n      )", ",\n      .Stmts)")
spec = (
    'requires "verification.k"\n\n'
    "module PINNING-SPEC\n"
    "  imports VERIFICATION\n\n"
    "  claim <k> solutionProgram =>\n"
    + "\n".join(f"    {line}" for line in program.splitlines())
    + "\n        </k>\n"
    "endmodule\n"
)
SCRATCH_OUTPUT.write_text(spec)
EVIDENCE_OUTPUT.write_text(spec)
print(f"SOURCE: {SOURCE}")
print(f"SCRATCH_OUTPUT: {SCRATCH_OUTPUT}")
print(f"EVIDENCE_OUTPUT: {EVIDENCE_OUTPUT}")
print(f"PROGRAM_BYTES: {len(SOURCE.read_bytes())}")
