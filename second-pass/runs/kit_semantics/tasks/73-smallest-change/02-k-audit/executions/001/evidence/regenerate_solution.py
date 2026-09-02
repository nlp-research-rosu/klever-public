#!/usr/bin/env python3
"""Regenerate solution.mpy with the trusted translator and compare bytes."""

from __future__ import annotations

import subprocess
from pathlib import Path


translator = Path("/reference/py2mpy.py")
solution_py = Path("/candidate/solution.py")
submitted = Path("/candidate/solution.mpy")
regenerated = Path("/tmp/audit-work/regenerated-solution.mpy")

command = ["python3", str(translator), str(solution_py)]
print("COMMAND:", " ".join(command), ">", regenerated)
result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
regenerated.write_bytes(result.stdout)
print(f"TRANSLATOR_EXIT_STATUS: {result.returncode}")
if result.stderr:
    print("TRANSLATOR_STDERR:")
    print(result.stderr.decode(errors="replace"))
same = result.returncode == 0 and result.stdout == submitted.read_bytes()
print(f"SUBMITTED_BYTES: {submitted.stat().st_size}")
print(f"REGENERATED_BYTES: {len(result.stdout)}")
print(f"BYTE_IDENTICAL: {same}")
raise SystemExit(0 if same else 1)
