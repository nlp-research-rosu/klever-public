#!/usr/bin/env python3
"""Capture complete stdout/stderr and exit codes for the required fresh build."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path


project = Path("/tmp/audit-work/lean-proof.6L7ByC")
environment = dict(os.environ)
environment.update(
    {
        "LAKE_HOME": (
            "/opt/elan/toolchains/leanprover--lean4---v4.22.0"
        ),
        "LEAN_SYSROOT": (
            "/opt/elan/toolchains/leanprover--lean4---v4.22.0"
        ),
        "LD_PRELOAD": "/tmp/audit-work/proc_self_exe_shim.so",
    }
)

for command in (["lake", "clean"], ["lake", "build"]):
    print("COMMAND:", " ".join(command))
    result = subprocess.run(
        command,
        cwd=project,
        env=environment,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    print("OUTPUT_BEGIN")
    print(result.stdout, end="")
    print("OUTPUT_END")
    print("EXIT_CODE:", result.returncode)
    if result.returncode != 0:
        raise SystemExit(result.returncode)
