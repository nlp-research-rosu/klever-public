#!/usr/bin/env bash
set -uo pipefail

run_checked() {
  echo "+ $*"
  "$@"
  local status=$?
  echo "EXIT: $status"
  if [[ $status -ne 0 ]]; then
    exit "$status"
  fi
}

cd /tmp/audit-work/reconstruction
run_checked kprove stage4-ground.k \
  --definition auditor-verification-kompiled \
  --spec-module STAGE4-GROUND-PROGRAM
run_checked kprove stage4-ground.k \
  --definition auditor-verification-kompiled \
  --spec-module STAGE4-GROUND-SUMMARIES
run_checked python3 /audit-output/evidence/stage4_ground_python.py
