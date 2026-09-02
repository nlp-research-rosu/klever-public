#!/usr/bin/env bash
set -uo pipefail

audit_work=/tmp/audit-work/111-histogram
proof_definition="$audit_work/verification-audit-kompiled"
overall_status=0

printf 'COMMAND: cp /audit-output/evidence/spec-vacuity.k %s/spec-vacuity.k\n' "$audit_work"
cp /audit-output/evidence/spec-vacuity.k "$audit_work/spec-vacuity.k"
command_status=$?
printf 'EXIT_STATUS: %s\n' "$command_status"
if (( command_status != 0 )); then overall_status=1; fi

printf 'SATISFYING_WITNESS: standard initial configuration with input ""\n'
printf 'PYTHON_FACT: candidate histogram("") == {}; canonical histogram("") == {}\n'

printf '%s\n' \
  "COMMAND: kprove --dry-run spec-vacuity.k --definition $proof_definition --spec-module HISTOGRAM-SPEC-VACUITY --warnings none"
(
  cd "$audit_work" &&
  kprove --dry-run spec-vacuity.k \
    --definition "$proof_definition" \
    --spec-module HISTOGRAM-SPEC-VACUITY \
    --warnings none
)
command_status=$?
printf 'MUTATION_BUILD_EXIT_STATUS: %s\n' "$command_status"
if (( command_status != 0 )); then overall_status=1; fi

printf '%s\n' \
  "COMMAND: kprove spec-vacuity.k --definition $proof_definition --spec-module HISTOGRAM-SPEC-VACUITY --claims HISTOGRAM-SPEC-VACUITY.false-empty-result --warnings none"
(
  cd "$audit_work" &&
  kprove spec-vacuity.k \
    --definition "$proof_definition" \
    --spec-module HISTOGRAM-SPEC-VACUITY \
    --claims HISTOGRAM-SPEC-VACUITY.false-empty-result \
    --warnings none 2>&1 | tee spec-vacuity-proof.raw.log
  proof_status=${PIPESTATUS[0]}
  printf 'EXPECTED_NONZERO_EXIT_STATUS: %s\n' "$proof_status"
  test "$proof_status" -ne 0 &&
    grep -q 'WarnStuckClaimState' spec-vacuity-proof.raw.log &&
    grep -q 'AssertionError' spec-vacuity-proof.raw.log &&
    grep -q '<exit-code>' spec-vacuity-proof.raw.log
)
command_status=$?
printf 'EXPECTED_FAILURE_VALIDATION_EXIT_STATUS: %s\n' "$command_status"
if (( command_status != 0 )); then overall_status=1; fi

exit "$overall_status"
