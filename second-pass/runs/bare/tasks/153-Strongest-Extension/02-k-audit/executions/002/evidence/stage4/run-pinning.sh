#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/153-strongest-extension
evidence=/audit-output/evidence/stage4
overall=0

echo '$ kast regenerated-solution.mpy --definition verification-kompiled --sort Program --output kore'
kast "$scratch/regenerated-solution.mpy" \
  --definition "$scratch/verification-kompiled" \
  --sort Program --output kore > "$evidence/regenerated-solution.kore"
solution_status=$?
echo "exit_status=$solution_status"

echo '$ kast verification-input.mpy --definition verification-kompiled --sort Program --output kore'
kast "$scratch/verification-input.mpy" \
  --definition "$scratch/verification-kompiled" \
  --sort Program --output kore > "$evidence/strongest-program-macro.kore"
macro_status=$?
echo "exit_status=$macro_status"

echo '$ cmp regenerated-solution.kore strongest-program-macro.kore'
cmp "$evidence/regenerated-solution.kore" "$evidence/strongest-program-macro.kore"
cmp_status=$?
echo "exit_status=$cmp_status"

echo '$ sha256sum regenerated-solution.kore strongest-program-macro.kore'
sha256sum "$evidence/regenerated-solution.kore" "$evidence/strongest-program-macro.kore"
hash_status=$?
echo "exit_status=$hash_status"

echo '$ python3 claim-witnesses.py canonical.py solution.py'
python3 "$evidence/claim-witnesses.py" \
  "$scratch/canonical.py" "$scratch/solution.py"
witness_status=$?
echo "exit_status=$witness_status"

for status in "$solution_status" "$macro_status" "$cmp_status" "$hash_status" "$witness_status"; do
  if [[ $status -ne 0 ]]; then
    overall=1
  fi
done
exit "$overall"
