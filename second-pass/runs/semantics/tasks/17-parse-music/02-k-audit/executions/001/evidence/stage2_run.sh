#!/usr/bin/env bash
set -u
set -o pipefail
set -x

work=/tmp/audit-work/reconstruction

python3 /reference/py2mpy.py "$work/solution.py" > "$work/solution.regenerated.mpy"
translator_status=$?
printf 'trusted translator exit: %d\n' "$translator_status"

cmp -s "$work/solution.regenerated.mpy" "$work/solution.mpy"
identity_status=$?
printf 'solution.mpy byte-identity cmp exit: %d\n' "$identity_status"
if test "$identity_status" -ne 0; then
  diff -u "$work/solution.mpy" "$work/solution.regenerated.mpy"
fi

sha256sum "$work/solution.mpy" "$work/solution.regenerated.mpy"

python3 /audit-output/evidence/stage2_differential.py
differential_status=$?
printf 'differential test exit: %d\n' "$differential_status"

if test "$translator_status" -ne 0 || test "$identity_status" -ne 0 || test "$differential_status" -ne 0; then
  exit 1
fi
exit 0
