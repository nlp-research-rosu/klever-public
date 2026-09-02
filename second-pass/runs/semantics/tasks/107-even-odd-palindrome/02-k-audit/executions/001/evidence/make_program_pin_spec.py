#!/usr/bin/env python3
"""Build an audit claim equating the proof's program macro to trusted translation."""

from pathlib import Path


scratch = Path("/tmp/audit-work/reconstruction")
translated = Path("/audit-output/evidence/regenerated-solution.mpy").read_text().rstrip()
indented = "\n".join("      " + line for line in translated.splitlines())

rendered = f'''requires "verification.k"

module SPEC-PROGRAM-PIN
  imports VERIFICATION

  claim
    <k>
      solutionModule
      =>
{indented}
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

endmodule
'''

(scratch / "spec-program-pin.k").write_text(rendered)
Path("/audit-output/evidence/spec-program-pin.k").write_text(rendered)
