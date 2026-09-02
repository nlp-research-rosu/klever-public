import json
import os
import subprocess
from pathlib import Path

from tools.klean_preflight import check_generation


TOOLCHAIN = Path(
    "/opt/elan/toolchains/leanprover--lean4---v4.22.0"
)
SHIM = "/tmp/audit-work/lean-proc-self-shim.so"


def sandbox_compatible_run(command, *, cwd, timeout):
    environment = os.environ.copy()
    environment.update(
        {
            "LD_PRELOAD": SHIM,
            "LEAN_SYSROOT": str(TOOLCHAIN),
            "LAKE_HOME": str(TOOLCHAIN / "src/lean/lake"),
            "PATH": f'{TOOLCHAIN / "bin"}:{environment["PATH"]}',
        }
    )
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


result = check_generation(
    Path("/reference/k-proof"),
    Path("/reference/lemma-discovery.json"),
    Path("/reference/klean-generation"),
    toolchain_lock=Path("/reference/klean-toolchain.lock.json"),
    run_command=sandbox_compatible_run,
)
print(json.dumps(result, indent=2, sort_keys=True))
