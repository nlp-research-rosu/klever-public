#!/usr/bin/env bash
set -u

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

printf '%s\n' '$ python3 /reference/py2mpy.py /tmp/audit-work/candidate/solution.py > /tmp/audit-work/regenerated-solution.mpy'
python3 /reference/py2mpy.py /tmp/audit-work/candidate/solution.py \
  > /tmp/audit-work/regenerated-solution.mpy
status=$?
printf '[exit %d]\n' "$status"
if (( status != 0 )); then
  exit "$status"
fi

run cmp -- /tmp/audit-work/regenerated-solution.mpy /tmp/audit-work/candidate/solution.mpy
run sha256sum /tmp/audit-work/regenerated-solution.mpy /tmp/audit-work/candidate/solution.mpy
run python3 /audit-output/evidence/differential_test.py
