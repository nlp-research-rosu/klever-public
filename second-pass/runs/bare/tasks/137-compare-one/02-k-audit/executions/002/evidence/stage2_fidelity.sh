#!/usr/bin/env bash
set -uo pipefail

work=/tmp/audit-work/137-compare-one-audit

printf '%s\n' 'COMMAND: sha256sum trusted and candidate source artifacts'
sha256sum \
  /reference/canonical.py \
  "$work/trusted-canonical.py" \
  /candidate/solution.py \
  "$work/solution.py" \
  /reference/py2mpy.py \
  "$work/trusted-py2mpy.py"
status=$?
printf 'EXIT: %s\n' "$status"
(( status == 0 )) || exit "$status"

printf '%s\n' 'COMMAND: python3 trusted-py2mpy.py solution.py > regenerated-solution.mpy'
(
  cd "$work" &&
    python3 trusted-py2mpy.py solution.py > regenerated-solution.mpy
)
status=$?
printf 'EXIT: %s\n' "$status"
(( status == 0 )) || exit "$status"

printf '%s\n' 'COMMAND: cmp regenerated-solution.mpy solution.mpy'
cmp "$work/regenerated-solution.mpy" "$work/solution.mpy"
status=$?
printf 'EXIT: %s\n' "$status"
(( status == 0 )) || exit "$status"
sha256sum "$work/regenerated-solution.mpy" "$work/solution.mpy"

printf '%s\n' 'COMMAND: python3 -m py_compile solution.py trusted-canonical.py'
(
  cd "$work" &&
    python3 -m py_compile solution.py trusted-canonical.py
)
status=$?
printf 'EXIT: %s\n' "$status"
(( status == 0 )) || exit "$status"

printf '%s\n' 'COMMAND: python3 /audit-output/evidence/differential_test.py'
python3 /audit-output/evidence/differential_test.py
status=$?
printf 'EXIT: %s\n' "$status"
exit "$status"
