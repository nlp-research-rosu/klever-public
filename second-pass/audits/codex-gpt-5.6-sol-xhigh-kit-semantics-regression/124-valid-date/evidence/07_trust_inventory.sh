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

root=/tmp/audit-work/124-valid-date

record rg -n \
  'syntax .*\[(?:[^]]*(?:symbol\(|no-evaluators))' \
  "$root/reference-semantics/semantics"

record bash -c \
  'if rg -n "\[(?:[^]]*(?:simplification|functional))" /tmp/audit-work/124-valid-date/verification.k; then exit 1; else echo "NO_PROOF_LOCAL_SIMPLIFICATION_OR_FUNCTIONAL_DECLARATIONS"; fi'

record rg -n \
  'syntax .*\[function|^\s*rule ' \
  "$root/verification.k"

record rg -n \
  'Non exhaustive match detected|mapStrVS|floorFI|toF|ceilF|joinCodes|valSeqAt' \
  /audit-output/evidence/03_reconstruct.log
