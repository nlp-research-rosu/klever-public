#!/usr/bin/env bash
set -euo pipefail

echo "Candidate-local proof theory (complete source with line numbers)"
nl -ba /candidate/verification.k

echo "Candidate claims (complete source with line numbers)"
nl -ba /candidate/spec.k

echo "Candidate-local declaration counts"
printf 'syntax_starts='
rg -c '^[[:space:]]*syntax ' /candidate/verification.k
printf 'rule_starts='
rg -c '^[[:space:]]*rule ' /candidate/verification.k
printf 'claim_starts='
rg -c '^[[:space:]]*claim' /candidate/spec.k

echo "Supplied-semantics declaration/rule/context/configuration index"
rg -n --no-heading \
  '^[[:space:]]*(configuration|context|rule|syntax)' \
  /reference/reference-semantics/semantics.k \
  /reference/reference-semantics/semantics/*.k
