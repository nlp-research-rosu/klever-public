#!/usr/bin/env bash
set -euo pipefail
printf '%s\n' \
  'COMMAND: LD_PRELOAD=/tmp/audit-work/05_proc_exe_compat.so PYTHONPATH=/reference python3 /audit-output/evidence/04_rerun_preflight.py'
LD_PRELOAD=/tmp/audit-work/05_proc_exe_compat.so \
PYTHONPATH=/reference \
python3 /audit-output/evidence/04_rerun_preflight.py
