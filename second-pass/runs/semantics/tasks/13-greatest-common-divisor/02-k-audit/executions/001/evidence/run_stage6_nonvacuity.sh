#!/usr/bin/env bash
set +e

WORK=/tmp/audit-work/source
EVIDENCE=/audit-output/evidence

printf 'COMMAND: cp %s %s\n' \
  "$EVIDENCE/spec-vacuity.k" "$WORK/spec-vacuity.k"
cp "$EVIDENCE/spec-vacuity.k" "$WORK/spec-vacuity.k"
copy_status=$?
printf 'COPY EXIT STATUS: %d\n' "$copy_status"

printf 'COMMAND: kprove %s --definition %s --spec-module GCD-SPEC-VACUITY --claims false-off-by-one --dry-run --warnings none\n' \
  "$WORK/spec-vacuity.k" "$WORK/verification-kompiled" \
  | tee "$EVIDENCE/stage6_dry_run.log"
kprove "$WORK/spec-vacuity.k" \
  --definition "$WORK/verification-kompiled" \
  --spec-module GCD-SPEC-VACUITY \
  --claims false-off-by-one \
  --dry-run \
  --warnings none \
  2>&1 | tee -a "$EVIDENCE/stage6_dry_run.log"
dry_status=${PIPESTATUS[0]}
printf 'EXIT STATUS: %d\n' "$dry_status" | tee -a "$EVIDENCE/stage6_dry_run.log"

printf 'COMMAND: kprove %s --definition %s --spec-module GCD-SPEC-VACUITY --claims false-off-by-one --warnings none\n' \
  "$WORK/spec-vacuity.k" "$WORK/verification-kompiled" \
  | tee "$EVIDENCE/stage6_false_proof.log"
kprove "$WORK/spec-vacuity.k" \
  --definition "$WORK/verification-kompiled" \
  --spec-module GCD-SPEC-VACUITY \
  --claims false-off-by-one \
  --warnings none \
  2>&1 | tee -a "$EVIDENCE/stage6_false_proof.log"
proof_status=${PIPESTATUS[0]}
printf 'EXIT STATUS: %d\n' "$proof_status" | tee -a "$EVIDENCE/stage6_false_proof.log"

grep -q 'WarnStuckClaimState' "$EVIDENCE/stage6_false_proof.log"
stuck_status=$?
printf 'EXPECTED STUCK-CLAIM MARKER CHECK EXIT STATUS: %d\n' "$stuck_status"

if (( copy_status == 0 && dry_status == 0 && proof_status != 0 && stuck_status == 0 )); then
  printf 'STAGE 6 RESULT: expected meaningful proof failure observed\n'
  exit 0
fi

printf 'STAGE 6 RESULT: non-vacuity conditions not all met\n'
exit 1
