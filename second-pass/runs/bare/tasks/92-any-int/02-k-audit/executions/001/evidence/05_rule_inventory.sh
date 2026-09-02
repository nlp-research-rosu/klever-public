#!/usr/bin/env bash
set -u

log=/audit-output/evidence/05_rule_inventory.log
exec > >(tee "$log") 2>&1

run() {
  printf '\nCOMMAND:'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf 'EXIT_STATUS: %d\n' "$status"
}

src=/tmp/audit-work/92-any-int/src
printf 'AUDIT_STAGE: 5 local declaration and rule inventory\n'
run nl -ba "$src/semantic.k"
run nl -ba "$src/verification.k"
run nl -ba "$src/spec.k"
run bash -c 'set -o pipefail; rg -n "^[[:space:]]*(module|imports|configuration|syntax|rule|claim)|\\[(function|total|functional|simplification|concrete|priority|macro|anywhere|owise)" "$1" "$2" "$3"' _ "$src/semantic.k" "$src/verification.k" "$src/spec.k"
run bash -c 'printf "semantic_rule_count="; rg -c "^[[:space:]]*rule " "$1"; printf "verification_rule_count="; rg -c "^[[:space:]]*rule " "$2"; printf "spec_claim_count="; rg -c "^[[:space:]]*claim " "$3"' _ "$src/semantic.k" "$src/verification.k" "$src/spec.k"
run bash -c 'if rg -n "\\[(function|total|functional|simplification|concrete|priority|anywhere|owise|opaque)" "$1" "$2" "$3"; then exit 1; else echo "NO_LOCAL_FUNCTION_TOTAL_FUNCTIONAL_SIMPLIFICATION_PRIORITY_OR_OPAQUE_ATTRIBUTES"; fi' _ "$src/semantic.k" "$src/verification.k" "$src/spec.k"
