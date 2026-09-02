#!/usr/bin/env bash
set -uo pipefail

cd /tmp/audit-work/132-is-nested-review || exit 90

run_and_record() {
  echo "\$ $*"
  "$@"
  local status=$?
  echo "EXIT_STATUS: ${status}"
  return "${status}"
}

run_and_record python3 py2mpy.py solution.py

echo '$ python3 py2mpy.py solution.py > regenerated-solution.mpy'
python3 py2mpy.py solution.py > regenerated-solution.mpy
regen_status=$?
echo "EXIT_STATUS: ${regen_status}"

run_and_record cmp regenerated-solution.mpy solution.mpy
run_and_record sha256sum regenerated-solution.mpy solution.mpy
run_and_record python3 /audit-output/evidence/differential_test.py
