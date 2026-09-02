#!/usr/bin/env bash
set -euo pipefail
set -x

python3 /reference/py2mpy.py \
  /tmp/audit-work/candidate-src/solution.py \
  > /tmp/audit-work/solution-regenerated.mpy

cmp /tmp/audit-work/candidate-src/solution.mpy \
  /tmp/audit-work/solution-regenerated.mpy

sha256sum \
  /tmp/audit-work/candidate-src/solution.mpy \
  /tmp/audit-work/solution-regenerated.mpy

python3 /audit-output/evidence/differential_test.py
