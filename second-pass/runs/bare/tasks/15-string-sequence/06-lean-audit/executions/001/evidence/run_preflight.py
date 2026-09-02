#!/usr/bin/env python3

import hashlib
import json
import os
import subprocess
from pathlib import Path

from tools.klean_preflight import check_generation


PRELOAD = "/tmp/audit-work/libouterpid.so"
FULL_OUTPUT = Path("/audit-output/evidence/preflight-build-full.log")


def run_command(command: list[str], *, cwd: Path, timeout: int) -> tuple[int, str]:
    environment = dict(os.environ)
    environment["LD_PRELOAD"] = PRELOAD
    environment["LEAN_SYSROOT"] = (
        "/opt/elan/toolchains/leanprover--lean4---v4.22.0"
    )
    environment["LAKE_HOME"] = (
        "/opt/elan/toolchains/leanprover--lean4---v4.22.0/src/lean/lake"
    )
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            timeout=timeout,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            env=environment,
        )
        output = result.stdout
        code = result.returncode
    except subprocess.TimeoutExpired as error:
        output = (error.stdout or "") + (error.stderr or "")
        code = 124
    with FULL_OUTPUT.open("a", encoding="utf-8") as stream:
        stream.write(f"$ (cd {cwd} && {' '.join(command)})\n")
        stream.write(output)
        if output and not output.endswith("\n"):
            stream.write("\n")
        stream.write(f"EXIT: {code}\n")
    return code, output


def main() -> None:
    FULL_OUTPUT.write_text("", encoding="utf-8")
    result = check_generation(
        Path("/reference/k-proof"),
        Path("/reference/lemma-discovery.json"),
        Path("/reference/klean-generation"),
        toolchain_lock=Path("/reference/klean-toolchain.lock.json"),
        run_command=run_command,
    )
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    Path("/audit-output/evidence/preflight-rerun.json").write_text(
        encoded, encoding="utf-8"
    )
    print(encoded, end="")
    print(
        "preflight-rerun.json sha256",
        hashlib.sha256(encoded.encode()).hexdigest(),
    )


if __name__ == "__main__":
    main()
