#!/usr/bin/env bash
set +e

cd /tmp/audit-work/129-minpath || exit 99

printf '$ cp /audit-output/evidence/artifacts/reviewer-vacuity.k /tmp/audit-work/129-minpath/reviewer-vacuity.k\n'
cp /audit-output/evidence/artifacts/reviewer-vacuity.k /tmp/audit-work/129-minpath/reviewer-vacuity.k
copy_status=$?
printf '[exit %d]\n' "$copy_status"

printf '\n$ kprove reviewer-vacuity.k --definition verification-fresh-kompiled --spec-module REVIEWER-VACUITY --dry-run\n'
kprove reviewer-vacuity.k --definition verification-fresh-kompiled --spec-module REVIEWER-VACUITY --dry-run
dry_status=$?
printf '[exit %d]\n' "$dry_status"

printf '\n$ kprove reviewer-vacuity.k --definition verification-fresh-kompiled --spec-module REVIEWER-VACUITY\n'
kprove reviewer-vacuity.k --definition verification-fresh-kompiled --spec-module REVIEWER-VACUITY 2>&1 | tee reviewer-vacuity.raw.log
proof_status=${PIPESTATUS[0]}
printf '[exit %d]\n' "$proof_status"

printf '\n$ rg -n WarnStuckClaimState reviewer-vacuity.raw.log\n'
rg -n WarnStuckClaimState reviewer-vacuity.raw.log
stuck_status=$?
printf '[exit %d]\n' "$stuck_status"

if [ "$copy_status" -eq 0 ] && [ "$dry_status" -eq 0 ] && [ "$proof_status" -ne 0 ] && [ "$stuck_status" -eq 0 ]; then
  printf 'NON_VACUITY_RESULT=PASS_EXPECTED_UNMET_RESULT_OBLIGATION\n'
  exit 0
fi

printf 'NON_VACUITY_RESULT=FAIL_DIAGNOSTIC_DID_NOT_MATCH\n'
exit 1
