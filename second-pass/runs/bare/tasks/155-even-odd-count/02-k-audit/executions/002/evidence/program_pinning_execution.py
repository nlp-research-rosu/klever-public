#!/usr/bin/env python3
"""Mechanically compare claim-alias and submitted-program first-step states."""

from __future__ import annotations

import subprocess
from pathlib import Path


root = Path("/tmp/audit-work/155-even-odd-count-audit/reconstruction")
definition = "proof-fresh-kompiled"
alias_command = [
    "krun",
    "claim-program.mpy",
    "--definition",
    definition,
    "--parser",
    "/audit-output/evidence/parse_verification_program.sh",
    "-cNUM=123",
    "--depth",
    "1",
]
source_command = [
    "krun",
    "solution.mpy",
    "--definition",
    definition,
    "-cNUM=123",
    "--depth",
    "1",
]


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    print(f"command={' '.join(command)}")
    completed = subprocess.run(
        command,
        cwd=root,
        check=False,
        text=True,
        capture_output=True,
    )
    print(f"exit_status={completed.returncode}")
    print(f"stdout_sha256_input_length={len(completed.stdout)}")
    if completed.stderr:
        print(f"stderr={completed.stderr.rstrip()}")
    return completed


alias = run(alias_command)
source = run(source_command)
same_state = alias.stdout == source.stdout
print(f"first_step_configuration_identity={same_state}")
print("alias_first_step_configuration:")
print(alias.stdout.rstrip())
if alias.returncode or source.returncode or not same_state:
    raise SystemExit(1)
