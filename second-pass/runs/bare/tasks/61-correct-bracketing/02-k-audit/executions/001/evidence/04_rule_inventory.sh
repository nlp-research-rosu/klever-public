#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/candidate-src

echo "SOURCE_HASHES"
sha256sum \
  "$scratch/semantic.k" \
  "$scratch/verification.k" \
  "$scratch/spec.k" \
  "$scratch/solution.mpy"

echo "SEMANTIC_DECLARATIONS_CONFIGURATION_AND_RULE_STARTS"
rg -n '^[[:space:]]*(syntax|configuration|rule|claim|priority)' \
  "$scratch/semantic.k"

echo "VERIFICATION_DECLARATIONS_AND_RULE_STARTS"
rg -n '^[[:space:]]*(syntax|configuration|rule|claim|priority)' \
  "$scratch/verification.k"

echo "SPEC_CLAIMS"
rg -n '^[[:space:]]*claim' "$scratch/spec.k"

echo "ATTRIBUTES_AND_OPAQUE_MARKERS"
rg -n '\[(function|total|functional|simplification|priority|opaque|macro|anywhere|trusted)' \
  "$scratch/semantic.k" "$scratch/verification.k" "$scratch/spec.k" || true

echo "COUNTS"
printf 'semantic_rule_count='
rg -c '^[[:space:]]*rule' "$scratch/semantic.k"
printf 'verification_rule_count='
rg -c '^[[:space:]]*rule' "$scratch/verification.k"
printf 'spec_claim_count='
rg -c '^[[:space:]]*claim' "$scratch/spec.k"

echo "NUMBERED_SEMANTIC_SOURCE"
nl -ba "$scratch/semantic.k"

echo "NUMBERED_VERIFICATION_SOURCE"
nl -ba "$scratch/verification.k"

echo "NUMBERED_SPEC_SOURCE"
nl -ba "$scratch/spec.k"
