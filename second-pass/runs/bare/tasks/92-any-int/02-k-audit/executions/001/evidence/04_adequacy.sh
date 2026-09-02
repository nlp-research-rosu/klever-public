#!/usr/bin/env bash
set -u

log=/audit-output/evidence/04_adequacy.log
failures=0
exec > >(tee "$log") 2>&1

run() {
  printf '\nCOMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf 'EXIT_STATUS: %d\n' "$status"
  if [ "$status" -ne 0 ]; then
    failures=$((failures + 1))
  fi
}

printf 'AUDIT_STAGE: 4 adequacy and real-program pinning\n'
run cmp -s \
  /tmp/audit-work/92-any-int/generated/submitted-program.kore \
  /tmp/audit-work/92-any-int/generated/wrapper-program.kore
run sha256sum \
  /tmp/audit-work/92-any-int/generated/submitted-program.kore \
  /tmp/audit-work/92-any-int/generated/wrapper-program.kore
run python3 /audit-output/evidence/04_claim_witnesses.py
printf '\nESSENTIAL_FAILURES: %d\n' "$failures"
exit "$failures"
