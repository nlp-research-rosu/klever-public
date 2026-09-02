#!/usr/bin/env bash
set -euo pipefail

cd /audit-output/evidence/body-mutation
python3 py2mpy.py solution.py > solution.mpy

cp solution.py solution.mpy semantic.k solution-program.k \
  verification.k spec.k definition.k py2mpy.py \
  /tmp/audit-work/body-mutation/

sha256sum solution.py solution.mpy solution-program.k verification.k spec.k
find /tmp/audit-work/body-mutation -maxdepth 1 -printf '%y %f size=%s\n' | sort
