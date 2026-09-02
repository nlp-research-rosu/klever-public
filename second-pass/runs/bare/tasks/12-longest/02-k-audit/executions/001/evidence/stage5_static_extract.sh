#!/usr/bin/env bash
set -euo pipefail
cd /tmp/audit-work/12-longest-audit

echo '$ local declarations and rules in semantic.k'
rg -n '^[[:space:]]*(syntax|configuration|rule)' semantic.k

echo '$ local declarations and rules in verification.k'
rg -n '^[[:space:]]*(syntax|configuration|rule)' verification.k

echo '$ claims in spec.k'
rg -n '^[[:space:]]*claim' spec.k

echo '$ special attributes'
rg -n '\[(function|total|functional|simplification|macro|priority|owise|concrete)[^]]*\]' \
  semantic.k verification.k spec.k || true

echo '$ explicit priority or functional declarations (expected none)'
if rg -n 'priority|\bfunctional\b' semantic.k verification.k spec.k; then
  :
else
  echo 'NONE'
fi

echo '$ rule/declaration counts'
printf 'semantic_rules='
rg -c '^[[:space:]]*rule' semantic.k
printf 'verification_rules='
rg -c '^[[:space:]]*rule' verification.k
printf 'spec_claims='
rg -c '^[[:space:]]*claim' spec.k

echo 'SCRIPT_EXIT_STATUS=0'
