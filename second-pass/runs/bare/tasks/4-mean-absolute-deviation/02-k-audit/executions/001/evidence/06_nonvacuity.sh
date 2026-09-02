#!/usr/bin/env bash
set -u
set -o pipefail

scratch=/tmp/audit-work/reconstruction
mutation_output=/tmp/audit-work/06_mutation_proof_output.txt

run() {
  local description="$1"
  shift
  printf '\nCOMMAND (%s):' "$description"
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf 'EXIT STATUS: %d\n' "$status"
  return "$status"
}

printf 'AUDIT STAGE 6: fresh false-result non-vacuity mutation\n'

run "copy reviewer-authored mutation into scratch" \
  cp /audit-output/evidence/06_spec_vacuity.k "$scratch/spec-vacuity.k"
copy_status=$?

run "mutation parses and builds to KORE without proving" \
  kprove "$scratch/spec-vacuity.k" \
    --definition "$scratch/verification-kompiled" \
    --spec-module SPEC-VACUITY \
    --dry-run
dry_run_status=$?

printf '\nCOMMAND (prove deliberately false result): kprove %q --definition %q --spec-module SPEC-VACUITY\n' \
  "$scratch/spec-vacuity.k" "$scratch/verification-kompiled"
kprove "$scratch/spec-vacuity.k" \
  --definition "$scratch/verification-kompiled" \
  --spec-module SPEC-VACUITY \
  2>&1 | tee "$mutation_output"
proof_status=${PIPESTATUS[0]}
printf 'EXIT STATUS: %d\n' "$proof_status"

run "failure contains expected stuck-claim diagnostic" \
  rg -n 'WarnStuckClaimState|cannot be rewritten further|implication check.*failed' \
    "$mutation_output"
diagnostic_status=$?

printf '\nMUTATION STATUS SUMMARY\n'
printf 'copy=%d dry_run=%d false_proof=%d diagnostic=%d\n' \
  "$copy_status" "$dry_run_status" "$proof_status" "$diagnostic_status"

if (( copy_status || dry_run_status || diagnostic_status )); then
  exit 1
fi
if (( proof_status == 0 )); then
  printf 'ERROR: false mutation unexpectedly closed\n'
  exit 2
fi
printf 'EXPECTED NON-ZERO PROOF REJECTION OBSERVED\n'

