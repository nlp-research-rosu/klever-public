#!/usr/bin/env python3
"""Run the trusted Stage 4 preflight and retain complete subprocess evidence."""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

from tools.klean_preflight import check_generation


EVIDENCE = Path("/audit-output/evidence")
APP_PATH_SHIM = Path("/tmp/audit-work/lean_app_path_shim.so")


def run_and_record(
    command: list[str],
    *,
    cwd: Path,
    timeout: int,
) -> tuple[int, str]:
    try:
        environment = os.environ.copy()
        environment["LD_PRELOAD"] = str(APP_PATH_SHIM)
        completed = subprocess.run(
            command,
            cwd=cwd,
            env=environment,
            timeout=timeout,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        code = completed.returncode
        output = completed.stdout
    except subprocess.TimeoutExpired as error:
        code = 124
        output = f"TIMEOUT after {timeout}s\n"
        if error.stdout:
            output += (
                error.stdout
                if isinstance(error.stdout, str)
                else error.stdout.decode(errors="replace")
            )
    label = "-".join(command)
    transcript = (
        f"cwd: {cwd}\n"
        f"command: {' '.join(command)}\n"
        f"LD_PRELOAD: {APP_PATH_SHIM}\n"
        f"exit_code: {code}\n"
        "output:\n"
        f"{output}"
    )
    (EVIDENCE / f"preflight-{label}.log").write_text(transcript)
    return code, output


result = check_generation(
    Path("/reference/k-proof"),
    Path("/reference/lemma-discovery.json"),
    Path("/reference/klean-generation"),
    toolchain_lock=Path("/reference/klean-toolchain.lock.json"),
    run_command=run_and_record,
)
print(json.dumps(result, indent=2, sort_keys=True))
