#!/usr/bin/env python3
"""Rerun the trusted Stage 5 mechanical gate and preserve full output."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

from tools.klean_final_gate import check_proof_candidate


OUTPUT = Path("/audit-output/evidence")
counter = 0


def recorded_run(
    command: list[str], *, cwd: Path, timeout: int
) -> tuple[int, str]:
    global counter
    counter += 1
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=timeout,
            check=False,
        )
        code = result.returncode
        output = result.stdout
    except subprocess.TimeoutExpired as error:
        code = 124
        output = (
            (error.stdout or "")
            + (error.stderr or "")
            + f"\nTIMEOUT after {timeout}s\n"
        )
    label = "-".join(command)
    log = OUTPUT / f"final-gate-{counter:02d}-{label}.log"
    log.write_text(
        "COMMAND: " + " ".join(command) + "\n"
        + f"CWD: {cwd}\n"
        + f"EXIT_CODE: {code}\n"
        + f"OUTPUT_SHA256: {hashlib.sha256(output.encode()).hexdigest()}\n"
        + "OUTPUT:\n"
        + output
    )
    return code, output


result = check_proof_candidate(
    Path("/reference/klean-generation"),
    Path("/candidate"),
    run_command=recorded_run,
)
(OUTPUT / "final-gate-returned-evidence.json").write_text(
    json.dumps(result, indent=2, sort_keys=True) + "\n"
)
print(json.dumps(result, indent=2, sort_keys=True))
