#!/usr/bin/env bash
set -u

definition=${1:-verification-kompiled-audit}
evidence_dir=/audit-output/evidence
recorder="$evidence_dir/record-command.sh"

claims=(
  number-value-zero
  number-value-one
  number-value-two
  number-value-three
  number-value-four
  number-value-five
  number-value-six
  number-value-seven
  number-value-eight
  number-value-nine
  sort-numbers
)

overall_status=0
for claim in "${claims[@]}"; do
  log_path="$evidence_dir/07-kprove-${claim}.log"
  "$recorder" "$log_path" \
    kprove spec.k \
      --definition "$definition" \
      --spec-module SPEC \
      --claims "SPEC.$claim"
  status=$?
  top_count=$(grep -c '^#Top$' "$log_path" || true)
  printf 'CLAIM %s STATUS %d TOP_COUNT %d\n' "$claim" "$status" "$top_count"
  if (( status != 0 || top_count != 1 )); then
    overall_status=1
  fi
done

printf 'POSITIVE_CLAIM_COUNT %d\n' "${#claims[@]}"
printf 'OVERALL_STATUS %d\n' "$overall_status"
exit "$overall_status"
