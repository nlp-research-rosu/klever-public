#!/usr/bin/env bash
set -uo pipefail

evidence_dir=/audit-output/evidence
bridge_dir=/tmp/audit-work/88-sort-array/bridge-free
definition="$bridge_dir/verification-bridge-free-kompiled"
bridge_definition=/tmp/audit-work/88-sort-array/verification-audit-kompiled
log_file="$evidence_dir/bridge_audit.log"

run() {
  local command_text=$1
  printf '\n$ %s\n' "$command_text"
  bash -o pipefail -c "$command_text"
  local status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

{
  run "diff -u /tmp/audit-work/88-sort-array/verification.k $bridge_dir/verification.k" || diff_status=$?
  if [[ ${diff_status:-0} -ne 1 ]]; then
    printf 'unexpected diff status: %d\n' "${diff_status:-0}"
    exit 90
  fi
  if [[ -d "$definition" ]]; then
    run "rm -rf -- $definition" || exit $?
  fi
  run "kompile $bridge_dir/verification.k --backend haskell --main-module VERIFICATION --syntax-module VERIFICATION --output-definition $definition" || exit $?

  for label in fixed-ground-empty-middle fixed-ground-one-middle; do
    run "kprove $evidence_dir/bridge-connection.k -I $bridge_dir --definition $definition --spec-module BRIDGE-CONNECTION --claims BRIDGE-CONNECTION.$label" || exit $?
  done
  for label in bridge-ground-empty-middle bridge-ground-one-middle; do
    run "kprove $evidence_dir/bridge-connection.k -I /tmp/audit-work/88-sort-array --definition $bridge_definition --spec-module BRIDGE-CONNECTION --claims BRIDGE-CONNECTION.$label" || exit $?
  done

  for label in reachable-domain complete-match-domain; do
    run "kprove $evidence_dir/bridge-connection.k -I $bridge_dir --definition $definition --spec-module BRIDGE-CONNECTION --claims BRIDGE-CONNECTION.$label"
    proof_status=$?
    if [[ "$proof_status" -eq 0 ]]; then
      printf 'BRIDGE_FREE_CONNECTION_%s=PROVED\n' "$label"
    else
      printf 'BRIDGE_FREE_CONNECTION_%s=NOT_PROVED kprove_exit=%d\n' "$label" "$proof_status"
    fi
  done
} 2>&1 | tee "$log_file"
status=${PIPESTATUS[0]}
printf 'SCRIPT_EXIT=%d\n' "$status" | tee -a "$log_file"
exit "$status"
