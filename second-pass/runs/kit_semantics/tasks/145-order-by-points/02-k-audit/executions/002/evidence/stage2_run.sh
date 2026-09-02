#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/145-order-by-points-002
overall=0

echo "$ cd $scratch"
cd "$scratch" || exit 1
echo "EXIT: 0"

echo "$ python3 /reference/py2mpy.py solution.py > regenerated-solution.mpy"
python3 /reference/py2mpy.py solution.py > regenerated-solution.mpy
command_status=$?
echo "EXIT: $command_status"
if [ "$command_status" -ne 0 ]; then overall=1; fi

echo "$ cmp regenerated-solution.mpy solution.mpy"
cmp regenerated-solution.mpy solution.mpy
command_status=$?
echo "EXIT: $command_status"
if [ "$command_status" -ne 0 ]; then overall=1; fi

echo "$ sha256sum solution.py solution.mpy regenerated-solution.mpy"
sha256sum solution.py solution.mpy regenerated-solution.mpy
command_status=$?
echo "EXIT: $command_status"
if [ "$command_status" -ne 0 ]; then overall=1; fi

echo "$ python3 /audit-output/evidence/differential_test.py /reference/canonical.py $scratch/solution.py"
python3 /audit-output/evidence/differential_test.py \
  /reference/canonical.py \
  "$scratch/solution.py"
command_status=$?
echo "EXIT: $command_status"
if [ "$command_status" -ne 0 ]; then overall=1; fi

echo "STAGE2 SCRIPT EXIT: $overall"
exit "$overall"
