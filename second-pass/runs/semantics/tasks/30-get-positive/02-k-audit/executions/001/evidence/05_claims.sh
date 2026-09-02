#!/usr/bin/env bash
set -u

work=/tmp/audit-work/30-get-positive
failed=0

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf '[exit %d]\n' "$status"
  if test "$status" -ne 0; then
    failed=1
  fi
}

# Prove the auxiliary induction claim on its own.
run kprove "$work/spec.k" \
  --definition "$work/verification-kompiled" \
  --spec-module SPEC \
  --claims SPEC.filter-loop \
  --smt-timeout 10000

# Prove the entry target independently after admitting only the already
# independently proved induction claim as a staged lemma.
run kprove "$work/spec.k" \
  --definition "$work/verification-kompiled" \
  --spec-module SPEC \
  --claims SPEC.filter-loop,SPEC.get-positive-correct \
  --trusted SPEC.filter-loop \
  --smt-timeout 10000

# Re-run the submitted proof exactly as a joint, untrusted two-claim proof.
run kprove "$work/spec.k" \
  --definition "$work/verification-kompiled" \
  --spec-module SPEC \
  --smt-timeout 10000

exit "$failed"
