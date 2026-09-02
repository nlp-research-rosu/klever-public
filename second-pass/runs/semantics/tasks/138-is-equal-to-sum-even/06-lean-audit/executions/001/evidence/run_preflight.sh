#!/usr/bin/env bash
set -uo pipefail

log=/audit-output/evidence/preflight-check-generation-repaired.log
lean_bin=/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin
shim=/audit-output/evidence/lean_exepath_shim.so

{
  printf '%s\n' '$ env PYTHONPATH=/reference PATH=/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin:$PATH LD_PRELOAD=/audit-output/evidence/lean_exepath_shim.so AUDIT_LEAN_EXE_PATH=/opt/elan/toolchains/leanprover--lean4---v4.22.0/bin/lake python3 -c <check_generation invocation>'
  env \
    PYTHONPATH=/reference \
    PATH="$lean_bin:$PATH" \
    LD_PRELOAD="$shim" \
    AUDIT_LEAN_EXE_PATH="$lean_bin/lake" \
    python3 -c '
import json
from pathlib import Path
from tools.klean_preflight import check_generation

result = check_generation(
    Path("/reference/k-proof"),
    Path("/reference/lemma-discovery.json"),
    Path("/reference/klean-generation"),
    toolchain_lock=Path("/reference/klean-toolchain.lock.json"),
)
print(json.dumps(result, indent=2, sort_keys=True))
'
  code=$?
  printf '\nEXIT_CODE: %s\n' "$code"
  exit "$code"
} >"$log" 2>&1
