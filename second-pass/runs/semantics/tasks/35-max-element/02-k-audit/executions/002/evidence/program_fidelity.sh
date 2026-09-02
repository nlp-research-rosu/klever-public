#!/usr/bin/env bash
set -u

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

cd /tmp/audit-work/work || exit 2
run python3 py2mpy.py solution.py
run python3 py2mpy.py solution.py
python3 py2mpy.py solution.py > regenerated-solution.mpy
regen_status=$?
printf '[regeneration exit %d]\n' "$regen_status"
run cmp -s regenerated-solution.mpy solution.mpy
run sha256sum regenerated-solution.mpy solution.mpy
run diff -u solution.mpy regenerated-solution.mpy
run python3 /audit-output/evidence/differential_test.py
