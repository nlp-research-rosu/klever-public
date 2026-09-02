#!/usr/bin/env python3
"""Invoke the trusted preflight while repairing only Lean child app-path lookup."""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

from tools.klean_preflight import check_generation


SHIM = "/tmp/audit-work/proc-self-shim.so"


def run_lean(command: list[str], *, cwd: Path, timeout: int) -> tuple[int, str]:
    environment = os.environ.copy()
    environment["LD_PRELOAD"] = SHIM
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            timeout=timeout,
            env=environment,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        return result.returncode, result.stdout
    except subprocess.TimeoutExpired:
        return 124, f"TIMEOUT after {timeout}s"


result = check_generation(
    Path("/reference/k-proof"),
    Path("/reference/lemma-discovery.json"),
    Path("/reference/klean-generation"),
    toolchain_lock=Path("/reference/klean-toolchain.lock.json"),
    run_command=run_lean,
)
serialized = json.dumps(result, indent=2, sort_keys=True) + "\n"
Path("/audit-output/evidence/07-preflight-returned.json").write_text(serialized)
print(serialized, end="", flush=True)
