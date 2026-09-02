#!/usr/bin/env bash
set -u

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return 0
}

cd /tmp/audit-work/reconstruction || exit 125
printf '%s\n' '$ python3 trusted-py2mpy.py solution.py > regenerated-solution.mpy'
python3 trusted-py2mpy.py solution.py > regenerated-solution.mpy
printf '[exit %d]\n' "$?"
run cmp -s solution.mpy regenerated-solution.mpy
run sha256sum solution.mpy regenerated-solution.mpy
run python3 /audit-output/evidence/differential_test.py
