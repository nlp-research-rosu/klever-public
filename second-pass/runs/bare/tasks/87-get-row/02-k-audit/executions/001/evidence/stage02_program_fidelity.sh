#!/usr/bin/env bash
set -u

status=0
scratch=/tmp/audit-work/87-get-row

printf '%s\n' '$ python3 /reference/py2mpy.py source/solution.py > regenerated_solution.mpy'
python3 /reference/py2mpy.py "$scratch/source/solution.py" \
  > "$scratch/regenerated_solution.mpy"
rc=$?
printf 'translate_exit=%d\n' "$rc"
(( rc == 0 )) || status=1

printf '%s\n' '$ cmp regenerated_solution.mpy submitted solution.mpy'
cmp "$scratch/regenerated_solution.mpy" "$scratch/source/solution.mpy"
rc=$?
printf 'mpy_cmp_exit=%d\n' "$rc"
(( rc == 0 )) || status=1

printf '%s\n' '$ sha256sum regenerated and submitted MPY'
sha256sum "$scratch/regenerated_solution.mpy" "$scratch/source/solution.mpy"
rc=$?
printf 'sha_exit=%d\n' "$rc"
(( rc == 0 )) || status=1

printf '%s\n' '$ python3 /audit-output/evidence/differential_test.py'
python3 /audit-output/evidence/differential_test.py
rc=$?
printf 'differential_exit=%d\n' "$rc"
(( rc == 0 )) || status=1

printf 'overall_exit=%d\n' "$status"
exit "$status"
