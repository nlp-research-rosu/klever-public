#!/usr/bin/env bash
set -euxo pipefail

cd /tmp/audit-work/reconstruction
python3 /tmp/audit-work/reference/py2mpy.py solution.py > solution.regenerated.mpy
cmp solution.regenerated.mpy solution.mpy
sha256sum solution.regenerated.mpy solution.mpy
python3 /audit-output/evidence/differential.py \
  /tmp/audit-work/reference/canonical.py \
  /tmp/audit-work/reconstruction/solution.py
