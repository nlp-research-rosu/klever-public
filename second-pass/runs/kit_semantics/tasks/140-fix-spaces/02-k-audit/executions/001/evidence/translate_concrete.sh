#!/usr/bin/env bash
set -euo pipefail

python3 /tmp/audit-work/reference/py2mpy.py \
  /tmp/audit-work/candidate-src/concrete_cases.py \
  > /tmp/audit-work/candidate-src/concrete_cases.mpy
sha256sum /tmp/audit-work/candidate-src/concrete_cases.mpy
