#!/usr/bin/env bash
set -u

record() {
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf 'EXIT_STATUS: %d\n\n' "$status"
  return "$status"
}

overall=0
work=/tmp/audit-work/124-valid-date

record cp \
  /audit-output/evidence/06_spec_false.k \
  "$work/spec-audit-false.k" \
  || overall=1

record kprove "$work/spec-audit-false.k" \
  --definition "$work/verification-fresh-kompiled" \
  --spec-module AUDIT-SPEC-FALSE \
  --dry-run \
  || overall=1

printf 'COMMAND: kprove %q --definition %q --spec-module AUDIT-SPEC-FALSE\n' \
  "$work/spec-audit-false.k" \
  "$work/verification-fresh-kompiled"
set +e
kprove "$work/spec-audit-false.k" \
  --definition "$work/verification-fresh-kompiled" \
  --spec-module AUDIT-SPEC-FALSE \
  2>&1 | tee /audit-output/evidence/06_false_proof_output.log
proof_status=${PIPESTATUS[0]}
set -e
printf 'EXIT_STATUS: %d\n\n' "$proof_status"
if (( proof_status == 0 )); then
  overall=1
fi

record rg -q WarnStuckClaimState \
  /audit-output/evidence/06_false_proof_output.log \
  || overall=1
record rg -n '<k>|true|false|implication check' \
  /audit-output/evidence/06_false_proof_output.log \
  || overall=1

printf 'EXPECTED_NONZERO_PROOF_STATUS: %d\n' "$proof_status"
printf 'OVERALL_STATUS: %d\n' "$overall"
exit "$overall"
