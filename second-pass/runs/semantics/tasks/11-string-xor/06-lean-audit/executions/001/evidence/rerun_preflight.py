#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

from tools.klean_preflight import check_generation


def observed_run(command: list[str], *, cwd: Path, timeout: int) -> tuple[int, str]:
    print(f"COMMAND: {' '.join(command)}")
    print(f"CWD: {cwd}")
    result = subprocess.run(
        command,
        cwd=cwd,
        timeout=timeout,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    print(f"EXIT_CODE: {result.returncode}")
    print("BEGIN_COMPLETE_OUTPUT")
    print(result.stdout, end="")
    if result.stdout and not result.stdout.endswith("\n"):
        print()
    print("END_COMPLETE_OUTPUT")
    return result.returncode, result.stdout


result = check_generation(
    Path("/reference/k-proof"),
    Path("/reference/lemma-discovery.json"),
    Path("/reference/klean-generation"),
    toolchain_lock=Path("/reference/klean-toolchain.lock.json"),
    run_command=observed_run,
)
print("RETURNED_EVIDENCE")
print(json.dumps(result, indent=2, sort_keys=True))
