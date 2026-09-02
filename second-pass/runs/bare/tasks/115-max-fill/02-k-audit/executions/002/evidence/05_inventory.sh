#!/usr/bin/env bash
set -euo pipefail

audit_root="/tmp/audit-work/reconstruction"
audit_files=(
  "$audit_root/semantic.k"
  "$audit_root/solution-program.k"
  "$audit_root/verification.k"
  "$audit_root/spec.k"
)

for audit_file in "${audit_files[@]}"; do
  printf 'FILE: %s\n' "$audit_file"
  printf 'DECLARATIONS_AND_RULE_STARTS\n'
  rg -n '^[[:space:]]*(module|endmodule|imports|configuration|syntax|rule|claim)' \
    "$audit_file" || true
  printf 'ATTRIBUTES_AND_SPECIAL_SYMBOLS\n'
  rg -n '\[(function|functional|total|simplification|concrete|priority|owise|anywhere|opaque)(,|\]|\()|\b(opaque|priority)\b' \
    "$audit_file" || true
  printf 'COUNTS\n'
  printf 'syntax_declaration_lines='
  rg -c '^[[:space:]]*syntax ' "$audit_file" || printf '0\n'
  printf 'rule_starts='
  rg -c '^[[:space:]]*rule([[:space:]]|$)' "$audit_file" || printf '0\n'
  printf 'claim_starts='
  rg -c '^[[:space:]]*claim([[:space:]]|$)' "$audit_file" || printf '0\n'
done
