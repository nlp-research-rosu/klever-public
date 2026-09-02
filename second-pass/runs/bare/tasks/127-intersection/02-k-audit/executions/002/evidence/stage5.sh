#!/usr/bin/env bash
set -u

source_dir=/tmp/audit-work/candidate-src
cd "${source_dir}" || exit 90

echo "COMMAND: rg -n '^[[:space:]]*(syntax|configuration|context|rule|claim|alias)\\b' semantic.k verification.k spec.k"
rg -n '^[[:space:]]*(syntax|configuration|context|rule|claim|alias)\b' \
  semantic.k verification.k spec.k
inventory_status=$?
echo "EXIT: ${inventory_status}"

echo "COMMAND: rg -n '\\[(total|functional|function|simplification|priority|anywhere|macro|alias)' semantic.k verification.k spec.k"
rg -n '\[(total|functional|function|simplification|priority|anywhere|macro|alias)' \
  semantic.k verification.k spec.k
attribute_status=$?
echo "EXIT: ${attribute_status}"

semantic_rule_count=$(rg -c '^[[:space:]]*rule\b' semantic.k)
verification_rule_count=$(rg -c '^[[:space:]]*rule\b' verification.k)
context_count=$(rg -c '^[[:space:]]*context\b' semantic.k)
claim_count=$(rg -c '^[[:space:]]*claim\b' spec.k)
semantic_rule_count=${semantic_rule_count:-0}
verification_rule_count=${verification_rule_count:-0}
context_count=${context_count:-0}
claim_count=${claim_count:-0}
echo "SEMANTIC_RULE_COUNT=${semantic_rule_count}"
echo "VERIFICATION_RULE_COUNT=${verification_rule_count}"
echo "CONTEXT_COUNT=${context_count}"
echo "CLAIM_COUNT=${claim_count}"

echo "COMMAND: rg -n '\\[(total|functional|simplification|anywhere|macro|alias)' semantic.k verification.k spec.k"
if rg -n '\[(total|functional|simplification|anywhere|macro|alias)' \
  semantic.k verification.k spec.k; then
  forbidden_status=1
else
  forbidden_status=0
fi
echo "NO_MATCH_EXPECTED_EXIT: ${forbidden_status}"

if [ "${inventory_status}" -ne 0 ] \
   || [ "${attribute_status}" -ne 0 ] \
   || [ "${semantic_rule_count}" -ne 33 ] \
   || [ "${verification_rule_count}" -ne 9 ] \
   || [ "${context_count}" -ne 8 ] \
   || [ "${claim_count}" -ne 5 ] \
   || [ "${forbidden_status}" -ne 0 ]; then
  exit 1
fi
