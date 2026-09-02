#!/usr/bin/env bash
set +e

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  rc=$?
  printf 'EXIT_STATUS=%d\n' "$rc"
  return "$rc"
}

printf 'STAGE 2 PROGRAM FIDELITY AND DIFFERENTIAL CHECKS\n'
printf '$ python3 /reference/py2mpy.py /tmp/audit-work/candidate-src/solution.py > /tmp/audit-work/regenerated-solution.mpy\n'
python3 /reference/py2mpy.py /tmp/audit-work/candidate-src/solution.py > /tmp/audit-work/regenerated-solution.mpy
printf 'EXIT_STATUS=%d\n' "$?"
run cmp /tmp/audit-work/regenerated-solution.mpy /tmp/audit-work/candidate-src/solution.mpy
run sha256sum /tmp/audit-work/regenerated-solution.mpy /tmp/audit-work/candidate-src/solution.mpy
run python3 /audit-output/evidence/differential_test.py \
  /reference/canonical.py \
  /tmp/audit-work/candidate-src/solution.py \
  /audit-output/evidence/differential-inputs.json
