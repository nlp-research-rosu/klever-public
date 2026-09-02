#!/usr/bin/env bash
set -u

cd /tmp/audit-work/proof || exit 90

run() {
  printf '\nCOMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf 'EXIT_STATUS: %s\n' "$status"
  return "$status"
}

printf '%s\n' 'CONTRACT: For any string containing only "(" and ")", return true exactly when no prefix has more closing than opening parentheses and the final counts are equal.'
printf '%s\n' 'COMMAND: python3 /reference/py2mpy.py /tmp/audit-work/proof/solution.py > /tmp/audit-work/proof/regenerated.mpy'
python3 /reference/py2mpy.py /tmp/audit-work/proof/solution.py > /tmp/audit-work/proof/regenerated.mpy
status=$?
printf 'EXIT_STATUS: %s\n' "$status"
test "$status" -eq 0 || exit "$status"

run sha256sum solution.mpy regenerated.mpy || exit $?
run cmp -s solution.mpy regenerated.mpy || exit $?
printf '%s\n' 'BYTE_IDENTITY: submitted solution.mpy exactly equals trusted regeneration'
run python3 /audit-output/evidence/differential_test.py || exit $?
