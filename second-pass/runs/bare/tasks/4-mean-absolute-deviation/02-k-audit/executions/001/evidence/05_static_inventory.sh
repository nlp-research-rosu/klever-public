#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/reconstruction

run() {
  local description="$1"
  shift
  printf '\nCOMMAND (%s):' "$description"
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf 'EXIT STATUS: %d\n' "$status"
  return "$status"
}

printf 'AUDIT STAGE 5: raw exhaustive declaration/rule inventory\n'

run "numbered semantic.k" nl -ba "$scratch/semantic.k"
semantic_status=$?
run "numbered verification.k" nl -ba "$scratch/verification.k"
verification_status=$?
run "numbered spec.k" nl -ba "$scratch/spec.k"
spec_status=$?

run "all local syntax, configuration, rule, and claim starts" \
  rg -n '^[[:space:]]*(syntax|configuration|rule|claim)([[:space:]]|$)' \
    "$scratch/semantic.k" "$scratch/verification.k" "$scratch/spec.k"
inventory_status=$?

printf '\nATTRIBUTE INVENTORY\n'
rg -n '\[(function|total|functional|simplification|concrete|priority|owise|opaque|anywhere|macro)(,|\])' \
  "$scratch/semantic.k" "$scratch/verification.k" "$scratch/spec.k" || true

printf '\nEXPLICIT ABSENCE CHECKS\n'
for attribute in function total functional simplification concrete priority owise opaque anywhere macro; do
  if rg -q "\\[$attribute(,|\\])" \
      "$scratch/semantic.k" "$scratch/verification.k" "$scratch/spec.k"; then
    printf 'PRESENT: %s\n' "$attribute"
  else
    printf 'ABSENT: %s\n' "$attribute"
  fi
done

printf '\nRULE COUNTS (multiline rules counted by rule-start lines)\n'
printf 'semantic.k rules: '
rg -c '^[[:space:]]*rule([[:space:]]|$)' "$scratch/semantic.k"
printf 'verification.k rules: '
rg -c '^[[:space:]]*rule([[:space:]]|$)' "$scratch/verification.k"
printf 'spec.k claims: '
rg -c '^[[:space:]]*claim([[:space:]]|$)' "$scratch/spec.k"

if (( semantic_status || verification_status || spec_status || inventory_status )); then
  exit 1
fi
