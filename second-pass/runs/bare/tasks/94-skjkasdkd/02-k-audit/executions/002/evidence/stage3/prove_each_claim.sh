#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/candidate-clean
definition="$scratch/audit-verification-kompiled"
spec="$scratch/spec-labeled.k"
labels=(prime-from prime choose largest digit-sum entry)
overall=0

for label in "${labels[@]}"; do
  printf 'CLAIM: SPEC-LABELED.%s\n' "$label"
  printf 'COMMAND: kprove %q --definition %q --spec-module SPEC-LABELED --claims %q\n' \
    "$spec" "$definition" "SPEC-LABELED.$label"
  kprove "$spec" \
    --definition "$definition" \
    --spec-module SPEC-LABELED \
    --claims "SPEC-LABELED.$label"
  claim_status=$?
  printf 'CLAIM_EXIT_STATUS: %d\n\n' "$claim_status"
  if (( claim_status != 0 )); then
    overall=$claim_status
  fi
done

exit "$overall"
