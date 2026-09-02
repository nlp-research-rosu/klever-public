#!/usr/bin/env bash
set -u

overall=0
run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  if [ "$status" -ne 0 ]; then
    overall=1
  fi
}

printf '%s\n' '$ python3 /tmp/audit-work/py2mpy.py /tmp/audit-work/solution.py > /tmp/audit-work/regenerated-solution.mpy'
python3 /tmp/audit-work/py2mpy.py /tmp/audit-work/solution.py \
  > /tmp/audit-work/regenerated-solution.mpy
status=$?
printf '[exit %d]\n' "$status"
if [ "$status" -ne 0 ]; then overall=1; fi

run cmp /tmp/audit-work/regenerated-solution.mpy /tmp/audit-work/submitted-solution.mpy
run sha256sum \
  /tmp/audit-work/regenerated-solution.mpy \
  /tmp/audit-work/submitted-solution.mpy
run python3 /audit-output/evidence/differential.py

printf '[script exit %d]\n' "$overall"
exit "$overall"
