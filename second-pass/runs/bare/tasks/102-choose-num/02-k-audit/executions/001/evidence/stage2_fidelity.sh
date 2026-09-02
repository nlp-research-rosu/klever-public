#!/usr/bin/env bash
set -u

LOG=/audit-output/evidence/stage2-fidelity.log
exec > >(tee "$LOG") 2>&1

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

printf 'STAGE 2 PROGRAM FIDELITY AND DIFFERENTIAL TESTS\n'
status=0
printf '$ python3 /reference/py2mpy.py /tmp/audit-work/solution.py > /tmp/audit-work/regenerated.mpy\n'
python3 /reference/py2mpy.py /tmp/audit-work/solution.py \
  > /tmp/audit-work/regenerated.mpy
translate_status=$?
printf '[exit %d]\n' "$translate_status"
if (( translate_status != 0 )); then status=1; fi
run cmp -s /tmp/audit-work/regenerated.mpy /tmp/audit-work/solution.mpy || status=1
run sha256sum /tmp/audit-work/regenerated.mpy /tmp/audit-work/solution.mpy || status=1
run python3 /audit-output/evidence/differential_test.py || status=1
printf 'stage2_status=%d\n' "$status"
exit "$status"
