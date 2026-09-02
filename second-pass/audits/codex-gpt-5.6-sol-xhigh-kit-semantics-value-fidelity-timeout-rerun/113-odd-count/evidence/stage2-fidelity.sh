#!/usr/bin/env bash
set -u

status=0

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  rc=$?
  printf '[exit %d]\n' "$rc"
  if (( rc != 0 )); then
    status=1
  fi
}

cd /tmp/audit-work/source || exit 1

printf 'Stage 2: trusted translation and independent differential tests\n'

printf '\n$ python3 /reference/py2mpy.py /tmp/audit-work/source/solution.py > /tmp/audit-work/source/regenerated-solution.mpy\n'
python3 /reference/py2mpy.py /tmp/audit-work/source/solution.py \
  > /tmp/audit-work/source/regenerated-solution.mpy
rc=$?
printf '[exit %d]\n' "$rc"
if (( rc != 0 )); then status=1; fi

run cmp -s /tmp/audit-work/source/regenerated-solution.mpy /tmp/audit-work/source/solution.mpy
run sha256sum /tmp/audit-work/source/regenerated-solution.mpy /tmp/audit-work/source/solution.mpy
run python3 /audit-output/evidence/differential_test.py

printf '\nFinal stage2_status=%d\n' "$status"
exit "$status"
