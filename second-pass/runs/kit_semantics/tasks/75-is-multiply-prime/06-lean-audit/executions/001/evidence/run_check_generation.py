#!/usr/bin/env python3
import json
import os
import subprocess
from pathlib import Path

from tools.klean_preflight import check_generation

TOOLCHAIN = Path("/opt/elan/toolchains/leanprover--lean4---v4.22.0")


def run_pinned(command: list[str], *, cwd: Path, timeout: int):
    actual = [str(TOOLCHAIN / "bin" / "lake"), *command[1:]]
    environment = dict(os.environ)
    environment.update(
        {
            "ELAN_HOME": "/opt/elan",
            "LEAN_SYSROOT": str(TOOLCHAIN),
            "LEAN": str(TOOLCHAIN / "bin" / "lean"),
            "LAKE_HOME": str(TOOLCHAIN),
            "LAKE_OVERRIDE_LEAN": "true",
            "LD_PRELOAD": "/tmp/audit-work/proc_exe_compat.so",
        }
    )
    print(f"RUN cwd={cwd} timeout={timeout}: {' '.join(actual)}")
    try:
        completed = subprocess.run(
            actual,
            cwd=cwd,
            timeout=timeout,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            env=environment,
        )
        print(completed.stdout, end="")
        print(f"EXIT {completed.returncode}")
        return completed.returncode, completed.stdout
    except subprocess.TimeoutExpired as error:
        output = error.stdout or ""
        print(output, end="")
        print(f"TIMEOUT after {timeout}s")
        return 124, f"{output}TIMEOUT after {timeout}s"


print(f"LD_PRELOAD={os.environ.get('LD_PRELOAD')}")
result = check_generation(
    Path("/reference/k-proof"),
    Path("/reference/lemma-discovery.json"),
    Path("/reference/klean-generation"),
    toolchain_lock=Path("/reference/klean-toolchain.lock.json"),
    run_command=run_pinned,
)
print(json.dumps(result, sort_keys=True, indent=2))
