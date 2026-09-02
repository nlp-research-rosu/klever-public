#!/usr/bin/env bash
set -u

python3 /tmp/audit-work/scratch/py2mpy.py \
  /audit-output/evidence/concrete_harness.py \
  >/tmp/audit-work/scratch/concrete_harness.mpy

krun /tmp/audit-work/scratch/concrete_harness.mpy \
  --definition /tmp/audit-work/scratch/runtime-kompiled
