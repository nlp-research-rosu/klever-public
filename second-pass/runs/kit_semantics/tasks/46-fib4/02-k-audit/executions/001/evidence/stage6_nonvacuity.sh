#!/usr/bin/env bash
set -uo pipefail

work=/tmp/audit-work/46-fib4
evidence=/audit-output/evidence
summary="$evidence/stage6-nonvacuity-summary.log"
: > "$summary"
cd "$work" || exit 1

dry_log="$evidence/stage6-nonvacuity-dry-run.log"
echo "COMMAND: kprove auditor-nonvacuity.k --definition verification-fresh-kompiled --spec-module AUDITOR-NONVACUITY --dry-run" | tee -a "$summary"
kprove auditor-nonvacuity.k \
  --definition verification-fresh-kompiled \
  --spec-module AUDITOR-NONVACUITY \
  --dry-run > "$dry_log" 2>&1
dry_rc=$?
echo "DRY_RUN_EXIT_STATUS=$dry_rc" | tee -a "$summary" "$dry_log"

proof_log="$evidence/stage6-nonvacuity-proof.log"
echo "COMMAND: kprove auditor-nonvacuity.k --definition verification-fresh-kompiled --spec-module AUDITOR-NONVACUITY" | tee -a "$summary"
kprove auditor-nonvacuity.k \
  --definition verification-fresh-kompiled \
  --spec-module AUDITOR-NONVACUITY > "$proof_log" 2>&1
proof_rc=$?
echo "PROOF_EXIT_STATUS=$proof_rc" | tee -a "$summary" "$proof_log"

if grep -q 'WarnStuckClaimState' "$proof_log"; then
  stuck=0
  echo "STUCK_CLAIM_CHECK=PASS" | tee -a "$summary"
else
  stuck=1
  echo "STUCK_CLAIM_CHECK=FAIL" | tee -a "$summary"
fi

if grep -Eq '<k>|2 ~> \\.K|[[:space:]]2[[:space:]]*$' "$proof_log"; then
  residual=0
  echo "EXPECTED_RESULT_2_RESIDUAL_CHECK=PASS" | tee -a "$summary"
else
  residual=1
  echo "EXPECTED_RESULT_2_RESIDUAL_CHECK=FAIL" | tee -a "$summary"
fi

sed -n '1,220p' "$proof_log" >> "$summary"

if [[ "$dry_rc" -eq 0 && "$proof_rc" -ne 0 && "$stuck" -eq 0 && "$residual" -eq 0 ]]; then
  echo "EXPECTED_NONVACUITY_RESULT=PASS" | tee -a "$summary"
  exit 0
fi
echo "EXPECTED_NONVACUITY_RESULT=FAIL" | tee -a "$summary"
exit 1
