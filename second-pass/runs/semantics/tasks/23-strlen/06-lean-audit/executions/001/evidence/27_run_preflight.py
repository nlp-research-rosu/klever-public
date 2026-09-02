#!/usr/bin/env python3
"""Run the trusted Stage 4 preflight and expose complete command output."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from tools.klean_preflight import check_generation


def recorded_run(
    command: list[str], *, cwd: Path, timeout: int
) -> tuple[int, str]:
    print(
        "COMMAND:",
        " ".join(command),
        f"(cwd={cwd}, timeout={timeout}s)",
        flush=True,
    )
    try:
        completed = subprocess.run(
            command,
            cwd=cwd,
            timeout=timeout,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        output = completed.stdout
        code = completed.returncode
    except subprocess.TimeoutExpired as error:
        output = (error.stdout or "") + (error.stderr or "")
        code = 124
    print("BEGIN COMMAND OUTPUT", flush=True)
    print(output, end="" if output.endswith("\n") or not output else "\n", flush=True)
    print("END COMMAND OUTPUT", flush=True)
    print(f"EXIT CODE: {code}", flush=True)
    return code, output


result = check_generation(
    Path("/reference/k-proof"),
    Path("/reference/lemma-discovery.json"),
    Path("/reference/klean-generation"),
    toolchain_lock=Path("/reference/klean-toolchain.lock.json"),
    run_command=recorded_run,
)
print("RETURNED PREFLIGHT EVIDENCE")
print(json.dumps(result, indent=2, sort_keys=True))
