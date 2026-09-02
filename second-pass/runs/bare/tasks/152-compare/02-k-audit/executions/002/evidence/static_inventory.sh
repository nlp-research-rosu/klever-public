#!/usr/bin/env bash
set -euo pipefail

cd /tmp/audit-work/152-compare

printf 'SOURCE semantic.k\n'
nl -ba semantic.k
printf 'SOURCE verification.k\n'
nl -ba verification.k
printf 'SOURCE spec.k\n'
nl -ba spec.k
printf 'DECLARATION_AND_RULE_INDEX\n'
rg -n \
  '^\s*rule\b|^\s*syntax\b|^\s*configuration\b|^\s*claim\b|\[(?:[^]]*\b(?:function|functional|total|simplification|priority|owise)\b[^]]*)\]' \
  semantic.k verification.k spec.k
printf 'semantic_rule_count='
rg -c '^\s*rule\b' semantic.k
printf 'verification_rule_count='
rg -c '^\s*rule\b' verification.k
printf 'spec_claim_count='
rg -c '^\s*claim\b' spec.k
printf 'priority_or_simplification_or_owise_count='
count="$(rg -c '\[(?:[^]]*\b(?:simplification|priority|owise)\b[^]]*)\]' semantic.k verification.k spec.k || true)"
if [[ -z "$count" ]]; then
  count=0
fi
printf '%s\n' "$count"
