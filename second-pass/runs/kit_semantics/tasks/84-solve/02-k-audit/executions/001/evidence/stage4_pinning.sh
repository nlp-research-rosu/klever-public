#!/usr/bin/env bash
set -euo pipefail
set -x

cd /tmp/audit-work/84-solve
sed -n '/BEGIN SOLUTION MPY/,/END SOLUTION MPY/p' verification.k \
  | sed '1d;$d;s/^    //' > embedded-solution.mpy
cmp -s solution.mpy embedded-solution.mpy
sha256sum solution.mpy embedded-solution.mpy
python3 /audit-output/evidence/claim_witnesses.py
