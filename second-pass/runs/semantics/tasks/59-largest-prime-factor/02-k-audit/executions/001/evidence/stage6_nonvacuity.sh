#!/usr/bin/env bash
set -u

cd /tmp/audit-work/review-59/candidate-src || exit 90
raw=/tmp/audit-work/review-59/stage6-proof.raw.log

echo '$ cmp -s scratch/spec-vacuity.k /audit-output/evidence/spec-vacuity.k'
cmp -s spec-vacuity.k /audit-output/evidence/spec-vacuity.k
copy_status=$?
echo "exit=$copy_status"

echo '$ kprove spec-vacuity.k --definition verification-kompiled --spec-module SPEC-VACUITY --dry-run'
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY \
  --dry-run
dry_status=$?
echo "exit=$dry_status"

echo '$ kprove spec-vacuity.k --definition verification-kompiled --spec-module SPEC-VACUITY'
kprove spec-vacuity.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY > "$raw" 2>&1
proof_status=$?
sed -n '1,260p' "$raw"
echo "exit=$proof_status"

grep -q 'WarnStuckClaimState' "$raw"
stuck_status=$?
echo "stuck_marker_status=$stuck_status"
grep -Fq 'F +Int 1' "$raw"
obligation_status=$?
echo "result_obligation_marker_status=$obligation_status"

if [ "$copy_status" -ne 0 ] || [ "$dry_status" -ne 0 ]; then
  exit 1
fi
if [ "$proof_status" -eq 0 ] || [ "$stuck_status" -ne 0 ] || [ "$obligation_status" -ne 0 ]; then
  exit 2
fi
exit 0
