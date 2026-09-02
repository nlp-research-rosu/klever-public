#!/usr/bin/env bash
set -u

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf 'EXIT_STATUS=%s\n' "$status"
  return "$status"
}

printf 'FRESH_SCRATCH_SOURCE=/tmp/audit-work/audit-113\n'
printf '$ python3 /reference/py2mpy.py /tmp/audit-work/audit-113/solution.py > /tmp/audit-work/audit-113/regenerated-solution.mpy\n'
python3 /reference/py2mpy.py /tmp/audit-work/audit-113/solution.py > /tmp/audit-work/audit-113/regenerated-solution.mpy
translator_status=$?
printf 'EXIT_STATUS=%s\n' "$translator_status"
if test "$translator_status" -ne 0; then
  exit "$translator_status"
fi
run cmp /tmp/audit-work/audit-113/regenerated-solution.mpy /tmp/audit-work/audit-113/solution.mpy
cmp_status=$?
run sha256sum /tmp/audit-work/audit-113/regenerated-solution.mpy /tmp/audit-work/audit-113/solution.mpy
exit "$cmp_status"
