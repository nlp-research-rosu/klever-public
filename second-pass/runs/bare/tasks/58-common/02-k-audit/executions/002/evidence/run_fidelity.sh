#!/usr/bin/env bash
set -u -o pipefail

scratch=/tmp/audit-work/58-common-audit

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

overall=0
printf '\n$ python3 %q %q > %q\n' \
  "$scratch/trusted/py2mpy.py" \
  "$scratch/candidate/solution.py" \
  "$scratch/regenerated.mpy"
python3 "$scratch/trusted/py2mpy.py" \
  "$scratch/candidate/solution.py" > "$scratch/regenerated.mpy"
status=$?
printf '[exit %d]\n' "$status"
if [[ "$status" -ne 0 ]]; then overall=1; fi
run cmp "$scratch/regenerated.mpy" "$scratch/candidate/solution.mpy" || overall=1
run sha256sum "$scratch/regenerated.mpy" \
  "$scratch/candidate/solution.mpy" || overall=1
run python3 /audit-output/evidence/differential_test.py || overall=1
printf '\nOVERALL_EXIT=%d\n' "$overall"
exit "$overall"
