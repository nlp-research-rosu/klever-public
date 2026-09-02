#!/usr/bin/env bash
set -u

cd /tmp/audit-work/reconstruction || exit 90
cp /audit-output/evidence/06_false_result.k ./06_false_result.k

echo "COMMAND: kprove 06_false_result.k --definition fresh-verification-kompiled --spec-module AUDIT-FALSE-RESULT --dry-run"
kprove 06_false_result.k \
  --definition fresh-verification-kompiled \
  --spec-module AUDIT-FALSE-RESULT \
  --dry-run
dry_rc=$?
echo "DRY_RUN_EXIT_STATUS: $dry_rc"

echo "COMMAND: kprove 06_false_result.k --definition fresh-verification-kompiled --spec-module AUDIT-FALSE-RESULT"
kprove 06_false_result.k \
  --definition fresh-verification-kompiled \
  --spec-module AUDIT-FALSE-RESULT
proof_rc=$?
echo "PROOF_EXIT_STATUS: $proof_rc"

if [[ "$dry_rc" -eq 0 && "$proof_rc" -ne 0 ]]; then
  echo "EXPECTED_FALSE_RESULT_REJECTION"
  echo "SCRIPT_EXIT=0"
  exit 0
fi
echo "UNEXPECTED_FALSE_RESULT_OUTCOME"
echo "SCRIPT_EXIT=1"
exit 1
