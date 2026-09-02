#!/usr/bin/env bash
set -u

SCRATCH=/tmp/audit-work/anti-shuffle-audit
EVIDENCE=/audit-output/evidence
overall=0

run_logged() {
  output=$1
  shift
  printf 'COMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@" > "$output" 2>&1
  status=$?
  printf 'EXIT: %d\n' "$status"
  printf 'OUTPUT: %s\n\n' "$output"
  return "$status"
}

run_logged "$EVIDENCE/12_vacuity_dry_run.log" \
  kprove "$EVIDENCE/12_spec_vacuity.k" \
  --definition "$SCRATCH/verification-kompiled" \
  --spec-module AUDIT-VACUITY \
  --claims SPEC.insertion-loop,SPEC.character-loop,AUDIT-VACUITY.false-empty-result \
  --trusted SPEC.insertion-loop,SPEC.character-loop \
  --dry-run
dry_status=$?
if [ "$dry_status" -ne 0 ]; then
  overall=1
fi

run_logged "$EVIDENCE/12_vacuity_proof.log" \
  kprove "$EVIDENCE/12_spec_vacuity.k" \
  --definition "$SCRATCH/verification-kompiled" \
  --spec-module AUDIT-VACUITY \
  --claims SPEC.insertion-loop,SPEC.character-loop,AUDIT-VACUITY.false-empty-result \
  --trusted SPEC.insertion-loop,SPEC.character-loop
proof_status=$?

stuck_count=$(grep -c 'WarnStuckClaimState' "$EVIDENCE/12_vacuity_proof.log" || true)
actual_empty_count=$(grep -F -c 'str ( .IntSeq )' "$EVIDENCE/12_vacuity_proof.log" || true)
expected_bang_count=$(grep -F -c 'str(iCons(33, .IntSeq))' "$EVIDENCE/12_spec_vacuity.k" || true)
printf 'EXPECTED_PROOF_FAILURE_EXIT_NONZERO: %d\n' "$proof_status"
printf 'STUCK_WARNING_COUNT: %d\n' "$stuck_count"
printf 'ACTUAL_EMPTY_MARKER_COUNT: %d\n' "$actual_empty_count"
printf 'EXPECTED_BANG_MARKER_COUNT: %d\n' "$expected_bang_count"

if [ "$proof_status" -eq 0 ] || [ "$stuck_count" -lt 1 ]; then
  overall=1
fi

exit "$overall"
