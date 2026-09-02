#!/usr/bin/env bash
set -euo pipefail

cd /tmp/audit-work/scratch/proof

run_claim() {
  local definition=$1
  local spec_file=$2
  local spec_module=$3
  local label=$4
  printf '\nCOMMAND: kprove %s --definition %s --spec-module %s --claims %s\n' \
    "$spec_file" "$definition" "$spec_module" "$label"
  set +e
  kprove "$spec_file" \
    --definition "$definition" \
    --spec-module "$spec_module" \
    --claims "$label"
  local status=$?
  set -e
  printf 'EXIT STATUS: %d (%s)\n' "$status" "$label"
  if [[ $status -ne 0 ]]; then
    return "$status"
  fi
}

run_claim verification-base-rebuilt connection-spec.k CONNECTION-SPEC \
  CONNECTION-SPEC.parity-int
run_claim verification-base-rebuilt connection-spec.k CONNECTION-SPEC \
  CONNECTION-SPEC.parity-bool
run_claim verification-base-rebuilt connection-spec.k CONNECTION-SPEC \
  CONNECTION-SPEC.parity-float
run_claim verification-base-rebuilt connection-spec.k CONNECTION-SPEC \
  CONNECTION-SPEC.parity-int-exec
run_claim verification-base-rebuilt connection-spec.k CONNECTION-SPEC \
  CONNECTION-SPEC.parity-bool-exec
run_claim verification-base-rebuilt connection-spec.k CONNECTION-SPEC \
  CONNECTION-SPEC.parity-float-exec
run_claim verification-rebuilt spec.k SPEC SPEC.count-loop
run_claim verification-rebuilt spec.k SPEC SPEC.exchange
