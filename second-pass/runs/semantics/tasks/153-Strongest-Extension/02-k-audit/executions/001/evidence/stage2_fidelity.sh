#!/usr/bin/env bash
set -u

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return 0
}

printf '\n$ python3 /reference/py2mpy.py /candidate/solution.py > /tmp/audit-work/regenerated-solution.mpy\n'
python3 /reference/py2mpy.py /candidate/solution.py \
  > /tmp/audit-work/regenerated-solution.mpy
status=$?
printf '[exit %d]\n' "$status"
run cmp -s /tmp/audit-work/regenerated-solution.mpy /candidate/solution.mpy
run sha256sum /tmp/audit-work/regenerated-solution.mpy /candidate/solution.mpy
run python3 /audit-output/evidence/differential_test.py
