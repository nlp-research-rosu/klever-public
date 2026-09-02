#!/usr/bin/env bash
set -uo pipefail

audit_work=/tmp/audit-work/130-tri-audit
claim_source=/audit-output/evidence/positive-claims
definition="$audit_work/verification-proof-kompiled"

declare -a claims=(
  eval-call
  run-entry
  value-zero
  value-one
  value-even
  value-odd-recurrence
)

overall_status=0

printf '\nCOMMAND: kprove spec.k --definition %s --spec-module TRI-SPEC\n' \
  "$definition"
(
  cd "$audit_work" || exit 2
  kprove spec.k \
    --definition "$definition" \
    --spec-module TRI-SPEC
)
full_spec_status=$?
printf 'UNMODIFIED_FULL_SPEC_EXIT_STATUS=%s\n' "$full_spec_status"
if [[ "$full_spec_status" -ne 0 ]]; then
  overall_status=1
fi

for claim_name in "${claims[@]}"; do
  claim_file="$claim_name.k"
  printf '\nCOMMAND: cp -p %s/%s %s/%s\n' \
    "$claim_source" "$claim_file" "$audit_work" "$claim_file"
  cp -p "$claim_source/$claim_file" "$audit_work/$claim_file"
  copy_status=$?
  printf 'COPY_EXIT_STATUS=%s\n' "$copy_status"
  if [[ "$copy_status" -ne 0 ]]; then
    overall_status=1
    continue
  fi

  module_name=$(
    sed -n 's/^module \(AUDIT-[A-Z-]*\)$/\1/p' "$audit_work/$claim_file"
  )
  printf 'COMMAND: kprove %s --definition %s --spec-module %s\n' \
    "$claim_file" "$definition" "$module_name"
  (
    cd "$audit_work" || exit 2
    kprove "$claim_file" \
      --definition "$definition" \
      --spec-module "$module_name"
  )
  prove_status=$?
  printf 'CLAIM=%s EXIT_STATUS=%s\n' "$claim_name" "$prove_status"
  if [[ "$prove_status" -ne 0 ]]; then
    overall_status=1
  fi
done

printf '\nALL_POSITIVE_CLAIMS_EXIT_STATUS=%s\n' "$overall_status"
exit "$overall_status"
