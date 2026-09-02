#!/usr/bin/env bash
set -euo pipefail

cc -shared -fPIC -O2 -Wall -Wextra -Werror \
  -o /tmp/audit-work/lean_app_path_compat.so \
  /audit-output/evidence/lean_app_path_compat.c \
  -ldl
sha256sum \
  /audit-output/evidence/lean_app_path_compat.c \
  /tmp/audit-work/lean_app_path_compat.so

PYTHONPATH=/reference python3 - <<'PY'
import json
import os
import shlex
import subprocess
from pathlib import Path

from tools.klean_preflight import check_generation

lean_root = '/opt/elan/toolchains/leanprover--lean4---v4.22.0'
compat = '/tmp/audit-work/lean_app_path_compat.so'

def recording_run(command, *, cwd, timeout):
    print(f"INTERNAL COMMAND cwd={cwd}: {shlex.join(command)}")
    environment = os.environ.copy()
    environment.update({
        'LAKE_HOME': lean_root,
        'LEAN_SYSROOT': lean_root,
        'LD_PRELOAD': compat,
    })
    try:
        completed = subprocess.run(
            command,
            cwd=cwd,
            timeout=timeout,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            env=environment,
        )
        code, output = completed.returncode, completed.stdout
    except subprocess.TimeoutExpired:
        code, output = 124, f'TIMEOUT after {timeout}s'
    print(f"INTERNAL EXIT: {code}")
    print("INTERNAL OUTPUT BEGIN")
    print(output, end='' if output.endswith('\n') or not output else '\n')
    print("INTERNAL OUTPUT END")
    return code, output

result = check_generation(
    Path('/reference/k-proof'),
    Path('/reference/lemma-discovery.json'),
    Path('/reference/klean-generation'),
    toolchain_lock=Path('/reference/klean-toolchain.lock.json'),
    run_command=recording_run,
)
print("RETURNED EVIDENCE")
print(json.dumps(result, indent=2, sort_keys=True))
PY
