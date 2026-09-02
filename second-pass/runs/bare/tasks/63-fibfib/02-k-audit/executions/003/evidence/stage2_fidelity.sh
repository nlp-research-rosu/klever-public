#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/63-fibfib
candidate_src="$scratch/candidate-src"
trusted="$scratch/trusted"
regenerated="$candidate_src/solution.trusted-regenerated.mpy"
overall=0

printf '%s\n' \
  'COMMAND: python3 /tmp/audit-work/63-fibfib/trusted/py2mpy.py solution.py > solution.trusted-regenerated.mpy'
(
  cd "$candidate_src" || exit 125
  python3 "$trusted/py2mpy.py" solution.py > "$regenerated"
)
translate_status=$?
printf 'EXIT: %s\n' "$translate_status"
if (( translate_status != 0 )); then overall=1; fi

printf '%s\n' \
  'COMMAND: cmp --silent solution.mpy solution.trusted-regenerated.mpy'
cmp --silent "$candidate_src/solution.mpy" "$regenerated"
cmp_status=$?
printf 'EXIT: %s\n' "$cmp_status"
if (( cmp_status != 0 )); then
  overall=1
  diff -u "$candidate_src/solution.mpy" "$regenerated"
fi

sha256sum "$candidate_src/solution.mpy" "$regenerated"

printf '%s\n' \
  'COMMAND: python3 /audit-output/evidence/differential_test.py /tmp/audit-work/63-fibfib/trusted/canonical.py /tmp/audit-work/63-fibfib/candidate-src/solution.py'
python3 /audit-output/evidence/differential_test.py \
  "$trusted/canonical.py" "$candidate_src/solution.py"
differential_status=$?
printf 'EXIT: %s\n' "$differential_status"
if (( differential_status != 0 )); then overall=1; fi

printf 'STAGE2_EXIT: %s\n' "$overall"
exit "$overall"
