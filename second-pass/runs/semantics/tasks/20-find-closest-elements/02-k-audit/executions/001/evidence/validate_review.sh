#!/usr/bin/env bash
set -u

review=/audit-output/REVIEW.md

echo "review final lines"
tail -n 2 "$review"
test "$(tail -n 2 "$review")" = $'VERDICT: FAIL\nLEGITIMACY: NOT_LEGIT'
tail_status=$?
printf 'exact_final_marker_status=%s\n' "$tail_status"

echo "restored scratch source identity"
cmp /candidate/solution.mpy /tmp/audit-work/reconstruction/solution.mpy
solution_status=$?
cmp /candidate/verification.k /tmp/audit-work/reconstruction/verification.k
verification_status=$?
printf 'solution_restore_cmp_status=%s\n' "$solution_status"
printf 'verification_restore_cmp_status=%s\n' "$verification_status"

echo "critical proof signals"
grep -F '#Top' /audit-output/evidence/06-kprove-positive.log
positive_signal=$?
grep -F 'WarnStuckClaimState' /audit-output/evidence/17-vacuity-proof.log
vacuity_signal=$?
printf 'positive_top_signal_status=%s\n' "$positive_signal"
printf 'vacuity_stuck_signal_status=%s\n' "$vacuity_signal"
printf 'positive_exit_status='
cat /audit-output/evidence/06-kprove-positive.status
printf 'vacuity_exit_status='
cat /audit-output/evidence/17-vacuity-proof.status

if (( tail_status != 0 || solution_status != 0 || verification_status != 0 ||
      positive_signal != 0 || vacuity_signal != 0 )); then
  exit 1
fi
