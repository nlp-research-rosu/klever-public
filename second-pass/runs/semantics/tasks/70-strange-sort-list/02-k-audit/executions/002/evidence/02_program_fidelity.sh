#!/usr/bin/env bash
set -u

cd /tmp/audit-work/task70
status=0

echo "Trusted translator regeneration:"
python3 py2mpy.py solution.py > regenerated-solution.mpy
translator_status=$?
echo "translator exit=$translator_status"
if [[ "$translator_status" -ne 0 ]]; then
  status=1
fi

sha256sum solution.py solution.mpy regenerated-solution.mpy
if cmp -s solution.mpy regenerated-solution.mpy; then
  echo "MPY_BYTE_IDENTITY=PASS"
else
  echo "MPY_BYTE_IDENTITY=FAIL"
  diff -u solution.mpy regenerated-solution.mpy
  status=1
fi

echo "Independent canonical differential:"
python3 /audit-output/evidence/02_differential.py
differential_status=$?
echo "differential exit=$differential_status"
if [[ "$differential_status" -ne 0 ]]; then
  status=1
fi

exit "$status"
