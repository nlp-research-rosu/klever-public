#!/usr/bin/env python3
"""Rerun trusted Stage 4 check_generation and preserve its command output."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

from tools.klean_preflight import check_generation


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
    log = OUTPUT / f"preflight-{counter:02d}-{label}.log"
    log.write_text(
        "COMMAND: " + " ".join(command) + "\n"
        + f"CWD: {cwd}\n"
        + f"EXIT_CODE: {code}\n"
        + f"OUTPUT_SHA256: {hashlib.sha256(output.encode()).hexdigest()}\n"
        + "OUTPUT:\n"
        + output
    )
    return code, output


result = check_generation(
    Path("/reference/k-proof"),
    Path("/reference/lemma-discovery.json"),
    Path("/reference/klean-generation"),
    toolchain_lock=Path("/reference/klean-toolchain.lock.json"),
    run_command=recorded_run,
)
(OUTPUT / "preflight-returned-evidence.json").write_text(
    json.dumps(result, indent=2, sort_keys=True) + "\n"
)
print(json.dumps(result, indent=2, sort_keys=True))
