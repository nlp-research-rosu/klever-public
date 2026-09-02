#!/usr/bin/env python3
"""Run the trusted proof-candidate gate with complete subprocess output."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess

from tools.klean_final_gate import check_proof_candidate


def recorded_run(
    command: list[str], *, cwd: Path, timeout: int
) -> tuple[int, str]:
    result = subprocess.run(
        command,
        cwd=cwd,
        timeout=timeout,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        errors="replace",
        check=False,
    )
    print(f"PROOF GATE SUBCOMMAND CWD: {cwd}")
    print(f"PROOF GATE SUBCOMMAND: {' '.join(command)}")
    print(f"PROOF GATE SUBCOMMAND EXIT: {result.returncode}")
    print("PROOF GATE SUBCOMMAND OUTPUT:")
    print(result.stdout, end="")
    return result.returncode, result.stdout


evidence = check_proof_candidate(
    Path("/reference/klean-generation"),
    Path("/candidate"),
    run_command=recorded_run,
)
print("CHECK_PROOF_CANDIDATE RETURNED EVIDENCE:")
print(json.dumps(evidence, indent=2, sort_keys=True))
