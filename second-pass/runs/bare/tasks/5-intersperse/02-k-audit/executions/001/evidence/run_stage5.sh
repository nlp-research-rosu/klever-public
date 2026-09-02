#!/usr/bin/env bash
set -u

log="/audit-output/evidence/stage5-static-and-sensitivity.log"
scratch="/tmp/audit-work/reconstruction"
exec >"$log" 2>&1

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return 0
}

run nl -ba "$scratch/semantic.k"
run nl -ba "$scratch/verification.k"
run nl -ba "$scratch/spec.k"
run rg -n '\[(function|total|functional|simplification|concrete|priority|owise|anywhere|macro|alias)' "$scratch/semantic.k" "$scratch/verification.k" "$scratch/spec.k"
run rg -n '^[[:space:]]*rule([[:space:]]|$)' "$scratch/semantic.k" "$scratch/verification.k"
run kprove "$scratch/spec-body-mutation.k" --definition "$scratch/verification-fresh-kompiled" --spec-module SPEC-BODY-MUTATION --dry-run
run kprove "$scratch/spec-body-mutation.k" --definition "$scratch/verification-fresh-kompiled" --spec-module SPEC-BODY-MUTATION
