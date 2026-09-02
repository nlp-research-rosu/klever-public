#!/usr/bin/env bash
set -u

work=/tmp/audit-work/87-get-row-review

run() {
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf 'EXIT: %d\n' "$status"
  return "$status"
}

cd "$work" || exit 1
printf 'COMMAND: python3 trusted_py2mpy.py solution.py > regenerated-solution.mpy\n'
python3 trusted_py2mpy.py solution.py > regenerated-solution.mpy
translation_status=$?
printf 'EXIT: %d\n' "$translation_status"
if [ "$translation_status" -ne 0 ]; then
  exit "$translation_status"
fi
printf 'COMMAND: cmp -s regenerated-solution.mpy solution.mpy\n'
cmp -s regenerated-solution.mpy solution.mpy
status=$?
printf 'EXIT: %d\n' "$status"
if [ "$status" -ne 0 ]; then
  diff -u solution.mpy regenerated-solution.mpy
  exit "$status"
fi
run python3 /audit-output/evidence/differential.py
exit $?
