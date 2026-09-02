#!/usr/bin/env bash
set -u
set -o pipefail
set -x

work=/tmp/audit-work/candidate-clean
evidence=/audit-output/evidence

python3 /reference/py2mpy.py "$work/solution.py" > "$work/solution.regenerated.mpy"
translate_status=$?
printf 'TRANSLATE_EXIT=%s\n' "$translate_status"

cmp --silent "$work/solution.regenerated.mpy" "$work/solution.mpy"
identity_status=$?
printf 'SOLUTION_MPY_CMP_EXIT=%s\n' "$identity_status"
sha256sum "$work/solution.regenerated.mpy" "$work/solution.mpy"

PYTHONDONTWRITEBYTECODE=1 python3 "$evidence/differential_test.py" \
  --inputs-out "$evidence/differential-inputs.json"
diff_status=$?
printf 'DIFFERENTIAL_EXIT=%s\n' "$diff_status"

if (( translate_status == 0 && identity_status == 0 && diff_status == 0 )); then
  exit 0
fi
exit 1
