#!/usr/bin/env python3
"""Run the trusted final mechanical gate with complete nested output."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from tools.klean_final_gate import check_final


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


result = check_final(
    Path("/reference/k-proof"),
    Path("/reference/lemma-discovery.json"),
    Path("/reference/klean-generation"),
    Path("/candidate"),
    toolchain_lock=Path("/reference/klean-toolchain.lock.json"),
    audit_input=Path("/audit-input.json"),
    run_command=logged_run,
)
print("CHECK_FINAL_RETURN_BEGIN")
print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
print("CHECK_FINAL_RETURN_END")
