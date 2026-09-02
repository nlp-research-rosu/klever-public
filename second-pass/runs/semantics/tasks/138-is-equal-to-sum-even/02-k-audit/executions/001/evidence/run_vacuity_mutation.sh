#!/usr/bin/env bash
set -uo pipefail

work=/tmp/audit-work/review-138
evidence=/audit-output/evidence
cd "$work" || exit 99

dry_log="$evidence/vacuity-dry-run.log"
{
  echo "WORKDIR: $PWD"
  echo "COMMAND: kprove spec-vacuity-audit.k --definition verification-kompiled --spec-module SPEC-VACUITY-AUDIT --dry-run"
  kprove spec-vacuity-audit.k \
    --definition verification-kompiled \
    --spec-module SPEC-VACUITY-AUDIT \
    --dry-run > /dev/null
  dry_status=$?
  echo "OUTPUT: suppressed KORE serialization (dry-run parsing/build only)"
  echo "EXIT_STATUS: $dry_status"
  exit "$dry_status"
} 2>&1 | tee "$dry_log"
dry_status="${PIPESTATUS[0]}"

prove_log="$evidence/vacuity-proof.log"
{
  echo "WORKDIR: $PWD"
  echo "COMMAND: kprove spec-vacuity-audit.k --definition verification-kompiled --spec-module SPEC-VACUITY-AUDIT"
  kprove spec-vacuity-audit.k \
    --definition verification-kompiled \
    --spec-module SPEC-VACUITY-AUDIT
  prove_status=$?
  echo "EXIT_STATUS: $prove_status"
  exit "$prove_status"
} 2>&1 | tee "$prove_log"
prove_status="${PIPESTATUS[0]}"

echo "DRY_RUN_STATUS: $dry_status"
echo "PROOF_STATUS: $prove_status"

if [[ "$dry_status" -ne 0 ]]; then
  echo "AUDIT_CHECK: mutation did not build"
  exit 1
fi
if [[ "$prove_status" -eq 0 ]]; then
  echo "AUDIT_CHECK: false mutation unexpectedly proved"
  exit 1
fi
if ! grep -q 'WarnStuckClaimState' "$prove_log"; then
  echo "AUDIT_CHECK: failure was not the expected stuck claim"
  exit 1
fi

echo "AUDIT_CHECK: expected unmet result obligation observed"
exit 0
