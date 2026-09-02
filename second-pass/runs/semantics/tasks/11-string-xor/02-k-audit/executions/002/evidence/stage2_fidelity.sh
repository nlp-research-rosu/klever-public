#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/11-string-xor

run() {
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf 'EXIT_STATUS: %s\n' "$status"
  return "$status"
}

printf 'COMMAND: python3 %q %q > %q\n' \
  "$scratch/trusted/py2mpy.py" \
  "$scratch/candidate/solution.py" \
  "$scratch/regenerated-solution.mpy"
python3 "$scratch/trusted/py2mpy.py" "$scratch/candidate/solution.py" \
  > "$scratch/regenerated-solution.mpy"
translate_status=$?
printf 'EXIT_STATUS: %s\n' "$translate_status"
if [ "$translate_status" -ne 0 ]; then
  exit "$translate_status"
fi

printf 'COMMAND: cmp -s regenerated-solution.mpy candidate/solution.mpy\n'
cmp -s "$scratch/regenerated-solution.mpy" "$scratch/candidate/solution.mpy"
cmp_status=$?
printf 'EXIT_STATUS: %s\n' "$cmp_status"
if [ "$cmp_status" -ne 0 ]; then
  exit "$cmp_status"
fi

run sha256sum \
  "$scratch/regenerated-solution.mpy" \
  "$scratch/candidate/solution.mpy" \
  "$scratch/candidate/solution.py" \
  "$scratch/trusted/canonical.py"
hash_status=$?
if [ "$hash_status" -ne 0 ]; then
  exit "$hash_status"
fi

run python3 /audit-output/evidence/differential_test.py
exit $?
