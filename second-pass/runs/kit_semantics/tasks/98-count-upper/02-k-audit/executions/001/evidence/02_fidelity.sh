#!/usr/bin/env bash
set -euo pipefail

python3 /reference/py2mpy.py /candidate/solution.py \
  > /tmp/audit-work/98-count-upper/solution.regenerated.mpy
cmp /candidate/solution.mpy \
  /tmp/audit-work/98-count-upper/solution.regenerated.mpy
sha256sum /candidate/solution.mpy \
  /tmp/audit-work/98-count-upper/solution.regenerated.mpy
echo "TRUSTED_TRANSLATION_BYTE_IDENTITY=PASS"

python3 /audit-output/evidence/02_differential.py
echo "INDEPENDENT_DIFFERENTIAL=PASS"
