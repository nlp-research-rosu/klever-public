#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/30-get-positive
files=(
  "$scratch/solution.mpy"
  "$scratch/semantic.k"
  "$scratch/verification.k"
  "$scratch/spec.k"
)

for file in "${files[@]}"; do
  printf 'SOURCE path=%s sha256=%s lines=%s\n' \
    "$file" "$(sha256sum "$file" | cut -d' ' -f1)" "$(wc -l < "$file")"
  nl -ba "$file"
done

printf 'DECLARATION_AND_RULE_MATCHES\n'
rg -n \
  '^[[:space:]]*(syntax|configuration|rule|claim)|\[(function|total|functional|simplification|concrete|priority|owise|symbol|constructor)' \
  "$scratch/semantic.k" "$scratch/verification.k" "$scratch/spec.k"

printf 'SPECIAL_ATTRIBUTE_COUNTS\n'
for token in function total functional simplification concrete priority owise opaque anywhere macro alias trusted; do
  count=$(rg -o "\\[[^]]*\\b${token}\\b[^]]*\\]" "$scratch/semantic.k" "$scratch/verification.k" "$scratch/spec.k" | wc -l)
  printf '%s=%s\n' "$token" "$count"
done
