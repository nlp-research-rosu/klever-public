#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/153-strongest-extension
labels=(
  prompt_worked
  prompt_tie
  later_stronger
  uncased_characters
  empty_first
  all_negative
  singleton
)
overall=0

for label in "${labels[@]}"; do
  log="/audit-output/evidence/stage3/kprove-${label}.log"
  echo "\$ kprove spec-labeled.k --definition verification-kompiled --spec-module SPECLABELED --claims $label" \
    | tee "$log"
  kprove "$scratch/spec-labeled.k" \
    --definition "$scratch/verification-kompiled" \
    --spec-module SPECLABELED \
    --claims "$label" 2>&1 | tee -a "$log"
  status=${PIPESTATUS[0]}
  echo "exit_status=$status" | tee -a "$log"
  if [[ $status -ne 0 ]] || ! rg -q '^#Top$' "$log"; then
    overall=1
  fi
done

exit "$overall"
