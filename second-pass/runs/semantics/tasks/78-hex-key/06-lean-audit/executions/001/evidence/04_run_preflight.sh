#!/usr/bin/env bash
set -euo pipefail

# Lean 4.22 needs the compatibility preload documented and built by 04a.
# The required checker call itself is in 04_run_preflight.py.
LD_PRELOAD=/tmp/audit-work/lean-hostpid-preload.so \
PYTHONPATH=/reference \
python3 /audit-output/evidence/04_run_preflight.py
