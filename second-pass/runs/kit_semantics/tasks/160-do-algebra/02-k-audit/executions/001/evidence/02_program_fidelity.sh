#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/160-do-algebra
submitted="$scratch/solution.mpy"
regenerated="$scratch/solution.regenerated.mpy"

echo "COMMAND: python3 py2mpy.py solution.py > solution.regenerated.mpy"
(
  cd "$scratch" || exit 90
  python3 py2mpy.py solution.py > solution.regenerated.mpy
)
translate_status=$?
echo "TRANSLATOR_EXIT_STATUS=$translate_status"
if (( translate_status != 0 )); then
  exit "$translate_status"
fi

echo "COMMAND: cmp -s solution.regenerated.mpy solution.mpy"
cmp -s "$regenerated" "$submitted"
cmp_status=$?
echo "CMP_EXIT_STATUS=$cmp_status"
if (( cmp_status != 0 )); then
  diff -u "$submitted" "$regenerated"
  exit "$cmp_status"
fi
sha256sum "$submitted" "$regenerated"

echo "COMMAND: python3 /audit-output/evidence/02_differential.py"
python3 /audit-output/evidence/02_differential.py
differential_status=$?
echo "DIFFERENTIAL_EXIT_STATUS=$differential_status"
exit "$differential_status"
