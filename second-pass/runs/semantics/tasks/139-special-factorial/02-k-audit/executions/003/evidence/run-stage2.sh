#!/usr/bin/env bash
set -euo pipefail
set -x

cd /tmp/audit-work/case
python3 trusted-py2mpy.py solution.py > solution.regenerated.mpy
cmp solution.regenerated.mpy solution.mpy
sha256sum solution.regenerated.mpy solution.mpy
python3 /audit-output/evidence/differential_test.py
