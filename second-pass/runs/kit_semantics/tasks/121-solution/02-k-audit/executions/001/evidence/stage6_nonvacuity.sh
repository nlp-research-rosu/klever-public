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

cd /tmp/audit-work/reconstruction
run_success python3 /audit-output/evidence/stage6_prepare.py
cp -a stage6-false-result.k /audit-output/evidence/stage6-false-result.k
run_success kprove stage6-false-result.k \
  --definition auditor-verification-kompiled \
  --spec-module STAGE6-FALSE-RESULT \
  --dry-run \
  --output none

echo "+ kprove stage6-false-result.k --definition auditor-verification-kompiled --spec-module STAGE6-FALSE-RESULT"
kprove stage6-false-result.k \
  --definition auditor-verification-kompiled \
  --spec-module STAGE6-FALSE-RESULT
status=$?
echo "EXIT: $status (expected nonzero)"
if [[ $status -eq 0 ]]; then
  echo "ERROR: false full-program result unexpectedly proved"
  exit 1
fi
