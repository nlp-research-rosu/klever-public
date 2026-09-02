#!/usr/bin/env bash
set -u

WORK=/tmp/audit-work/rebuild
SUMMARY=/audit-output/evidence/06_nonvacuity.log
DRY=/audit-output/evidence/06_vacuity_dry_run.log
PROOF=/audit-output/evidence/06_vacuity_proof.log
: > "$SUMMARY"
: > "$DRY"
: > "$PROOF"

cd "$WORK" || exit 1

printf '%s\n' \
  'COMMAND: cp /audit-output/evidence/06_spec-vacuity.k /tmp/audit-work/rebuild/spec-vacuity.k' \
  >> "$SUMMARY"
cp /audit-output/evidence/06_spec-vacuity.k spec-vacuity.k
copy_status=$?
printf 'EXIT: %d\n\n' "$copy_status" >> "$SUMMARY"
if [ "$copy_status" -ne 0 ]; then
  exit "$copy_status"
fi

printf '%s\n' \
  'COMMAND: kprove spec-vacuity.k --definition verification-audit-kompiled --spec-module SPEC-VACUITY --dry-run' \
  | tee -a "$SUMMARY" > "$DRY"
kprove spec-vacuity.k \
  --definition verification-audit-kompiled \
  --spec-module SPEC-VACUITY \
  --dry-run \
  >> "$DRY" 2>&1
dry_status=$?
printf 'EXIT: %d\n\n' "$dry_status" | tee -a "$SUMMARY" >> "$DRY"

printf '%s\n' \
  'COMMAND: kprove spec-vacuity.k --definition verification-audit-kompiled --spec-module SPEC-VACUITY' \
  | tee -a "$SUMMARY" > "$PROOF"
kprove spec-vacuity.k \
  --definition verification-audit-kompiled \
  --spec-module SPEC-VACUITY \
  >> "$PROOF" 2>&1
proof_status=$?
has_stuck=no
has_top=no
if grep -q 'WarnStuckClaimState' "$PROOF"; then
  has_stuck=yes
fi
if grep -Fxq '#Top' "$PROOF"; then
  has_top=yes
fi
printf 'EXIT: %d\nHAS_STUCK_CLAIM: %s\nHAS_EXACT_TOP: %s\n' \
  "$proof_status" "$has_stuck" "$has_top" \
  | tee -a "$SUMMARY" >> "$PROOF"

printf 'EXPECTED: dry-run exit 0; proof nonzero; stuck=yes; exact_top=no\n' >> "$SUMMARY"
if [ "$dry_status" -eq 0 ] && [ "$proof_status" -ne 0 ] \
   && [ "$has_stuck" = yes ] && [ "$has_top" = no ]; then
  printf 'NONVACUITY_CHECK: PASS\n' >> "$SUMMARY"
  exit 0
fi
printf 'NONVACUITY_CHECK: FAIL\n' >> "$SUMMARY"
exit 1
