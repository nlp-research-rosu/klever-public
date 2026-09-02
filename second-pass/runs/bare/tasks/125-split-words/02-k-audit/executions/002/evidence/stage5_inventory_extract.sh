#!/usr/bin/env bash
set -uo pipefail

files=(
  /tmp/audit-work/candidate/semantic.k
  /tmp/audit-work/candidate/verification.k
  /tmp/audit-work/candidate/spec.k
)

echo 'COMMAND: rg -n "^\s*(syntax|configuration|rule|claim)" semantic.k verification.k spec.k'
rg -n '^\s*(syntax|configuration|rule|claim)' "${files[@]}"
extract_status=$?
echo "EXIT_STATUS: $extract_status"

echo 'COMMAND: rg -n "\[(function|total|functional|simplification|simplifier|priority|owise|anywhere|macro)" semantic.k verification.k spec.k'
rg -n '\[(function|total|functional|simplification|simplifier|priority|owise|anywhere|macro)' \
  "${files[@]}"
attribute_status=$?
echo "EXIT_STATUS: $attribute_status"

rule_count=$(rg -c '^\s*rule\b' "${files[0]}" "${files[1]}" |
  awk -F: '{ total += $2 } END { print total + 0 }')
claim_count=$(rg -c '^\s*claim\b' "${files[2]}")
echo "LOCAL_RULE_COUNT: $rule_count"
echo "TARGET_CLAIM_COUNT: $claim_count"

if (( extract_status != 0 || attribute_status != 0 )); then
  exit 1
fi
if [[ "$rule_count" != 48 || "$claim_count" != 8 ]]; then
  exit 1
fi
