#!/usr/bin/env bash
set -u

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

printf 'Regenerate solution.mpy with the trusted translator:\n'
printf '$ python3 /reference/py2mpy.py /tmp/audit-work/source/solution.py > /tmp/audit-work/source/regenerated-solution.mpy\n'
python3 /reference/py2mpy.py /tmp/audit-work/source/solution.py > /tmp/audit-work/source/regenerated-solution.mpy
status=$?
printf '[exit %d]\n' "$status"

printf '\nByte comparison with submitted solution.mpy:\n'
run cmp -s /tmp/audit-work/source/regenerated-solution.mpy /tmp/audit-work/source/solution.mpy
run sha256sum /tmp/audit-work/source/regenerated-solution.mpy /tmp/audit-work/source/solution.mpy

printf '\nIndependent differential test:\n'
run python3 /audit-output/evidence/differential_test.py
