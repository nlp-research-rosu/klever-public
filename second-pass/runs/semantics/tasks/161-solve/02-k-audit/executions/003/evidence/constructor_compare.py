#!/usr/bin/env python3
"""Generate a K claim comparing solutionModule() to trusted regeneration."""

import subprocess
from pathlib import Path


root = Path("/tmp/audit-work/161-solve")
module_term = subprocess.run(
    [
        "kast",
        "--definition",
        "audit-verification-kompiled",
        "--sort",
        "Module",
        "regenerated-solution.mpy",
        "--output",
        "pretty",
    ],
    cwd=root,
    check=True,
    text=True,
    stdout=subprocess.PIPE,
).stdout.strip()
spec = f'''requires "/tmp/audit-work/161-solve/verification.k"

module CONSTRUCTOR-COMPARE
  imports VERIFICATION

  claim [trusted-regeneration-equals-proof-module]:
    <k> solutionModule() => {module_term} </k>
endmodule
'''
Path("/audit-output/evidence/constructor-compare-spec.k").write_text(spec)
print(spec)
