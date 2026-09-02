#!/usr/bin/env bash
set -euo pipefail
set -x

cd /tmp/audit-work/84-solve
python3 py2mpy.py solution.py > solution.regenerated.mpy
cmp -s solution.regenerated.mpy solution.mpy
sha256sum solution.regenerated.mpy solution.mpy
python3 /audit-output/evidence/differential_test.py
