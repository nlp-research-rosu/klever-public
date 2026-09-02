#!/usr/bin/env bash
set -uo pipefail

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf 'EXIT STATUS: %d\n' "$status"
  return "$status"
}

printf '$ python3 /reference/py2mpy.py solution.py > regenerated-solution.mpy\n'
python3 /reference/py2mpy.py solution.py > regenerated-solution.mpy
translation_status=$?
printf 'EXIT STATUS: %d\n' "$translation_status"

run cmp -s regenerated-solution.mpy solution.mpy
comparison_status=$?
run sha256sum regenerated-solution.mpy solution.mpy

run python3 /audit-output/evidence/differential_factorize.py
differential_status=$?

printf 'TRANSLATION_BYTE_IDENTITY=%s\n' \
  "$([[ "$translation_status" == 0 && "$comparison_status" == 0 ]] && printf PASS || printf FAIL)"
printf 'DIFFERENTIAL_EXIT_STATUS=%d\n' "$differential_status"

if (( translation_status != 0 || comparison_status != 0 )); then
  exit 1
fi
exit 0
