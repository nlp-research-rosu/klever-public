#!/usr/bin/env bash
set -uo pipefail

work=/tmp/audit-work/137-compare-one-audit

printf '%s\n' 'COMMAND: sha256sum semantic.k verification.k spec.k'
sha256sum "$work/semantic.k" "$work/verification.k" "$work/spec.k"
status=$?
printf 'EXIT: %s\n' "$status"
(( status == 0 )) || exit "$status"

printf '%s\n' 'COMMAND: rg declaration/rule starts with line numbers'
rg -n \
  '^[[:space:]]*(requires|module|endmodule|imports|configuration|syntax|rule|claim)' \
  "$work/semantic.k" \
  "$work/verification.k" \
  "$work/spec.k"
status=$?
printf 'EXIT: %s\n' "$status"
(( status == 0 )) || exit "$status"

semantic_rule_count=$(rg -c '^[[:space:]]*rule ' "$work/semantic.k")
verification_rule_count=$(rg -c '^[[:space:]]*rule ' "$work/verification.k")
spec_claim_count=$(rg -c '^[[:space:]]*claim' "$work/spec.k")
printf 'COUNTS semantic_rules=%s verification_macro_rules=%s spec_claims=%s\n' \
  "$semantic_rule_count" "$verification_rule_count" "$spec_claim_count"

if [[ "$semantic_rule_count" != 37 || "$verification_rule_count" != 1 || "$spec_claim_count" != 10 ]]; then
  printf '%s\n' 'FAIL: inventory counts do not match reviewer inventory'
  exit 1
fi

printf '%s\n' 'COMMAND: search for semantic/proof attributes'
rg -n \
  '(function|total|functional|simplification|concrete|macro|token|priority|owise)' \
  "$work/semantic.k" \
  "$work/verification.k" \
  "$work/spec.k"
status=$?
printf 'EXIT: %s\n' "$status"
(( status == 0 )) || exit "$status"

printf '%s\n' 'STAGE5_INVENTORY_OK'
