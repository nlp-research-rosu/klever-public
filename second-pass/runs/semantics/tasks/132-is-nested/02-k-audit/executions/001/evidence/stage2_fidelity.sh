#!/usr/bin/env bash
set -u

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local command_status=$?
  printf '[exit %d]\n' "$command_status"
  return 0
}

cd /tmp/audit-work/132-is-nested/source || exit 99

printf '$ python3 py2mpy.py solution.py > regenerated-solution.mpy\n'
python3 py2mpy.py solution.py > regenerated-solution.mpy
translation_status=$?
printf '[exit %d]\n' "$translation_status"
run cmp -s regenerated-solution.mpy solution.mpy
run sha256sum regenerated-solution.mpy solution.mpy
run python3 /audit-output/evidence/differential.py
