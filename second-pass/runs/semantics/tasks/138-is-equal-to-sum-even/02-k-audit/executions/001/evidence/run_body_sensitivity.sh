#!/usr/bin/env bash
set -uo pipefail

work=/tmp/audit-work/review-138
evidence=/audit-output/evidence
cd "$work" || exit 99

dry_log="$evidence/body-sensitivity-dry-run.log"
{
  echo "WORKDIR: $PWD"
  echo "COMMAND: kprove spec-body-sensitivity.k --definition fixed-semantics-kompiled --spec-module SPEC-BODY-SENSITIVITY --dry-run"
  kprove spec-body-sensitivity.k \
    --definition fixed-semantics-kompiled \
    --spec-module SPEC-BODY-SENSITIVITY \
    --dry-run > /dev/null
  status=$?
  echo "OUTPUT: suppressed KORE serialization (dry-run parsing/build only)"
  echo "EXIT_STATUS: $status"
  exit "$status"
} 2>&1 | tee "$dry_log"
dry_status="${PIPESTATUS[0]}"

proof_log="$evidence/body-sensitivity-proof.log"
{
  echo "WORKDIR: $PWD"
  echo "COMMAND: kprove spec-body-sensitivity.k --definition fixed-semantics-kompiled --spec-module SPEC-BODY-SENSITIVITY"
  kprove spec-body-sensitivity.k \
    --definition fixed-semantics-kompiled \
    --spec-module SPEC-BODY-SENSITIVITY
  status=$?
  echo "EXIT_STATUS: $status"
  exit "$status"
} 2>&1 | tee "$proof_log"
proof_status="${PIPESTATUS[0]}"

echo "DRY_RUN_STATUS: $dry_status"
echo "PROOF_STATUS: $proof_status"

if [[ "$dry_status" -ne 0 || "$proof_status" -eq 0 ]]; then
  exit 1
fi
if ! grep -q 'WarnStuckClaimState' "$proof_log"; then
  exit 1
fi
echo "AUDIT_CHECK: changed real function body invalidated the original result obligation"
