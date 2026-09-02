#!/usr/bin/env bash
set -euo pipefail
printf '%s\n' \
  'COMMAND: PYTHONPATH=/reference python3 /audit-output/evidence/03_inventory_reconstruction.py'
PYTHONPATH=/reference python3 \
  /audit-output/evidence/03_inventory_reconstruction.py
