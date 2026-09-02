#!/usr/bin/env python3
"""Make a K claim that compares solutionProgram with the regenerated .mpy term."""

from pathlib import Path


program = Path("/audit-output/evidence/regenerated-solution.mpy").read_text(encoding="utf-8")
spec = f'''requires "/tmp/audit-work/candidate-src/verification.k"

module AUDIT-PROGRAM-IDENTITY
  imports VALID-DATE-VERIFICATION

  claim <k> solutionProgram => {program.rstrip()} </k>
endmodule
'''
Path("/audit-output/evidence/program_identity.k").write_text(spec, encoding="utf-8")
print("wrote /audit-output/evidence/program_identity.k")
