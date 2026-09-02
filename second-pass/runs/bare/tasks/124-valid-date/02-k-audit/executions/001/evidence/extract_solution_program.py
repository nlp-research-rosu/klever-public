#!/usr/bin/env python3
"""Extract the duplicated solutionProgram RHS for parser-level identity checking."""

from pathlib import Path


source = Path("/tmp/audit-work/candidate-src/verification.k").read_text(encoding="utf-8")
marker = "  rule solutionProgram =>\n"
start = source.index(marker) + len(marker)
end = source.index("\n\n  // An independent", start)
# `.Stmts` is K's internal list-unit spelling used in rules; the concrete
# Program parser represents the same unit as the empty text after a comma.
rhs = source[start:end].strip().replace(".Stmts", "") + "\n"
output = Path("/audit-output/evidence/solutionProgram_rhs.mpy")
output.write_text(rhs, encoding="utf-8")
print(f"wrote {output} ({len(rhs.encode())} bytes)")
