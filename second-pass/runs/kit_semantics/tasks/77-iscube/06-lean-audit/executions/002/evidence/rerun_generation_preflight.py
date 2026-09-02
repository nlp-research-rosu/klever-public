#!/usr/bin/env python3
"""Call the trusted generation checker while exposing complete subprocess output."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess

from tools.klean_preflight import check_generation


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
    print(f"PREFLIGHT SUBCOMMAND CWD: {cwd}")
    print(f"PREFLIGHT SUBCOMMAND: {' '.join(command)}")
    print(f"PREFLIGHT SUBCOMMAND EXIT: {result.returncode}")
    print("PREFLIGHT SUBCOMMAND OUTPUT:")
    print(result.stdout, end="")
    return result.returncode, result.stdout


evidence = check_generation(
    Path("/reference/k-proof"),
    Path("/reference/lemma-discovery.json"),
    Path("/reference/klean-generation"),
    toolchain_lock=Path("/reference/klean-toolchain.lock.json"),
    run_command=recorded_run,
)
print("CHECK_GENERATION RETURNED EVIDENCE:")
print(json.dumps(evidence, indent=2, sort_keys=True))
