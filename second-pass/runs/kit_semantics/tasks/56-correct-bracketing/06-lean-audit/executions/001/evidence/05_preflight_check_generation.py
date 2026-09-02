#!/usr/bin/env python3
import json
import os
import subprocess
from pathlib import Path

from tools.klean_preflight import check_generation


def run_and_capture(command, *, cwd, timeout):
    print(f'PREFLIGHT_SUBCOMMAND: cwd={cwd} command={command!r} timeout={timeout}', flush=True)
    environment = os.environ.copy()
    toolchain = '/opt/elan/toolchains/leanprover--lean4---v4.22.0'
    environment.update({
        'LD_PRELOAD': '/tmp/audit-work/lean-proc-shim/lean_proc_pid_shim.so',
        'LEAN_SYSROOT': toolchain,
        'LEAN': f'{toolchain}/bin/lean',
        'LAKE': f'{toolchain}/bin/lake',
        'LAKE_HOME': toolchain,
    })
    completed = subprocess.run(
        command,
        cwd=cwd,
        env=environment,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
        check=False,
    )
    print(f'PREFLIGHT_SUBCOMMAND_EXIT: {completed.returncode}', flush=True)
    print('PREFLIGHT_SUBCOMMAND_OUTPUT_BEGIN', flush=True)
    print(completed.stdout, end='' if completed.stdout.endswith('\n') or not completed.stdout else '\n', flush=True)
    print('PREFLIGHT_SUBCOMMAND_OUTPUT_END', flush=True)
    return completed.returncode, completed.stdout


print('COMMAND: PYTHONPATH=/reference tools.klean_preflight.check_generation(')
print('  /reference/k-proof, /reference/lemma-discovery.json,')
print('  /reference/klean-generation, toolchain_lock=/reference/klean-toolchain.lock.json)')
result = check_generation(
    Path('/reference/k-proof'),
    Path('/reference/lemma-discovery.json'),
    Path('/reference/klean-generation'),
    toolchain_lock=Path('/reference/klean-toolchain.lock.json'),
    run_command=run_and_capture,
)
print('CHECK_GENERATION_RETURN_BEGIN')
print(json.dumps(result, indent=2, sort_keys=True))
print('CHECK_GENERATION_RETURN_END')
if result.get('status') != 'KLEAN_NO_OBLIGATIONS':
    raise SystemExit('UNEXPECTED_PREFLIGHT_STATUS')
audit_preflight = json.loads(Path('/audit-input.json').read_text())['resolution']['stage4_preflight']
print(f'RETURN_EXACTLY_MATCHES_AUDIT_INPUT_STAGE4_PREFLIGHT: {result == audit_preflight}')
if result != audit_preflight:
    raise SystemExit('RERUN_PREFLIGHT_DIFFERS_FROM_LAUNCHER_RECORD')
