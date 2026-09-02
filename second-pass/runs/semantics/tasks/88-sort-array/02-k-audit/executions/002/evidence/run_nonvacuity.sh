#!/usr/bin/env bash
set -uo pipefail

evidence_dir=/audit-output/evidence
scratch_dir=/tmp/audit-work/88-sort-array
definition="$scratch_dir/verification-audit-kompiled"
log_file="$evidence_dir/nonvacuity.log"

run() {
  local command_text=$1
  printf '\n$ %s\n' "$command_text"
  bash -o pipefail -c "$command_text"
  local status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

{
  run "kprove $evidence_dir/spec-vacuity.k -I $scratch_dir --definition $definition --spec-module SPEC-VACUITY"
  proof_status=$?
  if [[ "$proof_status" -eq 0 ]]; then
    printf 'NONVACUITY=FAIL unexpected_false_claim_success\n'
    exit 91
  fi
  printf 'NONVACUITY=PASS expected_false_claim_failure kprove_exit=%d witness=[]\n' "$proof_status"
} 2>&1 | tee "$log_file"
status=${PIPESTATUS[0]}
printf 'SCRIPT_EXIT=%d\n' "$status" | tee -a "$log_file"
exit "$status"
