#!/usr/bin/env bash
set -euxo pipefail

root=/tmp/audit-work/99-closest-integer-audit
python3 "$root/trusted/py2mpy.py" \
  /audit-output/evidence/04_ground_concrete.py \
  > "$root/candidate/ground-concrete.mpy"
krun "$root/candidate/ground-concrete.mpy" \
  --definition "$root/candidate/runtime-kompiled"
