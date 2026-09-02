#!/usr/bin/env bash
set -euo pipefail

root="/tmp/audit-work/86-anti-shuffle"
files=(
  "$root/reference-semantics/semantics.k"
  "$root"/reference-semantics/semantics/*.k
  "$root/verification.k"
)

printf 'Inventory policy:\n'
printf '  DECLARATION records every local syntax, rule, configuration, and context start.\n'
printf '  ATTRIBUTE records every declaration/rule line carrying K attributes.\n'
printf '  OPAQUE records every declaration using no-evaluators or symbol attributes.\n'
printf '  Files are the clean scratch copies; hashes make the inventory reproducible.\n\n'

sha256sum "${files[@]}"

printf '\nCOUNTS\n'
for file in "${files[@]}"; do
  syntax_count=$(rg -c '^[[:space:]]*syntax([[:space:]]|$)' "$file" || true)
  rule_count=$(rg -c '^[[:space:]]*rule([[:space:]]|$)' "$file" || true)
  config_count=$(rg -c '^[[:space:]]*configuration([[:space:]]|$)' "$file" || true)
  context_count=$(rg -c '^[[:space:]]*context([[:space:]]|$)' "$file" || true)
  printf '%s\tsyntax=%s\trule=%s\tconfiguration=%s\tcontext=%s\n' \
    "$file" "${syntax_count:-0}" "${rule_count:-0}" \
    "${config_count:-0}" "${context_count:-0}"
done

printf '\nDECLARATIONS\n'
rg -n --no-heading \
  '^[[:space:]]*(syntax|rule|configuration|context)([[:space:]]|$)' \
  "${files[@]}" || true

printf '\nATTRIBUTES\n'
rg -n --no-heading \
  '\[[^]]*(function|functional|total|simplification|priority|macro|anywhere|owise|strict|seqstrict|concrete|symbol|no-evaluators)[^]]*\]' \
  "${files[@]}" || true

printf '\nOPAQUE_OR_UNINTERPRETED_DECLARATIONS\n'
rg -n --no-heading \
  '\[[^]]*(no-evaluators|symbol)[^]]*\]|trusted opaque|opaque symbolic' \
  "${files[@]}" || true
