#!/usr/bin/env python3
"""Rerun the trusted Stage 4 preflight while preserving complete build output."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

from tools.klean_preflight import check_generation


def logged_run(
    command: list[str],
    *,
    cwd: Path,
    timeout: int,
) -> tuple[int, str]:
    print(f"RUN cwd={cwd} timeout={timeout}: {' '.join(command)}", flush=True)
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            timeout=timeout,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        output = result.stdout
        code = result.returncode
    except subprocess.TimeoutExpired as error:
        output = (error.stdout or "") + (error.stderr or "")
        code = 124
    print(f"EXIT {code}", flush=True)
    print("BEGIN COMPLETE COMMAND OUTPUT", flush=True)
    print(output, end="" if output.endswith("\n") or not output else "\n", flush=True)
    print("END COMPLETE COMMAND OUTPUT", flush=True)
    print(f"OUTPUT SHA-256 {hashlib.sha256(output.encode()).hexdigest()}", flush=True)
    return code, output


result = check_generation(
    Path("/reference/k-proof"),
    Path("/reference/lemma-discovery.json"),
    Path("/reference/klean-generation"),
    toolchain_lock=Path("/reference/klean-toolchain.lock.json"),
    run_command=logged_run,
)
print("RETURNED PREFLIGHT EVIDENCE")
print(json.dumps(result, indent=2, sort_keys=True))
