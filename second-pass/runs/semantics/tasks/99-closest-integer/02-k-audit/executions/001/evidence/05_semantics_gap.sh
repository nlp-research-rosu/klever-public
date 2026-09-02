#!/usr/bin/env bash
set -euxo pipefail

root=/tmp/audit-work/99-closest-integer-audit
python3 "$root/trusted/py2mpy.py" \
  /audit-output/evidence/05_semantics_gap.py \
  > "$root/candidate/semantics-gap.mpy"
krun "$root/candidate/semantics-gap.mpy" \
  --definition "$root/candidate/runtime-kompiled"
