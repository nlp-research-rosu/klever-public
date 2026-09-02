#!/usr/bin/env python3
"""Call the trusted Stage 4 generation checker and expose full diagnostics."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from tools.klean_preflight import check_generation


def logged_run(command: list[str], *, cwd: Path, timeout: int) -> tuple[int, str]:
    print(f"COMMAND: {' '.join(command)}")
    print(f"CWD: {cwd}")
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            timeout=timeout,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        output = result.stdout
        code = result.returncode
    except subprocess.TimeoutExpired as error:
        output = (error.stdout or "") + f"\nTIMEOUT after {timeout}s\n"
        code = 124
    print(f"EXIT_CODE: {code}")
    print("OUTPUT_BEGIN")
    print(output, end="" if output.endswith("\n") or not output else "\n")
    print("OUTPUT_END")
    return code, output


result = check_generation(
    Path("/reference/k-proof"),
    Path("/reference/lemma-discovery.json"),
    Path("/reference/klean-generation"),
    toolchain_lock=Path("/reference/klean-toolchain.lock.json"),
    run_command=logged_run,
)
print("RETURNED_EVIDENCE_BEGIN")
print(json.dumps(result, indent=2, sort_keys=True))
print("RETURNED_EVIDENCE_END")
