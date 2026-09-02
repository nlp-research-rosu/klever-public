#!/usr/bin/env bash
set -euo pipefail
set -x

cd /tmp/audit-work/prime-length-audit
python3 /reference/py2mpy.py solution.py > solution.regenerated.mpy
sha256sum solution.mpy solution.regenerated.mpy
cmp solution.mpy solution.regenerated.mpy
python3 /audit-output/evidence/stage2_differential.py
