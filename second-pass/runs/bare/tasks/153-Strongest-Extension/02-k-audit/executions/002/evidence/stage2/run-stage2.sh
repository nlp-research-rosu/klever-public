#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/153-strongest-extension

echo '$ python3 trusted-py2mpy.py solution.py > regenerated-solution.mpy'
python3 "$scratch/trusted-py2mpy.py" "$scratch/solution.py" \
  > "$scratch/regenerated-solution.mpy"
regen_status=$?
echo "exit_status=$regen_status"

echo '$ cmp regenerated-solution.mpy solution.mpy'
cmp "$scratch/regenerated-solution.mpy" "$scratch/solution.mpy"
cmp_status=$?
echo "exit_status=$cmp_status"

echo '$ sha256sum regenerated-solution.mpy solution.mpy'
sha256sum "$scratch/regenerated-solution.mpy" "$scratch/solution.mpy"
hash_status=$?
echo "exit_status=$hash_status"

echo '$ python3 differential.py canonical.py solution.py'
python3 /audit-output/evidence/stage2/differential.py \
  "$scratch/canonical.py" "$scratch/solution.py"
diff_status=$?
echo "exit_status=$diff_status (nonzero means a semantic mismatch was found)"

if [[ $regen_status -ne 0 || $cmp_status -ne 0 || $hash_status -ne 0 ]]; then
  exit 2
fi
exit "$diff_status"
