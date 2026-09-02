#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
from pathlib import Path

from tools.klean_preflight import check_generation


def main() -> None:
    complete_commands: list[dict[str, object]] = []

    def recording_runner(
        command: list[str], *, cwd: Path, timeout: int
    ) -> tuple[int, str]:
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
                (error.stdout or "")
                + (error.stderr or "")
                + f"\nTIMEOUT after {timeout}s"
            )
        complete_commands.append(
            {
                "command": command,
                "cwd": str(cwd),
                "timeout_seconds": timeout,
                "exit_code": code,
                "complete_output": output,
            }
        )
        return code, output

    result = check_generation(
        Path("/reference/k-proof"),
        Path("/reference/lemma-discovery.json"),
        Path("/reference/klean-generation"),
        toolchain_lock=Path("/reference/klean-toolchain.lock.json"),
        run_command=recording_runner,
    )
    print(
        json.dumps(
            {
                "call": {
                    "function": "tools.klean_preflight.check_generation",
                    "PYTHONPATH": "/reference",
                    "frozen_input": "/reference/k-proof",
                    "discovery_manifest": "/reference/lemma-discovery.json",
                    "generation": "/reference/klean-generation",
                    "toolchain_lock": "/reference/klean-toolchain.lock.json",
                },
                "returned_evidence": result,
                "complete_command_records": complete_commands,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
