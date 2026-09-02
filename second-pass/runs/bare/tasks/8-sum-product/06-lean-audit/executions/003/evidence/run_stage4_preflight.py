#!/usr/bin/env python3
"""Rerun the trusted Stage 4 generation preflight on mounted inputs."""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

from tools.klean_preflight import check_generation


TOOLCHAIN_BIN = Path(
    "/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin"
)
APP_PATH_SHIM = Path("/audit-output/evidence/app_path_shim.so")


def run_with_sandbox_app_path(
    command: list[str], *, cwd: Path, timeout: int
) -> tuple[int, str]:
    """Run pinned Lake while supplying the app path hidden by the sandbox."""

    environment = os.environ.copy()
    environment["PATH"] = (
        f"{TOOLCHAIN_BIN}:{environment.get('PATH', '')}"
    )
    environment["LD_PRELOAD"] = str(APP_PATH_SHIM)
    environment["AUDIT_TOOLCHAIN_BIN"] = str(TOOLCHAIN_BIN)
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            timeout=timeout,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            env=environment,
        )
        return result.returncode, result.stdout
    except subprocess.TimeoutExpired:
        return 124, f"TIMEOUT after {timeout}s"


result = check_generation(
    Path("/reference/k-proof"),
    Path("/reference/lemma-discovery.json"),
    Path("/reference/klean-generation"),
    toolchain_lock=Path("/reference/klean-toolchain.lock.json"),
    run_command=run_with_sandbox_app_path,
)
print("TOOLCHAIN_BIN", TOOLCHAIN_BIN)
print("APP_PATH_SHIM", APP_PATH_SHIM)
print(json.dumps(result, indent=2, sort_keys=True))
