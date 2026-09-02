#!/usr/bin/env python3
"""Run the required trusted Stage 4 preflight and print returned evidence."""

import json
import os
import subprocess
from pathlib import Path

from tools.klean_preflight import check_generation


def run_with_proc_fix(command, *, cwd, timeout):
    environment = os.environ.copy()
    environment["LD_PRELOAD"] = "/audit-output/evidence/proc_exe_shim.so"
    environment["PATH"] = (
        "/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin:"
        "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
    )
    environment["LEAN_NUM_THREADS"] = "1"
    environment["TERM"] = "dumb"
    environment["NO_COLOR"] = "1"
    actual_command = [command[0], "--quiet", *command[1:]]
    try:
        completed = subprocess.run(
            actual_command,
            cwd=cwd,
            timeout=timeout,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            env=environment,
        )
        return completed.returncode, completed.stdout
    except subprocess.TimeoutExpired:
        return 124, f"TIMEOUT after {timeout}s"


result = check_generation(
    Path("/reference/k-proof"),
    Path("/reference/lemma-discovery.json"),
    Path("/reference/klean-generation"),
    toolchain_lock=Path("/reference/klean-toolchain.lock.json"),
    run_command=run_with_proc_fix,
)
print(json.dumps(result, indent=2, sort_keys=True))
