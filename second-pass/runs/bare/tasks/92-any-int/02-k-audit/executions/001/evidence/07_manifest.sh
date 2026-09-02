#!/usr/bin/env bash
set -u

log=/audit-output/evidence/07_manifest.log
exec > >(tee "$log") 2>&1
failures=0

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

printf 'AUDIT_STAGE: 7 evidence completeness and final-marker validation\n'
run find /audit-output/evidence -maxdepth 1 -type f -printf '%f\n'
run cmp -s \
  /audit-output/evidence/03_spec-individual.k \
  /tmp/audit-work/92-any-int/src/spec-individual.k
run cmp -s \
  /audit-output/evidence/05_solution-body-mutation.py \
  /tmp/audit-work/92-any-int/generated/solution-body-mutation.py
run cmp -s \
  /audit-output/evidence/06_spec-vacuity-audit.k \
  /tmp/audit-work/92-any-int/src/spec-vacuity-audit.k
run rg -n 'ESSENTIAL_FAILURES: 0' \
  /audit-output/evidence/03_reconstruct.log \
  /audit-output/evidence/04_adequacy.log
run rg -n 'BODY_SENSITIVITY_RESULT: PASS' \
  /audit-output/evidence/05_program_sensitivity.log
run rg -n 'NONVACUITY_RESULT: PASS' \
  /audit-output/evidence/06_nonvacuity.log
run bash -c 'test "$(tail -n 2 /audit-output/REVIEW.md)" = $'"'"'VERDICT: CONCERNS\nLEGITIMACY: LEGIT'"'"''
run bash -c 'find /audit-output/evidence -maxdepth 1 -type f ! -name 07_manifest.log -print0 | sort -z | xargs -0 sha256sum'

printf '\nMANIFEST_FAILURES: %d\n' "$failures"
exit "$failures"
