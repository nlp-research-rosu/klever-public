#!/usr/bin/env python3
"""Parse and compare solution.mpy with the RHS of `solutionProgram`."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys


verification = Path(sys.argv[1])
solution_mpy = Path(sys.argv[2])
definition = Path(sys.argv[3])

source = verification.read_text()
tail = source.split("rule solutionProgram", 1)[1]
rhs = tail.split("=>", 1)[1].rsplit("endmodule", 1)[0].strip()
# `.Stmts` is K rule syntax for the empty list, while the concrete program
# grammar renders the same empty list as an empty field after the comma.
rhs_program_surface = rhs.replace(".Stmts", "")

common = [
    "kast",
    "--definition",
    str(definition),
    "--module",
    "MPY-SYNTAX",
    "--sort",
    "Pgm",
    "--output",
    "kore",
]
submitted = subprocess.run(
    [*common, str(solution_mpy)],
    check=False,
    capture_output=True,
    text=True,
)
defined = subprocess.run(
    [*common, "--expression", rhs_program_surface],
    check=False,
    capture_output=True,
    text=True,
)

print(f"SUBMITTED_COMMAND={[*common, str(solution_mpy)]!r}")
print(f"SUBMITTED_EXIT={submitted.returncode}")
print(f"RHS_COMMAND={[*common, '--expression', '<extracted solutionProgram RHS>']!r}")
print(f"RHS_EXIT={defined.returncode}")
print("RHS_NORMALIZATION=replace explicit .Stmts unit with concrete empty field")
print(f"PARSED_KORE_BYTE_IDENTITY={submitted.stdout == defined.stdout}")
print(f"SUBMITTED_KORE={submitted.stdout.strip()}")
print(f"RHS_KORE={defined.stdout.strip()}")
if submitted.stderr:
    print(f"SUBMITTED_STDERR={submitted.stderr.strip()}")
if defined.stderr:
    print(f"RHS_STDERR={defined.stderr.strip()}")

ok = (
    submitted.returncode == 0
    and defined.returncode == 0
    and submitted.stdout == defined.stdout
)
raise SystemExit(0 if ok else 1)
