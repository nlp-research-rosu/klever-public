#!/usr/bin/env bash
set -u

python3 /reference/py2mpy.py /tmp/audit-work/scratch/solution.py \
  > /tmp/audit-work/scratch/regenerated-solution.mpy
translator_status=$?
echo "translator_exit_status=$translator_status"

cmp -s /tmp/audit-work/scratch/regenerated-solution.mpy \
       /tmp/audit-work/scratch/solution.mpy
identity_status=$?
echo "solution_mpy_cmp_status=$identity_status"

sha256sum /tmp/audit-work/scratch/solution.py \
          /tmp/audit-work/scratch/solution.mpy \
          /tmp/audit-work/scratch/regenerated-solution.mpy

if (( translator_status != 0 || identity_status != 0 )); then
  diff -u /tmp/audit-work/scratch/solution.mpy \
          /tmp/audit-work/scratch/regenerated-solution.mpy
  exit 1
fi
