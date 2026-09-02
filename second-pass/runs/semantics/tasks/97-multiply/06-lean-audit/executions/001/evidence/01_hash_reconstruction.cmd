#!/usr/bin/env bash
set -euo pipefail
printf '%s\n' \
  'COMMAND: PYTHONPATH=/reference python3 /audit-output/evidence/01_hash_reconstruction.py'
PYTHONPATH=/reference python3 \
  /audit-output/evidence/01_hash_reconstruction.py
