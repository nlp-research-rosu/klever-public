#!/usr/bin/env bash
set -u

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

overall=0
printf '\n$ python3 /reference/py2mpy.py /tmp/audit-work/candidate-src/solution.py > /tmp/audit-work/regenerated-solution.mpy\n'
python3 /reference/py2mpy.py \
  /tmp/audit-work/candidate-src/solution.py \
  > /tmp/audit-work/regenerated-solution.mpy
status=$?
printf '[exit %d]\n' "$status"
if (( status != 0 )); then
  overall=1
fi

run cmp -s \
  /tmp/audit-work/regenerated-solution.mpy \
  /tmp/audit-work/candidate-src/solution.mpy || overall=1

run sha256sum \
  /tmp/audit-work/regenerated-solution.mpy \
  /tmp/audit-work/candidate-src/solution.mpy

run python3 /audit-output/evidence/differential_test.py || overall=1

printf '\n[script exit %d]\n' "$overall"
exit "$overall"
