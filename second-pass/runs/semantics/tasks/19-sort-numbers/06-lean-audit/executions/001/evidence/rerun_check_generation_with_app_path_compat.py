#!/usr/bin/env python3
import hashlib
import json
import os
import subprocess
from pathlib import Path

from tools.klean_preflight import check_generation


LEAN_ROOT = Path("/opt/elan/toolchains/leanprover--lean4---v4.22.0")
COMPAT = Path("/tmp/audit-work/lean-app-path-compat.so")


def run_with_compat(
    command: list[str], *, cwd: Path, timeout: int
) -> tuple[int, str]:
    actual = list(command)
    if actual and actual[0] == "lake":
        actual[0] = str(LEAN_ROOT / "bin" / "lake")
    environment = dict(os.environ)
    environment["LD_PRELOAD"] = str(COMPAT)
    environment["LEAN_SYSROOT"] = str(LEAN_ROOT)
    result = subprocess.run(
        actual,
        cwd=cwd,
        timeout=timeout,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env=environment,
    )
    return result.returncode, result.stdout


print(
    "compatibility_shim_sha256="
    + hashlib.sha256(COMPAT.read_bytes()).hexdigest()
)
result = check_generation(
    Path("/reference/k-proof"),
    Path("/reference/lemma-discovery.json"),
    Path("/reference/klean-generation"),
    toolchain_lock=Path("/reference/klean-toolchain.lock.json"),
    run_command=run_with_compat,
)
print(json.dumps(result, indent=2, sort_keys=True))
