#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/121-solution-audit
status=0

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  rc=$?
  printf '[exit %d]\n' "$rc"
  if [ "$rc" -ne 0 ]; then
    status=1
  fi
}

printf '$ python3 %q %q > %q\n' \
  "$scratch/reference/py2mpy.py" \
  "$scratch/candidate/solution.py" \
  "$scratch/regenerated-solution.mpy"
python3 "$scratch/reference/py2mpy.py" "$scratch/candidate/solution.py" \
  > "$scratch/regenerated-solution.mpy"
rc=$?
printf '[exit %d]\n' "$rc"
if [ "$rc" -ne 0 ]; then
  status=1
fi

run cmp -- "$scratch/candidate/solution.mpy" "$scratch/regenerated-solution.mpy"
run sha256sum \
  "$scratch/candidate/solution.mpy" "$scratch/regenerated-solution.mpy"
run python3 /audit-output/evidence/differential_test.py

exit "$status"
