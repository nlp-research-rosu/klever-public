#!/usr/bin/env bash
set -u

log=/audit-output/evidence/07b_corrected_attribute_inventory.log
exec > >(tee "$log") 2>&1
scratch=/tmp/audit-work/133-sum-squares

run() {
  printf '\nCOMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf 'EXIT_STATUS: %d\n' "$status"
  return 0
}

printf 'COMMAND: cd %q\n' "$scratch"
cd "$scratch"
printf 'EXIT_STATUS: %d\n' "$?"
run rg -n '^[[:space:]]*(syntax|configuration|rule|claim|imports|requires)' \
  semantic.k verification.k spec.k
run rg -n '\[(function|total|functional|simplification|concrete|priority|owise)' \
  semantic.k verification.k spec.k
run rg -n '(functional|simplification|concrete|priority|owise|opaque)' \
  semantic.k verification.k spec.k
