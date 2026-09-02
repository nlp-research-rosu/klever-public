#!/usr/bin/env bash
set -u

cd /tmp/audit-work/reconstruction || exit 90
cp /audit-output/evidence/04_body_sensitivity.k ./04_body_sensitivity.k

echo "COMMAND: kprove 04_body_sensitivity.k --definition fresh-verification-kompiled --spec-module AUDIT-BODY-SENSITIVITY --dry-run"
kprove 04_body_sensitivity.k \
  --definition fresh-verification-kompiled \
  --spec-module AUDIT-BODY-SENSITIVITY \
  --dry-run
dry_rc=$?
echo "DRY_RUN_EXIT_STATUS: $dry_rc"

echo "COMMAND: kprove 04_body_sensitivity.k --definition fresh-verification-kompiled --spec-module AUDIT-BODY-SENSITIVITY"
kprove 04_body_sensitivity.k \
  --definition fresh-verification-kompiled \
  --spec-module AUDIT-BODY-SENSITIVITY
proof_rc=$?
echo "PROOF_EXIT_STATUS: $proof_rc"

if [[ "$dry_rc" -eq 0 && "$proof_rc" -ne 0 ]]; then
  echo "EXPECTED_BODY_SENSITIVITY_FAILURE"
  echo "SCRIPT_EXIT=0"
  exit 0
fi
echo "UNEXPECTED_BODY_SENSITIVITY_RESULT"
echo "SCRIPT_EXIT=1"
exit 1
