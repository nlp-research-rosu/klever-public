#!/usr/bin/env bash
set -euo pipefail

cc -shared -fPIC -Wall -Wextra -Werror \
  -o /tmp/audit-work/proc_pid_shim.so \
  /audit-output/evidence/proc_pid_shim.c

export PYTHONPATH=/reference
export LAKE_HOME=/opt/elan/toolchains/leanprover--lean4---v4.22.0
export LEAN_SYSROOT=/opt/elan/toolchains/leanprover--lean4---v4.22.0
export LD_PRELOAD=/tmp/audit-work/proc_pid_shim.so

python /audit-output/evidence/hash_and_provenance_check.py
python /audit-output/evidence/inventory_check.py
python /audit-output/evidence/classification_cases.py
python /audit-output/evidence/stage4_structure_check.py
python /audit-output/evidence/preflight_check.py
