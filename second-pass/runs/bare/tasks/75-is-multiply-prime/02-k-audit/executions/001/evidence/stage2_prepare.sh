#!/usr/bin/env bash
set -euo pipefail

mkdir -p /tmp/audit-work/rebuild
cp /candidate/solution.py /tmp/audit-work/rebuild/solution.py
cp /candidate/solution.mpy /tmp/audit-work/rebuild/submitted-solution.mpy
cp /candidate/semantic.k /tmp/audit-work/rebuild/semantic.k
cp /candidate/solution-program.k /tmp/audit-work/rebuild/solution-program.k
cp /candidate/verification.k /tmp/audit-work/rebuild/verification.k
cp /candidate/spec.k /tmp/audit-work/rebuild/spec.k
cp /candidate/definition.k /tmp/audit-work/rebuild/definition.k
cp /reference/py2mpy.py /tmp/audit-work/rebuild/py2mpy.py
cp /reference/canonical.py /tmp/audit-work/rebuild/trusted-canonical.py
cp /reference/prompt.py /tmp/audit-work/rebuild/trusted-prompt.py

python3 /tmp/audit-work/rebuild/py2mpy.py \
  /tmp/audit-work/rebuild/solution.py \
  > /tmp/audit-work/rebuild/solution.mpy

cmp /tmp/audit-work/rebuild/solution.mpy \
    /tmp/audit-work/rebuild/submitted-solution.mpy

sha256sum \
  /tmp/audit-work/rebuild/solution.py \
  /tmp/audit-work/rebuild/solution.mpy \
  /tmp/audit-work/rebuild/submitted-solution.mpy \
  /tmp/audit-work/rebuild/py2mpy.py

printf 'SCRATCH_TREE:\n'
find /tmp/audit-work/rebuild -maxdepth 1 -printf '%y %f size=%s\n' | sort
printf 'REGENERATED_MPY_BYTE_IDENTITY: yes\n'
