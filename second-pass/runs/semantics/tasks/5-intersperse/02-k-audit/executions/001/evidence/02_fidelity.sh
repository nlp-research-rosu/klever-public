#!/usr/bin/env bash
set +e

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return 0
}

printf '%s\n' 'Stage 2: translation identity and independent differential test'
run python3 /reference/py2mpy.py /tmp/audit-work/candidate/solution.py
python3 /reference/py2mpy.py /tmp/audit-work/candidate/solution.py \
  > /tmp/audit-work/regenerated-solution.mpy
regen_status=$?
printf '\n$ python3 /reference/py2mpy.py /tmp/audit-work/candidate/solution.py > /tmp/audit-work/regenerated-solution.mpy\n'
printf '[exit %d]\n' "$regen_status"
run cmp -s /tmp/audit-work/regenerated-solution.mpy /tmp/audit-work/candidate/solution.mpy
run sha256sum /tmp/audit-work/regenerated-solution.mpy /tmp/audit-work/candidate/solution.mpy
run diff -u /tmp/audit-work/candidate/solution.mpy /tmp/audit-work/regenerated-solution.mpy
run python3 /audit-output/evidence/02_differential.py
