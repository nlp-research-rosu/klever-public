#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/95-check-dict-case-audit
printf '%s\n' 'COMMAND: exhaustive numbered source and declaration inventory'
for source in semantic.k program.k verification.k spec.k; do
  printf 'BEGIN_SOURCE %s\n' "$source"
  nl -ba "$scratch/$source"
  printf 'END_SOURCE %s\n' "$source"
done

printf '%s\n' 'DECLARATION_HEADS'
rg -n '^[[:space:]]*(configuration|syntax|rule|claim)([[:space:]]|$)' \
  "$scratch/semantic.k" \
  "$scratch/program.k" \
  "$scratch/verification.k" \
  "$scratch/spec.k"

printf '%s\n' 'SPECIAL_ATTRIBUTES'
rg -n '\[(function|total|functional|simplification|priority|owise|opaque|concrete)' \
  "$scratch/semantic.k" \
  "$scratch/program.k" \
  "$scratch/verification.k" \
  "$scratch/spec.k"
attribute_status=$?
printf 'ATTRIBUTE_SEARCH_EXIT=%s\n' "$attribute_status"

printf '%s\n' 'ABSENCE_COUNTS'
for token in functional simplification priority owise opaque concrete; do
  count=$(rg -o "\\[$token([^]]*)?\\]|\\b$token\\b" \
    "$scratch/semantic.k" \
    "$scratch/program.k" \
    "$scratch/verification.k" \
    "$scratch/spec.k" |
    wc -l)
  printf '%s_count=%s\n' "$token" "$count"
done

printf '%s\n' 'TARGET_CONSTRUCTORS'
rg -o '[A-Za-z][A-Za-z0-9]*\(' "$scratch/solution.mpy" |
  sed 's/($//' |
  sort -u

printf '%s\n' 'INVENTORY_EXIT=0'
exit 0
