#!/usr/bin/env bash
set -uo pipefail

evidence_dir=/audit-output/evidence
mutation_dir=/tmp/audit-work/88-sort-array/body-mutation
definition="$mutation_dir/verification-mutant-kompiled"
log_file="$evidence_dir/body_sensitivity.log"

run() {
  local command_text=$1
  printf '\n$ %s\n' "$command_text"
  bash -o pipefail -c "$command_text"
  local status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

{
  if [[ -d "$definition" ]]; then
    run "rm -rf -- $definition" || exit $?
  fi
  run "diff -u /tmp/audit-work/88-sort-array/verification.k $mutation_dir/verification.k" || diff_status=$?
  if [[ ${diff_status:-0} -ne 1 ]]; then
    printf 'unexpected diff status: %d\n' "${diff_status:-0}"
    exit 90
  fi
  run "kompile $mutation_dir/verification.k --backend haskell --main-module VERIFICATION --syntax-module VERIFICATION --output-definition $definition" || exit $?
  run "kprove $mutation_dir/spec-labeled.k --definition $definition --spec-module SPEC-LABELED --claims odd"
  proof_status=$?
  if [[ "$proof_status" -eq 0 ]]; then
    printf 'BODY_SENSITIVITY=UNEXPECTED_PROOF_SUCCESS\n'
    exit 91
  fi
  printf 'BODY_SENSITIVITY=EXPECTED_PROOF_FAILURE kprove_exit=%d\n' "$proof_status"
} 2>&1 | tee "$log_file"
status=${PIPESTATUS[0]}
printf 'SCRIPT_EXIT=%d\n' "$status" | tee -a "$log_file"
exit "$status"
