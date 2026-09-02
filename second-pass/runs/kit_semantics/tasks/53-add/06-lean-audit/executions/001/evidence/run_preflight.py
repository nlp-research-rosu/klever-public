#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

from tools.klean_preflight import check_generation


def run_and_echo(command: list[str], *, cwd: Path, timeout: int) -> tuple[int, str]:
    print(f"PREFLIGHT COMMAND: {command!r}")
    print(f"PREFLIGHT CWD: {cwd}")
    result = subprocess.run(
        command,
        cwd=cwd,
        timeout=timeout,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    print("PREFLIGHT COMMAND OUTPUT BEGIN")
    print(result.stdout, end="")
    print("PREFLIGHT COMMAND OUTPUT END")
    print(f"PREFLIGHT COMMAND EXIT: {result.returncode}")
    return result.returncode, result.stdout


result = check_generation(
    Path("/reference/k-proof"),
    Path("/reference/lemma-discovery.json"),
    Path("/reference/klean-generation"),
    toolchain_lock=Path("/reference/klean-toolchain.lock.json"),
    run_command=run_and_echo,
)
print("CHECK_GENERATION RETURN BEGIN")
print(json.dumps(result, indent=2, sort_keys=True))
print("CHECK_GENERATION RETURN END")
