#!/usr/bin/env python3
"""Run and print the complete output of the mandated fresh Lean build."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


project = Path("/tmp/audit-work/68-pluck-proof-audit-001")
for command in (["lake", "clean"], ["lake", "build"]):
    print(f"$ (cd {project} && {' '.join(command)})", flush=True)
    result = subprocess.run(
        command,
        cwd=project,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    print(result.stdout, end="" if result.stdout.endswith("\n") else "\n")
    print(f"EXIT_CODE: {result.returncode}", flush=True)
    if result.returncode != 0:
        sys.exit(result.returncode)
