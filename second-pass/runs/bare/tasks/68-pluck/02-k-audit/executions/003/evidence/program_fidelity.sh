#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/68-pluck-audit

echo '$ python3 trusted-py2mpy.py solution.py > regenerated-solution.mpy'
python3 "$scratch/trusted-py2mpy.py" "$scratch/solution.py" \
  > "$scratch/regenerated-solution.mpy"
translate_status=$?
echo "translator exit=$translate_status"

echo '$ cmp regenerated-solution.mpy solution.mpy'
cmp -s "$scratch/regenerated-solution.mpy" "$scratch/solution.mpy"
cmp_status=$?
echo "byte-identity cmp exit=$cmp_status"

echo '$ sha256sum regenerated-solution.mpy solution.mpy solution.py'
sha256sum \
  "$scratch/regenerated-solution.mpy" \
  "$scratch/solution.mpy" \
  "$scratch/solution.py"
hash_status=$?
echo "sha256sum exit=$hash_status"

exit $((translate_status || cmp_status || hash_status))
