#!/usr/bin/env python3
"""Run the trusted Stage 4 preflight while emitting complete subprocess output."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from tools.klean_preflight import check_generation


def logged_run(command: list[str], *, cwd: Path, timeout: int) -> tuple[int, str]:
    print(f"COMMAND: {' '.join(command)}")
    print(f"CWD: {cwd}")
    result = subprocess.run(
        command,
        cwd=cwd,
        timeout=timeout,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    print(f"EXIT: {result.returncode}")
    print("OUTPUT-BEGIN")
    print(result.stdout, end="" if result.stdout.endswith("\n") else "\n")
    print("OUTPUT-END")
    return result.returncode, result.stdout


result = check_generation(
    Path("/reference/k-proof"),
    Path("/reference/lemma-discovery.json"),
    Path("/reference/klean-generation"),
    toolchain_lock=Path("/reference/klean-toolchain.lock.json"),
    run_command=logged_run,
)
print("RETURNED-EVIDENCE-BEGIN")
print(json.dumps(result, indent=2, sort_keys=True))
print("RETURNED-EVIDENCE-END")
