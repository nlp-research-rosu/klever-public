#!/usr/bin/env python3
"""Generate an auxiliary claim directly from the submitted solution.mpy bytes."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys


DEFAULT_SOURCE = Path("/tmp/audit-work/124-valid-date/solution.mpy")
DEFAULT_DESTINATION = Path(
    "/tmp/audit-work/124-valid-date/audit-pinning-spec.k"
)
DEFINITION = Path(
    "/tmp/audit-work/124-valid-date/audit-verification-kompiled"
)


def main() -> None:
    source = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_SOURCE
    destination = (
        Path(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_DESTINATION
    )
    parsed = subprocess.run(
        [
            "kast",
            str(source),
            "--definition",
            str(DEFINITION),
            "--module",
            "MPY-SYNTAX",
            "--sort",
            "Module",
            "--output",
            "pretty",
        ],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    module_term = parsed.stdout.strip()
    indented = "\n".join("          " + line for line in module_term.splitlines())
    spec = f'''requires "verification.k"

module AUDIT-PINNING-SPEC
  imports VERIFICATION

  // SOURCE_TERM_SHA256 is recorded by the audit's byte-identity evidence.
  claim [module-load-pins-closure]:
    <k> #loadAll(
{indented}
        ) => .K
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map => "valid_date" |-> validDateClosure, parent(-1))
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
    destination.write_text(spec, encoding="utf-8")
    print(f"source={source}")
    print(f"destination={destination}")


if __name__ == "__main__":
    main()
