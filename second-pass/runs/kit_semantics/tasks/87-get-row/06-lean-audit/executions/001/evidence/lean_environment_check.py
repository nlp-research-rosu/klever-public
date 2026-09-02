#!/usr/bin/env python3
"""Record the PID-namespace cause and Lean compatibility-shim effect."""

from __future__ import annotations

import json
import os
import subprocess


def run(command, env=None):
    result = subprocess.run(
        command,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    return {"command": command, "exit_code": result.returncode, "output": result.stdout}


def main() -> int:
    status = {}
    for line in open("/proc/self/status"):
        if line.startswith(("Pid:", "NSpid:")):
            key, value = line.split(":", 1)
            status[key] = value.strip()
    inner_pid = os.getpid()
    numeric_proc_path = f"/proc/{inner_pid}/exe"
    try:
        numeric_proc_result = os.readlink(numeric_proc_path)
    except OSError as error:
        numeric_proc_result = f"{type(error).__name__}: {error}"
    shim_env = dict(os.environ)
    shim_env["LD_PRELOAD"] = "/tmp/audit-work/lean_getpid_compat.so"
    result = {
        "os_getpid": inner_pid,
        "proc_status": status,
        "numeric_proc_path": numeric_proc_path,
        "numeric_proc_readlink": numeric_proc_result,
        "proc_self_exe": os.readlink("/proc/self/exe"),
        "lean_without_shim": run(["lean", "--version"]),
        "lean_with_shim": run(["lean", "--version"], env=shim_env),
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
