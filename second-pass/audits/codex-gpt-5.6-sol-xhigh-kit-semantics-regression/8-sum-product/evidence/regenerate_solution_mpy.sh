#!/usr/bin/env bash
set -euo pipefail

python3 /tmp/audit-work/trusted/py2mpy.py \
  /tmp/audit-work/src/solution.py \
  > /tmp/audit-work/regenerated-solution.mpy

cmp /tmp/audit-work/src/solution.mpy /tmp/audit-work/regenerated-solution.mpy
sha256sum \
  /tmp/audit-work/src/solution.mpy \
  /tmp/audit-work/regenerated-solution.mpy
printf 'TRANSLATOR_BYTE_IDENTITY=PASS\n'
