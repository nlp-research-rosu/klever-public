#!/usr/bin/env bash
set -u

scratch="/tmp/audit-work/37-sort-even"
evidence="/audit-output/evidence"
summary="$evidence/06-nonvacuity-summary.log"
spec="$scratch/spec-vacuity-audit.k"
definition="$scratch/verification-kompiled-fresh"

printf '%s\n' \
  'COMMAND: cp -a /audit-output/evidence/06-spec-vacuity.k /tmp/audit-work/37-sort-even/spec-vacuity-audit.k' \
  > "$summary"
cp -a "$evidence/06-spec-vacuity.k" "$spec" >> "$summary" 2>&1
copy_status=$?
printf 'COPY_EXIT_STATUS: %s\n' "$copy_status" >> "$summary"

dry_log="$evidence/06-nonvacuity-dry-run.log"
printf '%s\n' \
  'COMMAND: kprove spec-vacuity-audit.k --definition verification-kompiled-fresh --spec-module SPEC-VACUITY --claims SPEC-VACUITY.false-result --dry-run --output none' \
  > "$dry_log"
if [ "$copy_status" -eq 0 ]; then
  (
    cd "$scratch" &&
    kprove spec-vacuity-audit.k \
      --definition "$definition" \
      --spec-module SPEC-VACUITY \
      --claims SPEC-VACUITY.false-result \
      --dry-run \
      --output none
  ) >> "$dry_log" 2>&1
  dry_status=$?
else
  dry_status=1
fi
printf 'EXIT_STATUS: %s\n' "$dry_status" >> "$dry_log"
printf 'DRY_RUN_EXIT_STATUS: %s\n' "$dry_status" >> "$summary"

proof_log="$evidence/06-nonvacuity-proof.log"
printf '%s\n' \
  'COMMAND: timeout 180 kprove spec-vacuity-audit.k --definition verification-kompiled-fresh --spec-module SPEC-VACUITY --claims SPEC-VACUITY.false-result --output pretty' \
  > "$proof_log"
if [ "$dry_status" -eq 0 ]; then
  (
    cd "$scratch" &&
    timeout 180 kprove spec-vacuity-audit.k \
      --definition "$definition" \
      --spec-module SPEC-VACUITY \
      --claims SPEC-VACUITY.false-result \
      --output pretty
  ) >> "$proof_log" 2>&1
  proof_status=$?
else
  proof_status=0
fi
printf 'EXIT_STATUS: %s\n' "$proof_status" >> "$proof_log"
printf 'EXPECTED_NONZERO_PROOF_EXIT_STATUS: %s\n' "$proof_status" >> "$summary"

stuck_status=1
if rg -q 'WarnStuckClaimState' "$proof_log" && \
   rg -Fq 'vCons ( 3 , vCons ( 6 , vCons ( 5 , vCons ( 4' "$proof_log"; then
  stuck_status=0
fi
printf 'EXPECTED_ACTUAL_RESULT_RESIDUAL_CHECK_EXIT_STATUS: %s\n' "$stuck_status" >> "$summary"

if [ "$copy_status" -ne 0 ] || [ "$dry_status" -ne 0 ] || \
   [ "$proof_status" -eq 0 ] || [ "$proof_status" -eq 124 ] || \
   [ "$stuck_status" -ne 0 ]; then
  printf '%s\n' 'OVERALL_EXIT_STATUS: 1' >> "$summary"
  exit 1
fi
printf '%s\n' 'OVERALL_EXIT_STATUS: 0' >> "$summary"
exit 0
