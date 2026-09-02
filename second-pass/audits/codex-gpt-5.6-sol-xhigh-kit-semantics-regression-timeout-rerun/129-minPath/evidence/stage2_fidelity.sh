#!/usr/bin/env bash
set +e
set -x

work=/tmp/audit-work/reconstruction
evidence=/audit-output/evidence
overall=0

cd "$work" || exit 2
python3 py2mpy.py solution.py > regenerated-solution.mpy
translator_status=$?
if (( translator_status != 0 )); then
  overall=1
fi

cmp -s regenerated-solution.mpy solution.mpy
identity_status=$?
if (( identity_status != 0 )); then
  overall=1
fi

sha256sum regenerated-solution.mpy solution.mpy
printf 'translator_exit=%d\n' "$translator_status"
printf 'byte_identity_cmp_exit=%d\n' "$identity_status"

python3 "$evidence/stage2_differential.py" \
  --inputs-json "$evidence/stage2-inputs.json"
differential_status=$?
if (( differential_status != 0 )); then
  overall=1
fi
printf 'differential_exit=%d\n' "$differential_status"

exit "$overall"
