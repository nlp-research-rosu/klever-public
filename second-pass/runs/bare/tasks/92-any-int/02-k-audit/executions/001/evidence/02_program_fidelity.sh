#!/usr/bin/env bash
set -u

log=/audit-output/evidence/02_program_fidelity.log
exec > >(tee "$log") 2>&1

run() {
  printf '\nCOMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf 'EXIT_STATUS: %d\n' "$status"
  return 0
}

printf 'AUDIT_STAGE: 2 program fidelity and differential behavior\n'
run python3 /tmp/audit-work/92-any-int/trusted/py2mpy.py /tmp/audit-work/92-any-int/src/solution.py
python3 /tmp/audit-work/92-any-int/trusted/py2mpy.py \
  /tmp/audit-work/92-any-int/src/solution.py \
  > /tmp/audit-work/92-any-int/generated/solution.regenerated.mpy
translation_status=$?
printf 'COMMAND: python3 trusted/py2mpy.py src/solution.py > generated/solution.regenerated.mpy\n'
printf 'EXIT_STATUS: %d\n' "$translation_status"
run cmp -s /tmp/audit-work/92-any-int/generated/solution.regenerated.mpy /tmp/audit-work/92-any-int/src/solution.mpy
run sha256sum /tmp/audit-work/92-any-int/generated/solution.regenerated.mpy /tmp/audit-work/92-any-int/src/solution.mpy
run python3 /audit-output/evidence/02_differential.py
