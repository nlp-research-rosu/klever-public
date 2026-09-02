#!/usr/bin/env bash
set -u

WORK=/tmp/audit-work/reconstruction

run() {
  printf '\nCOMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  rc=$?
  printf 'EXIT_STATUS: %d\n' "$rc"
  return 0
}

printf 'TRUSTED_TRANSLATION\n'
printf 'COMMAND: python3 %q %q > %q\n' \
  "$WORK/trusted/py2mpy.py" "$WORK/solution.py" "$WORK/regenerated-solution.mpy"
python3 "$WORK/trusted/py2mpy.py" "$WORK/solution.py" \
  > "$WORK/regenerated-solution.mpy"
rc=$?
printf 'EXIT_STATUS: %d\n' "$rc"
run cmp "$WORK/regenerated-solution.mpy" "$WORK/solution.mpy"
run sha256sum "$WORK/regenerated-solution.mpy" "$WORK/solution.mpy"

printf '\nPYTHON_SYNTAX_AND_DIFFERENTIAL\n'
run python3 -m py_compile "$WORK/solution.py" "$WORK/trusted/canonical.py"
run python3 /audit-output/evidence/differential.py
