#!/usr/bin/env bash
set -euo pipefail
printf '%s\n' \
  'COMMAND: PYTHONPATH=/reference python3 /audit-output/evidence/04_rerun_preflight.py'
PYTHONPATH=/reference python3 \
  /audit-output/evidence/04_rerun_preflight.py
