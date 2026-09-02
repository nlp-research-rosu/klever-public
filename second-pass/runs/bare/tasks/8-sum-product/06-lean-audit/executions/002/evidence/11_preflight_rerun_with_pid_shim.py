#!/usr/bin/env python3
import json
import os
import subprocess
from pathlib import Path

from tools.klean_preflight import check_generation

command_evidence = []


def run_with_pid_shim(command, *, cwd, timeout):
    environment = os.environ.copy()
    environment["LD_PRELOAD"] = "/tmp/audit-work/libouterpid.so"
    try:
        completed = subprocess.run(
            command,
            cwd=cwd,
            env=environment,
            timeout=timeout,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        code, output = completed.returncode, completed.stdout
    except subprocess.TimeoutExpired:
        code, output = 124, f"TIMEOUT after {timeout}s"
    command_evidence.append(
        {
            "command": command,
            "cwd": str(cwd),
            "exit_code": code,
            "complete_output": output,
        }
    )
    return code, output


result = check_generation(
    Path("/reference/k-proof"),
    Path("/reference/lemma-discovery.json"),
    Path("/reference/klean-generation"),
    toolchain_lock=Path("/reference/klean-toolchain.lock.json"),
    run_command=run_with_pid_shim,
)
print(
    json.dumps(
        {
            "command_evidence": command_evidence,
            "returned_evidence": result,
        },
        indent=2,
        sort_keys=True,
    )
)
