#!/usr/bin/env python3
import hashlib
import json
import subprocess
from pathlib import Path

from tools.klean_preflight import check_generation


def run_logged(command, *, cwd, timeout):
    print(
        json.dumps(
            {
                "event": "command",
                "argv": command,
                "cwd": str(cwd),
                "timeout_s": timeout,
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
        output = (error.stdout or "") + f"\nTIMEOUT after {timeout}s\n"
    print(output, end="" if output.endswith("\n") else "\n", flush=True)
    print(
        json.dumps(
            {
                "event": "command_result",
                "exit_code": code,
                "output_sha256": hashlib.sha256(
                    output.encode()
                ).hexdigest(),
            },
            sort_keys=True,
        ),
        flush=True,
    )
    return code, output


result = check_generation(
    Path("/reference/k-proof"),
    Path("/reference/lemma-discovery.json"),
    Path("/reference/klean-generation"),
    toolchain_lock=Path("/reference/klean-toolchain.lock.json"),
    run_command=run_logged,
)
print(
    json.dumps(
        {"event": "check_generation_return", "result": result},
        indent=2,
        sort_keys=True,
    )
)
