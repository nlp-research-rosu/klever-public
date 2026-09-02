#!/usr/bin/env python3
"""Rerun the trusted Stage 4 generation preflight with complete output."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from tools.klean_preflight import check_generation


def logged_run(
    command: list[str], *, cwd: Path, timeout: int
) -> tuple[int, str]:
    print(
        "NESTED_COMMAND_BEGIN "
        + json.dumps(
            {
                "command": command,
                "cwd": str(cwd),
                "timeout_seconds": timeout,
            },
            sort_keys=True,
        ),
        flush=True,
    )
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            timeout=timeout,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        code = result.returncode
        output = result.stdout
    except subprocess.TimeoutExpired as error:
        code = 124
        output = (error.stdout or "") + (error.stderr or "")
        output += f"\nTIMEOUT after {timeout}s\n"
    print(output, end="" if output.endswith("\n") or not output else "\n")
    print(
        "NESTED_COMMAND_END "
        + json.dumps({"command": command, "exit_code": code}, sort_keys=True),
        flush=True,
    )
    return code, output


result = check_generation(
    Path("/reference/k-proof"),
    Path("/reference/lemma-discovery.json"),
    Path("/reference/klean-generation"),
    toolchain_lock=Path("/reference/klean-toolchain.lock.json"),
    run_command=logged_run,
)
print("CHECK_GENERATION_RETURN_BEGIN")
print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
print("CHECK_GENERATION_RETURN_END")
