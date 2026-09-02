import json
import os
import subprocess
from pathlib import Path

from tools.klean_preflight import check_generation


LEAN_ROOT = Path(
    "/opt/elan/toolchains/leanprover--lean4---v4.22.0"
)
PROC_FIX = "/tmp/audit-work/proc_self_readlink_fix.so"


def run_pinned(command, *, cwd, timeout):
    actual = [str(LEAN_ROOT / "bin" / "lake"), *command[1:]]
    environment = os.environ.copy()
    environment["PATH"] = (
        f"{LEAN_ROOT / 'bin'}:/usr/local/bin:/usr/bin:/bin"
    )
    environment["LD_PRELOAD"] = PROC_FIX
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


result = check_generation(
    Path("/reference/k-proof"),
    Path("/reference/lemma-discovery.json"),
    Path("/reference/klean-generation"),
    toolchain_lock=Path("/reference/klean-toolchain.lock.json"),
    run_command=run_pinned,
)
print(json.dumps(result, indent=2, sort_keys=True))
