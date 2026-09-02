#!/usr/bin/env bash
set -u

cd /tmp/audit-work/reconstruction
python3 py2mpy.py solution.py > solution.regenerated.mpy
cmp solution.regenerated.mpy solution.mpy
sha256sum solution.regenerated.mpy solution.mpy solution.py canonical.py
python3 /audit-output/evidence/03_differential.py
python3 /audit-output/evidence/04_claim_witnesses.py
