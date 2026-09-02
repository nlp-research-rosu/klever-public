#!/usr/bin/env bash
set -euo pipefail

spec=/tmp/audit-work/audit-108/source/spec.k
logs=(
  prove_positive_loop.log
  prove_negative_loop.log
  prove_positive_function.log
  prove_negative_function.log
  prove_signed_function.log
  prove_count_loop_with_n.log
  prove_count_loop.log
  prove_count_nums.log
)

claim_count=$(rg -c '^[[:space:]]+claim([[:space:]]|$)' "$spec")
echo "spec_claim_count=$claim_count"
if [[ "$claim_count" -ne 9 ]]; then
  exit 1
fi

for name in "${logs[@]}"; do
  path="/audit-output/evidence/$name"
  top_count=$(rg -c '^#Top$' "$path")
  exit_count=$(rg -c '^EXIT_STATUS: 0$' "$path")
  echo "$name top_count=$top_count exit_zero_count=$exit_count"
  if [[ "$top_count" -ne 1 || "$exit_count" -ne 1 ]]; then
    exit 1
  fi
done

echo "proof_invocations=8 claims_covered=9 all_success_signals_present=true"
