#!/usr/bin/env bash
set -uo pipefail

run_success() {
  echo "+ $*"
  "$@"
  local status=$?
  echo "EXIT: $status"
  if [[ $status -ne 0 ]]; then
    exit "$status"
  fi
}

run_expected_failure() {
  echo "+ $*"
  "$@"
  local status=$?
  echo "EXIT: $status (expected nonzero)"
  if [[ $status -eq 0 ]]; then
    echo "ERROR: body mutation unexpectedly proved"
    exit 1
  fi
}

cd /tmp/audit-work/reconstruction
run_success kprove stage5-body-sensitivity.k \
  --definition auditor-verification-base-kompiled \
  --spec-module STAGE5-BODY-SENSITIVITY \
  --dry-run \
  --output none
run_expected_failure kprove stage5-body-sensitivity.k \
  --definition auditor-verification-base-kompiled \
  --spec-module STAGE5-BODY-SENSITIVITY
run_expected_failure kprove stage5-body-sensitivity.k \
  --definition auditor-verification-kompiled \
  --spec-module STAGE5-BODY-SENSITIVITY
