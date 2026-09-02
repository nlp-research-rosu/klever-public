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
  if [ "$rc" -ne 0 ]; then
    status=1
  fi
}

printf 'STAGE 2 PROGRAM FIDELITY AND DIFFERENTIAL\n'
run sed -n 1,120p /reference/prompt.py
run sed -n 1,160p /reference/canonical.py
run sed -n 1,160p /candidate/solution.py
run python3 /reference/py2mpy.py /candidate/solution.py

printf '\n$ python3 /reference/py2mpy.py /candidate/solution.py > /tmp/audit-work/reconstruction/solution.regenerated.mpy\n'
python3 /reference/py2mpy.py /candidate/solution.py > /tmp/audit-work/reconstruction/solution.regenerated.mpy
rc=$?
printf '[exit %d]\n' "$rc"
if [ "$rc" -ne 0 ]; then
  status=1
fi
run cmp -s /tmp/audit-work/reconstruction/solution.regenerated.mpy /candidate/solution.mpy
run sha256sum /tmp/audit-work/reconstruction/solution.regenerated.mpy /candidate/solution.mpy
run python3 /audit-output/evidence/differential_stage2.py

exit "$status"
