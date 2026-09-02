#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

from tools.klean_preflight import check_generation


command_records: list[dict[str, object]] = []


def recording_run(
    command: list[str], *, cwd: Path, timeout: int
) -> tuple[int, str]:
    print(f"$ (cd {cwd} && {' '.join(command)})", flush=True)
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
        output = (
            error.stdout.decode() if isinstance(error.stdout, bytes)
            else error.stdout or ""
        )
        output += f"\nTIMEOUT after {timeout}s\n"
    print(output, end="" if output.endswith("\n") or not output else "\n", flush=True)
    print(f"exit_code={code}", flush=True)
    command_records.append(
        {
            "command": command,
            "cwd": str(cwd),
            "exit_code": code,
            "output": output,
            "output_sha256": hashlib.sha256(output.encode()).hexdigest(),
        }
    )
    return code, output


returned = check_generation(
    Path("/reference/k-proof"),
    Path("/reference/lemma-discovery.json"),
    Path("/reference/klean-generation"),
    toolchain_lock=Path("/reference/klean-toolchain.lock.json"),
    run_command=recording_run,
)
print("RETURNED_EVIDENCE")
print(
    json.dumps(
        {
            "check_generation": returned,
            "complete_command_records": command_records,
        },
        indent=2,
        sort_keys=True,
    )
)
