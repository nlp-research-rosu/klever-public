#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/28-concatenate

echo 'COMMAND: python3 /reference/py2mpy.py /tmp/audit-work/28-concatenate/solution.py > /tmp/audit-work/28-concatenate/solution.regenerated.mpy'
python3 /reference/py2mpy.py "$scratch/solution.py" > "$scratch/solution.regenerated.mpy"
status=$?
echo "EXIT: $status"

echo 'COMMAND: cmp -s /tmp/audit-work/28-concatenate/solution.regenerated.mpy /tmp/audit-work/28-concatenate/solution.mpy'
cmp -s "$scratch/solution.regenerated.mpy" "$scratch/solution.mpy"
status=$?
echo "EXIT: $status"
sha256sum "$scratch/solution.regenerated.mpy" "$scratch/solution.mpy"

echo 'COMMAND: python3 /audit-output/evidence/stage2/differential_test.py'
python3 /audit-output/evidence/stage2/differential_test.py
status=$?
echo "EXIT: $status"
exit "$status"
