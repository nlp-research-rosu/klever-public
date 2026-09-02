#!/usr/bin/env python3
"""Add stable labels to each submitted claim without changing its body."""

from __future__ import annotations

from pathlib import Path


source = Path("/tmp/audit-work/candidate-src/spec.k").read_text(encoding="utf-8")
source = source.replace("module SPEC\n", "module SPEC-LABELLED\n", 1)
source = source.replace("endmodule\n", "endmodule\n", 1)

lines: list[str] = []
claim_count = 0
for line in source.splitlines():
    if line == "  claim <py>":
        claim_count += 1
        line = f"  claim [c{claim_count:02d}]: <py>"
    lines.append(line)

assert claim_count == 11
print("\n".join(lines))
