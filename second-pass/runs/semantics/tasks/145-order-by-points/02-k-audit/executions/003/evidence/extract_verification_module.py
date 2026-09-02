#!/usr/bin/env python3
"""Extract the complete RHS of `rule solutionModule => ...` by indentation.

The extracted text is parsed with the trusted MPY parser and compared to the
trusted-translator regeneration of solution.mpy.
"""
from pathlib import Path

source = Path("/tmp/audit-work/source/verification.k").read_text(encoding="utf-8")
marker = "  rule solutionModule =>\n"
start = source.index(marker) + len(marker)
end = source.index("\n\n  syntax Map ::=", start)
rhs = source[start:end]
lines = rhs.splitlines()
common_indent = min(len(line) - len(line.lstrip()) for line in lines if line.strip())
normalized = "\n".join(line[common_indent:] for line in lines) + "\n"
print(normalized, end="")
