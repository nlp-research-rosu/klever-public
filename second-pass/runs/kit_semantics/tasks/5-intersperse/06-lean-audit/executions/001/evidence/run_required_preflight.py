#!/usr/bin/env python3
import json
from pathlib import Path

from tools import klean_preflight


def logged_run(command, *, cwd, timeout):
    print(f"$ (cd {cwd} && {' '.join(command)})", flush=True)
    code, output = klean_preflight._run(
        command, cwd=cwd, timeout=timeout
    )
    print(output, end="" if output.endswith("\n") or not output else "\n")
    print(f"[exit_code={code}]", flush=True)
    return code, output


evidence = klean_preflight.check_generation(
    Path("/reference/k-proof"),
    Path("/reference/lemma-discovery.json"),
    Path("/reference/klean-generation"),
    toolchain_lock=Path("/reference/klean-toolchain.lock.json"),
    run_command=logged_run,
)
print("RETURNED_EVIDENCE_JSON")
print(json.dumps(evidence, indent=2, sort_keys=True))
