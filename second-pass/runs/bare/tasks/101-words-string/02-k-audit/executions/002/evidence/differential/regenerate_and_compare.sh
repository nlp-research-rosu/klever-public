#!/usr/bin/env bash
set -euo pipefail

python3 /tmp/audit-work/reference/py2mpy.py \
  /tmp/audit-work/candidate/solution.py \
  > /tmp/audit-work/regenerated-solution.mpy

cmp /tmp/audit-work/candidate/solution.mpy \
    /tmp/audit-work/regenerated-solution.mpy

sha256sum /tmp/audit-work/candidate/solution.mpy \
          /tmp/audit-work/regenerated-solution.mpy

printf 'BYTE_IDENTITY=PASS\n'
