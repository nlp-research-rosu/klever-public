#!/usr/bin/env bash
set -o pipefail

echo 'COMMAND: python3 /audit-output/evidence/02-precision-differential.py'
python3 /audit-output/evidence/02-precision-differential.py
rc=$?
echo "EXIT: $rc"
if (( rc == 1 )); then
  echo 'OBSERVED: candidate and trusted canonical materially diverge near the binary64 exact-integer boundary.'
  exit 0
fi
exit 1
