#!/usr/bin/env bash
set -uo pipefail

cd /tmp/audit-work/reconstruction
rc=0

echo "COMMAND: python3 /tmp/audit-work/trusted/py2mpy.py solution.py > regenerated-solution.mpy"
python3 /tmp/audit-work/trusted/py2mpy.py solution.py > regenerated-solution.mpy
status=$?
echo "EXIT=$status"
if (( status != 0 )); then rc=1; fi

echo "COMMAND: cmp regenerated-solution.mpy solution.mpy"
cmp regenerated-solution.mpy solution.mpy
status=$?
echo "EXIT=$status"
if (( status != 0 )); then rc=1; fi
sha256sum regenerated-solution.mpy solution.mpy

echo "COMMAND: PYTHONPYCACHEPREFIX=/tmp/audit-work/pycache python3 -m py_compile trusted canonical and candidate solution"
PYTHONPYCACHEPREFIX=/tmp/audit-work/pycache \
  python3 -m py_compile \
  /tmp/audit-work/trusted/canonical.py \
  /tmp/audit-work/reconstruction/solution.py
status=$?
echo "EXIT=$status"
if (( status != 0 )); then rc=1; fi

echo "COMMAND: python3 /audit-output/evidence/differential.py"
python3 /audit-output/evidence/differential.py
status=$?
echo "EXIT=$status"
if (( status != 0 )); then rc=1; fi

echo "OVERALL_STAGE2_EXIT=$rc"
exit "$rc"
