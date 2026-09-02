#!/usr/bin/env bash
set -uo pipefail
set -x

cd /tmp/audit-work/prime-length-audit

kprove spec-vacuity-audit.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC-VACUITY-AUDIT \
  --claims SPEC-VACUITY-AUDIT.prime-length-small-false \
  --dry-run
dry_run_status=$?
echo "EXIT_STATUS=${dry_run_status} EXPECTED=zero COMMAND=kprove spec-vacuity-audit.k --definition audit-verification-kompiled --spec-module SPEC-VACUITY-AUDIT --claims SPEC-VACUITY-AUDIT.prime-length-small-false --dry-run"

kprove spec-vacuity-audit.k \
  --definition audit-verification-kompiled \
  --spec-module SPEC-VACUITY-AUDIT \
  --claims SPEC-VACUITY-AUDIT.prime-length-small-false
proof_status=$?
echo "EXIT_STATUS=${proof_status} EXPECTED=nonzero COMMAND=kprove spec-vacuity-audit.k --definition audit-verification-kompiled --spec-module SPEC-VACUITY-AUDIT --claims SPEC-VACUITY-AUDIT.prime-length-small-false"

if [[ "$dry_run_status" -ne 0 || "$proof_status" -eq 0 ]]; then
  exit 1
fi
exit 0
