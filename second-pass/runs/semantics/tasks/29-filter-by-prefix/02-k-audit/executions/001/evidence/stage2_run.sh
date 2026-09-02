#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/29-filter-by-prefix
status=0

printf '%s\n' 'COMMAND: python3 /tmp/audit-work/29-filter-by-prefix/trusted/py2mpy.py /tmp/audit-work/29-filter-by-prefix/candidate-src/solution.py > /tmp/audit-work/29-filter-by-prefix/regenerated-solution.mpy'
python3 "$scratch/trusted/py2mpy.py" \
  "$scratch/candidate-src/solution.py" \
  > "$scratch/regenerated-solution.mpy"
rc=$?
printf 'EXIT: %d\n\n' "$rc"
(( rc == 0 )) || status=1

printf '%s\n' 'COMMAND: cmp -s /tmp/audit-work/29-filter-by-prefix/regenerated-solution.mpy /tmp/audit-work/29-filter-by-prefix/candidate-src/solution.mpy'
cmp -s "$scratch/regenerated-solution.mpy" "$scratch/candidate-src/solution.mpy"
rc=$?
printf 'EXIT: %d\n' "$rc"
if (( rc != 0 )); then
  diff -u "$scratch/candidate-src/solution.mpy" "$scratch/regenerated-solution.mpy" || true
  status=1
fi
printf '\n'

printf '%s\n' 'COMMAND: sha256sum regenerated-solution.mpy candidate-src/solution.mpy'
sha256sum "$scratch/regenerated-solution.mpy" "$scratch/candidate-src/solution.mpy"
rc=$?
printf 'EXIT: %d\n\n' "$rc"
(( rc == 0 )) || status=1

printf '%s\n' 'COMMAND: python3 /audit-output/evidence/differential_test.py'
python3 /audit-output/evidence/differential_test.py
rc=$?
printf 'EXIT: %d\n\n' "$rc"
(( rc == 0 )) || status=1

printf 'SCRIPT_EXIT: %d\n' "$status"
exit "$status"
