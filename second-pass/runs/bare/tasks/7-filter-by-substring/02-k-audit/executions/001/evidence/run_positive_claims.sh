#!/usr/bin/env bash

# Re-run each submitted positive claim independently against the fresh
# reviewer-built Haskell definition.
set +e

scratch=/tmp/audit-work/7-filter-by-substring
evidence=/audit-output/evidence
runner=$evidence/run_logged.sh
claims=(
  UNIVERSAL-PROGRAM-REDUCTION
  UNIVERSAL-BASE
  UNIVERSAL-STEP-KEEP
  UNIVERSAL-STEP-DROP
  EMPTY-EXAMPLE
  PROMPT-EXAMPLE
)

overall=0
summary=$evidence/stage3-positive-claims-summary.log
printf 'FRESH_DEFINITION: %s\n' "$scratch/verification-haskell-kompiled" > "$summary"

for claim in "${claims[@]}"; do
  log=$evidence/stage3-kprove-$claim.log
  "$runner" "$log" \
    kprove "$scratch/spec.k" \
    --definition "$scratch/verification-haskell-kompiled" \
    --spec-module SPEC \
    --claims "$claim"
  status=$?
  top_count=$(grep -c '^#Top$' "$log")
  printf '%s exit=%d top_count=%d log=%s\n' \
    "$claim" "$status" "$top_count" "$log" >> "$summary"
  if (( status != 0 || top_count == 0 )); then
    overall=1
  fi
done

printf 'OVERALL_EXIT_STATUS: %d\n' "$overall" >> "$summary"
exit "$overall"
