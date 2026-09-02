#!/usr/bin/env python3
"""Generate a claim equating the proof macro with the submitted .mpy AST."""

from pathlib import Path


PROGRAM = Path("/tmp/audit-work/reconstruction/solution.mpy")
SPEC = Path("/tmp/audit-work/reconstruction/program-pin-spec.k")

program_text = PROGRAM.read_text(encoding="utf-8").strip()
SPEC.write_text(
    'requires "verification.k"\n\n'
    "module PROGRAM-PIN-SPEC\n"
    "  imports VERIFICATION\n\n"
    "  claim solutionModule\n"
    f"    => {program_text}\n"
    "endmodule\n",
    encoding="utf-8",
)
print(SPEC)
