#!/usr/bin/env python3
"""Run the required trusted Stage 4 preflight and expose full subprocess output."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from tools import klean_preflight


def logged_run(
    command: list[str],
    *,
    cwd: Path,
    timeout: int,
) -> tuple[int, str]:
    print(f"SUBCOMMAND={json.dumps(command)}")
    print(f"CWD={cwd}")
    print(f"TIMEOUT={timeout}")
    try:
        completed = subprocess.run(
            command,
            cwd=cwd,
            timeout=timeout,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        output = completed.stdout
        code = completed.returncode
    except subprocess.TimeoutExpired as error:
        output = (
            (error.stdout or "")
            + (error.stderr or "")
            + f"\nTIMEOUT after {timeout}s\n"
        )
        code = 124
    print(f"EXIT_CODE={code}")
    print("BEGIN_COMPLETE_OUTPUT")
    print(output, end="" if output.endswith("\n") or not output else "\n")
    print("END_COMPLETE_OUTPUT")
    return code, output


print(
    "CALL=tools.klean_preflight.check_generation("
    "/reference/k-proof, /reference/lemma-discovery.json, "
    "/reference/klean-generation, "
    "toolchain_lock=/reference/klean-toolchain.lock.json)"
)
result = klean_preflight.check_generation(
    Path("/reference/k-proof"),
    Path("/reference/lemma-discovery.json"),
    Path("/reference/klean-generation"),
    toolchain_lock=Path("/reference/klean-toolchain.lock.json"),
    run_command=logged_run,
)
print("RETURNED_EVIDENCE")
print(json.dumps(result, indent=2, sort_keys=True))
