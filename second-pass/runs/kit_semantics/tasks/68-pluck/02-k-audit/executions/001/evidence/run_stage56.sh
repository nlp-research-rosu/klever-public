#!/usr/bin/env bash
set -u

run_logged() {
  local label="$1"
  shift
  local log="/audit-output/evidence/${label}.log"
  {
    printf 'CWD: %s\n' "$PWD"
    printf 'COMMAND:'
    printf ' %q' "$@"
    printf '\n'
    "$@"
    local status=$?
    printf 'EXIT_STATUS: %d\n' "$status"
    return "$status"
  } >"$log" 2>&1
}

cd /tmp/audit-work/68-pluck || exit 90

run_logged 20-projection-wrong-dry-run \
  kprove spec-projection-wrong.k \
    --definition audit-verification-kompiled \
    --spec-module SPEC-PROJECTION-WRONG \
    --dry-run
projection_dry_status=$?

run_logged 21-projection-wrong-proof \
  kprove spec-projection-wrong.k \
    --definition audit-verification-kompiled \
    --spec-module SPEC-PROJECTION-WRONG
projection_wrong_status=$?

run_logged 22-candidate-body-mutation-clean \
  kprove spec-body-mutation.k \
    --definition audit-verification-kompiled \
    --spec-module SPEC-BODY-MUTATION
body_mutation_status=$?

run_logged 23-fresh-false-value-dry-run \
  kprove spec-audit-false-value.k \
    --definition audit-verification-kompiled \
    --spec-module SPEC-AUDIT-FALSE-VALUE \
    --dry-run
false_dry_status=$?

run_logged 24-fresh-false-value-proof \
  kprove spec-audit-false-value.k \
    --definition audit-verification-kompiled \
    --spec-module SPEC-AUDIT-FALSE-VALUE
false_value_status=$?

printf '%s\n' \
  "projection_dry=$projection_dry_status projection_wrong=$projection_wrong_status" \
  "body_mutation=$body_mutation_status false_value_dry=$false_dry_status false_value=$false_value_status"

# Dry runs must build. All three actual probes are expected to fail by a stuck
# semantic obligation, so success would be an audit failure.
if (( projection_dry_status != 0 || false_dry_status != 0 )); then
  exit 1
fi
if (( projection_wrong_status == 0 || body_mutation_status == 0 ||
      false_value_status == 0 )); then
  exit 1
fi
