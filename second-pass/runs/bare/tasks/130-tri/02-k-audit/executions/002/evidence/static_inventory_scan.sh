#!/usr/bin/env bash
set -uo pipefail

audit_work=/tmp/audit-work/130-tri-audit
cd "$audit_work" || exit 2

printf 'COMMAND: sha256sum semantic.k verification.k spec.k solution.mpy\n'
sha256sum semantic.k verification.k spec.k solution.mpy
printf 'EXIT_STATUS=%s\n' "$?"

printf '\nCOMMAND: enumerate local K declarations, attributes, rules, and claims\n'
rg -n \
  '^[[:space:]]*(configuration|syntax|rule|claim)|\[(function|total|functional|macro|simplification|priority|owise|concrete)' \
  semantic.k verification.k spec.k
scan_status=$?
printf 'EXIT_STATUS=%s\n' "$scan_status"

printf '\nCOMMAND: count ordinary rules and claims per file\n'
for file in semantic.k verification.k spec.k; do
  rule_count=$(rg -c '^[[:space:]]*rule ' "$file" || true)
  claim_count=$(rg -c '^[[:space:]]*claim ' "$file" || true)
  syntax_count=$(rg -c '^[[:space:]]*syntax ' "$file" || true)
  printf '%s RULES=%s CLAIMS=%s SYNTAX_DECLARATION_LINES=%s\n' \
    "$file" "${rule_count:-0}" "${claim_count:-0}" "${syntax_count:-0}"
done

printf '\nCOMMAND: search for high-risk attributes and opaque/priority declarations\n'
rg -n \
  '\[(total|functional|simplification|priority|owise|concrete)|syntax .*\[.*(function|macro)|opaque' \
  semantic.k verification.k spec.k
risk_scan_status=$?
printf 'RISK_SCAN_EXIT_STATUS=%s (1 means no additional matches)\n' \
  "$risk_scan_status"
