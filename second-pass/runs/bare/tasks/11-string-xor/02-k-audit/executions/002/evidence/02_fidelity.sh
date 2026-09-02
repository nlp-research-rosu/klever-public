#!/usr/bin/env bash
set -euo pipefail
trap 'rc=$?; echo "EXIT_STATUS=$rc"' EXIT

echo 'COMMAND: bash /audit-output/evidence/02_fidelity.sh'
echo 'COMMAND: python3 /tmp/audit-work/11-string-xor/reference/py2mpy.py /tmp/audit-work/11-string-xor/source/solution.py > /tmp/audit-work/11-string-xor/regenerated.mpy'
python3 /tmp/audit-work/11-string-xor/reference/py2mpy.py \
  /tmp/audit-work/11-string-xor/source/solution.py \
  > /tmp/audit-work/11-string-xor/regenerated.mpy

echo 'COMMAND: cmp /tmp/audit-work/11-string-xor/regenerated.mpy /tmp/audit-work/11-string-xor/source/solution.mpy'
cmp \
  /tmp/audit-work/11-string-xor/regenerated.mpy \
  /tmp/audit-work/11-string-xor/source/solution.mpy
echo 'translator_byte_identity=true'

echo 'COMMAND: python3 /audit-output/evidence/02_differential.py'
python3 /audit-output/evidence/02_differential.py
