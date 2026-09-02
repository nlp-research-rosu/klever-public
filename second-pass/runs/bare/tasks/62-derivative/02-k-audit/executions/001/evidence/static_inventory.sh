#!/usr/bin/env bash
set -uo pipefail

work=/tmp/audit-work/audit-62

printf 'Numbered source: semantic.k\n'
nl -ba "$work/semantic.k"
printf '\nNumbered source: verification.k\n'
nl -ba "$work/verification.k"
printf '\nNumbered source: spec.k\n'
nl -ba "$work/spec.k"

printf '\nDeclarations and rule/claim starts\n'
rg -n \
  '^\s*(syntax|configuration|rule|claim)|\[(function|total|functional|simplification|concrete|priority|owise|macro|anywhere)' \
  "$work/semantic.k" "$work/verification.k" "$work/spec.k"

printf '\nSpecial proof-affecting attributes\n'
for attribute in function total functional simplification concrete priority owise macro anywhere; do
  count=$(rg -o "\\b${attribute}\\b" \
    "$work/semantic.k" "$work/verification.k" "$work/spec.k" | wc -l)
  printf '%s=%s\n' "$attribute" "$count"
done
