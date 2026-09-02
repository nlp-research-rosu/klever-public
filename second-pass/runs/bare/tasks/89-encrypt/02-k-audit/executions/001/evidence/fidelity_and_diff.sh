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

cd /tmp/audit-work/source || exit 99
run python3 /reference/py2mpy.py solution.py

printf '$ python3 /reference/py2mpy.py solution.py > /tmp/audit-work/source/regenerated-solution.mpy\n'
python3 /reference/py2mpy.py solution.py > /tmp/audit-work/source/regenerated-solution.mpy
regen_status=$?
printf '[exit %d]\n' "$regen_status"
run cmp -s /tmp/audit-work/source/regenerated-solution.mpy /candidate/solution.mpy
run sha256sum /tmp/audit-work/source/regenerated-solution.mpy /candidate/solution.mpy
run python3 /audit-output/evidence/differential_test.py

exit "$regen_status"
