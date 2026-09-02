#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/52-below-threshold
evidence=/audit-output/evidence
failures=0

run_checked() {
  local label="$1"
  shift
  printf 'COMMAND[%s]:' "$label"
  printf ' %q' "$@"
  printf '\n'
  "$@"
  local status=$?
  printf 'EXIT[%s]=%s\n' "$label" "$status"
  if [[ "$status" -ne 0 ]]; then
    failures=$((failures + 1))
  fi
}

run_checked submitted-kast \
  kast "$scratch/solution.mpy" \
    --definition "$scratch/reviewer-verification-base-kompiled" \
    --module VERIFICATION-BASE \
    --sort Module \
    --output json \
    --expand-macros \
    --output-file "$scratch/solution-expanded.json"

run_checked call-kast \
  kast \
    --expression '#belowThresholdCall(.IntSeq, 0)' \
    --definition "$scratch/reviewer-verification-base-kompiled" \
    --module VERIFICATION-BASE \
    --sort KItem \
    --output json \
    --expand-macros \
    --output-file "$scratch/call-expanded.json"

run_checked pinning /audit-output/evidence/pinning_check.py
run_checked witnesses /audit-output/evidence/witnesses.py
run_checked inventory /audit-output/evidence/inventory_k.py

printf 'PINNING_INVENTORY_FAILURE_COUNT=%s\n' "$failures"
exit "$failures"
