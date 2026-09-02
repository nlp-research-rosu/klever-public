#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/candidate
verification_definition=/tmp/audit-work/runs/verification-kompiled
spec_file="$scratch/isolated-specs.k"
overall_status=0

run_claim() {
  local module="$1"
  echo "COMMAND[$module]: kprove $spec_file --definition $verification_definition --spec-module $module"
  kprove "$spec_file" \
    --definition "$verification_definition" \
    --spec-module "$module"
  local claim_status=$?
  echo "EXIT[$module]: $claim_status"
  if [[ "$claim_status" -ne 0 ]]; then
    overall_status=1
  fi
}

run_claim AUDIT-SPEC-EXAMPLE
run_claim AUDIT-SPEC-INCREASING
run_claim AUDIT-SPEC-SINGLE

echo "INDIVIDUAL_CLAIMS_OVERALL_EXIT=$overall_status"
exit "$overall_status"
