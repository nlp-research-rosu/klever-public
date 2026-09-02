#!/usr/bin/env bash
set -u

work=/tmp/audit-work/reconstruction

printf '%s\n' 'COMMAND: nl -ba semantic.k'
nl -ba "$work/semantic.k"
code=$?
printf 'EXIT: %s\n' "$code"
(( code == 0 )) || exit 1

printf '%s\n' 'COMMAND: nl -ba verification.k'
nl -ba "$work/verification.k"
code=$?
printf 'EXIT: %s\n' "$code"
(( code == 0 )) || exit 1

printf '%s\n' 'COMMAND: source inventory counts'
printf 'semantic_rule_count='
rg '^  rule ' "$work/semantic.k" | wc -l
printf 'verification_rule_count='
rg '^  rule ' "$work/verification.k" | wc -l
printf 'semantic_syntax_declaration_count='
rg '^  syntax ' "$work/semantic.k" | wc -l
printf 'verification_syntax_declaration_count='
rg '^  syntax ' "$work/verification.k" | wc -l
printf 'function_attribute_count='
rg -o '\[function\]' "$work/semantic.k" "$work/verification.k" | wc -l
printf 'total_attribute_count='
rg -o '\[total\]' "$work/semantic.k" "$work/verification.k" | wc -l
printf 'functional_attribute_count='
rg -o '\[functional\]' "$work/semantic.k" "$work/verification.k" | wc -l
printf 'simplification_attribute_count='
rg -o '\[simplification\]' "$work/semantic.k" "$work/verification.k" | wc -l
printf 'concrete_attribute_count='
rg -o '\[concrete\]' "$work/semantic.k" "$work/verification.k" | wc -l
printf 'owise_attribute_count='
rg -o '\[owise\]' "$work/semantic.k" "$work/verification.k" | wc -l
printf 'explicit_priority_attribute_count='
rg -o '\[(priority|priorities)[^]]*\]' "$work/semantic.k" "$work/verification.k" | wc -l
printf 'EXIT: 0\n'

printf '%s\n' 'COMMAND: sed -n "1110,1148p;1718,1775p;1838,1870p" /usr/include/kframework/builtin/domains.md'
sed -n '1110,1148p;1718,1775p;1838,1870p' \
  /usr/include/kframework/builtin/domains.md
code=$?
printf 'EXIT: %s\n' "$code"
exit "$code"
