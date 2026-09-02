#!/usr/bin/env bash
set -u
set -o pipefail

work=/tmp/audit-work/submitted

echo 'CMD: python3 /reference/py2mpy.py /tmp/audit-work/submitted/solution.py > /tmp/audit-work/submitted/regenerated-solution.mpy'
python3 /reference/py2mpy.py "$work/solution.py" > "$work/regenerated-solution.mpy"
translator_status=$?
echo "EXIT: $translator_status"

echo 'CMD: cmp -s /tmp/audit-work/submitted/regenerated-solution.mpy /tmp/audit-work/submitted/solution.mpy'
cmp -s "$work/regenerated-solution.mpy" "$work/solution.mpy"
cmp_status=$?
echo "EXIT: $cmp_status"

if [[ $cmp_status -ne 0 ]]; then
  diff -u "$work/solution.mpy" "$work/regenerated-solution.mpy"
fi

echo 'CMD: python3 /audit-output/evidence/02_differential.py --workdir /tmp/audit-work/submitted --inputs-out /audit-output/evidence/02_differential_inputs.json'
python3 /audit-output/evidence/02_differential.py \
  --workdir "$work" \
  --inputs-out /audit-output/evidence/02_differential_inputs.json
diff_status=$?
echo "EXIT: $diff_status"

if [[ $translator_status -ne 0 || $cmp_status -ne 0 || $diff_status -ne 0 ]]; then
  exit 1
fi
