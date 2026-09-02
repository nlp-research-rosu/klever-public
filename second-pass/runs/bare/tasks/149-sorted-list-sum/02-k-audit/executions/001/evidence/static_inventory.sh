#!/usr/bin/env bash
set -u

for source in semantic.k solution-program.k verification.k spec.k; do
  printf 'FILE %s\n' "$source"
  nl -ba "$source" | grep -E \
    'module |endmodule|imports |configuration |syntax |^[[:space:]]*[0-9]+[[:space:]]+(rule|claim) |\[(function|functional|total|simplification|concrete|priority|owise|symbol)'
done

printf 'ATTRIBUTE COUNTS\n'
for attribute in function functional total simplification concrete priority owise symbol; do
  count=$(grep -F "[$attribute]" \
    semantic.k solution-program.k verification.k spec.k | wc -l)
  printf '%s=%s\n' "$attribute" "$count"
done
