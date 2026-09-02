#!/usr/bin/env bash
set -euo pipefail
set -x

cd /tmp/audit-work/fresh
python3 trusted/py2mpy.py solution.py > regenerated-solution.mpy
cmp solution.mpy regenerated-solution.mpy
sha256sum solution.mpy regenerated-solution.mpy
python3 /audit-output/evidence/02-differential.py
