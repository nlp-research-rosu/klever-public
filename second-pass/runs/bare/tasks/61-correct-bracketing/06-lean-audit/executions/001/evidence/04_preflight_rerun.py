#!/usr/bin/env python3
"""Run the required trusted check_generation and expose complete build output."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
from pathlib import Path

from tools import klean_preflight


TOOLCHAIN_BIN = Path(
    "/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin"
)
PROC_COMPAT = Path("/tmp/audit-work/proc-self-compat.so")


def visible_run(
    command: list[str],
    *,
    cwd: Path,
    timeout: int,
) -> tuple[int, str]:
    environment = os.environ.copy()
    environment["PATH"] = (
        f"{TOOLCHAIN_BIN}:{environment.get('PATH', '')}"
    )
    environment["LD_PRELOAD"] = str(PROC_COMPAT)
    print(f"COMMAND={' '.join(command)}")
    print(f"CWD={cwd}")
    print(f"PINNED_TOOLCHAIN_BIN={TOOLCHAIN_BIN}")
    print(f"PROC_COMPAT={PROC_COMPAT}")
    result = subprocess.run(
        command,
        cwd=cwd,
        timeout=timeout,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env=environment,
    )
    print(f"EXIT={result.returncode}")
    print("OUTPUT_BEGIN")
    print(result.stdout, end="")
    print("OUTPUT_END")
    print(f"OUTPUT_SHA256={hashlib.sha256(result.stdout.encode()).hexdigest()}")
    return result.returncode, result.stdout


assert PROC_COMPAT.is_file()
result = klean_preflight.check_generation(
    Path("/reference/k-proof"),
    Path("/reference/lemma-discovery.json"),
    Path("/reference/klean-generation"),
    toolchain_lock=Path("/reference/klean-toolchain.lock.json"),
    run_command=visible_run,
)
print("RETURNED_EVIDENCE_BEGIN")
print(json.dumps(result, indent=2, sort_keys=True))
print("RETURNED_EVIDENCE_END")
recorded = json.loads(
    Path("/reference/klean-generation/preflight.json").read_text()
)
audit_input = json.loads(Path("/audit-input.json").read_text())
assert result == recorded
assert result == audit_input["resolution"]["stage4_preflight"]
print("RETURNED_EVIDENCE_EXACTLY_MATCHES_RECORDED_AND_AUDIT_INPUT=PASS")
assert result["status"] == "KLEAN_NO_OBLIGATIONS"
assert result["obligation_count"] == 0
assert result["target"] is None
print("OVERALL=PASS")
