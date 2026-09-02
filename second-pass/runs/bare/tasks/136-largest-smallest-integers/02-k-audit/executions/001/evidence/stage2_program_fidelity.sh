#!/usr/bin/env bash
set -uo pipefail

work=/tmp/audit-work/reconstruction
evidence=/audit-output/evidence

echo 'COMMAND: python3 py2mpy.py solution.py > regenerated.solution.mpy'
(
  cd "$work" || exit 98
  python3 py2mpy.py solution.py > regenerated.solution.mpy
)
translate_status=$?
echo "TRANSLATE_EXIT_STATUS=$translate_status"

echo 'COMMAND: cmp -s regenerated.solution.mpy solution.mpy'
cmp -s "$work/regenerated.solution.mpy" "$work/solution.mpy"
cmp_status=$?
echo "BYTE_IDENTITY_EXIT_STATUS=$cmp_status"
sha256sum "$work/regenerated.solution.mpy" "$work/solution.mpy"

echo 'COMMAND: python3 differential_test.py canonical.py solution.py differential_inputs.json'
python3 "$evidence/differential_test.py" \
  "$work/canonical.py" \
  "$work/solution.py" \
  "$evidence/differential_inputs.json"
diff_status=$?
echo "DIFFERENTIAL_EXIT_STATUS=$diff_status"

if (( translate_status != 0 || cmp_status != 0 || diff_status != 0 )); then
  exit 1
fi
exit 0
