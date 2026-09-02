#!/usr/bin/env bash
set -euxo pipefail

cd /tmp/audit-work/reconstruction
python3 py2mpy.py solution.py > regenerated-solution.mpy
cmp regenerated-solution.mpy solution.mpy
sha256sum solution.py solution.mpy regenerated-solution.mpy
python3 /audit-output/evidence/02_independent_differential.py
