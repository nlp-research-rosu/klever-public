#!/usr/bin/env bash
set -euxo pipefail

python3 /reference/py2mpy.py /tmp/audit-work/fresh/solution.py \
  > /tmp/audit-work/fresh/solution.regenerated.mpy
cmp /tmp/audit-work/fresh/solution.regenerated.mpy /candidate/solution.mpy
cmp /tmp/audit-work/fresh/solution.regenerated.mpy /tmp/audit-work/fresh/solution.mpy
sha256sum \
  /reference/py2mpy.py \
  /tmp/audit-work/fresh/solution.py \
  /tmp/audit-work/fresh/solution.mpy \
  /tmp/audit-work/fresh/solution.regenerated.mpy
python3 /audit-output/evidence/differential.py \
  --cases-output /audit-output/evidence/differential-cases.jsonl
