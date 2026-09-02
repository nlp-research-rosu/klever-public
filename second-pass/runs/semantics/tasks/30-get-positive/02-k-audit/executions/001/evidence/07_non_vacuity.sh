#!/usr/bin/env bash
set -u

work=/tmp/audit-work/30-get-positive
failed=0

printf '$ kprove %s/spec-vacuity.k --definition %s/verification-kompiled --spec-module SPEC-VACUITY --dry-run > %s/spec-vacuity.kore\n' \
  "$work" "$work" "$work"
kprove "$work/spec-vacuity.k" \
  --definition "$work/verification-kompiled" \
  --spec-module SPEC-VACUITY \
  --dry-run \
  > "$work/spec-vacuity.kore"
dry_status=$?
printf '[exit %d]\n' "$dry_status"
if test "$dry_status" -ne 0; then
  failed=1
fi

printf '\n$ wc -c %s/spec-vacuity.kore\n' "$work"
wc -c "$work/spec-vacuity.kore"
wc_status=$?
printf '[exit %d]\n' "$wc_status"
if test "$wc_status" -ne 0; then
  failed=1
fi

printf '\n$ kprove %s/spec-vacuity.k --definition %s/verification-kompiled --spec-module SPEC-VACUITY --claims SPEC-VACUITY.filter-loop,SPEC-VACUITY.get-positive-wrong --trusted SPEC-VACUITY.filter-loop --smt-timeout 10000\n' \
  "$work" "$work"
kprove "$work/spec-vacuity.k" \
  --definition "$work/verification-kompiled" \
  --spec-module SPEC-VACUITY \
  --claims SPEC-VACUITY.filter-loop,SPEC-VACUITY.get-positive-wrong \
  --trusted SPEC-VACUITY.filter-loop \
  --smt-timeout 10000 \
  > /audit-output/evidence/07_non_vacuity.raw.log 2>&1
proof_status=$?
sed -n '1,260p' /audit-output/evidence/07_non_vacuity.raw.log
printf '[exit %d]\n' "$proof_status"

if test "$proof_status" -eq 0; then
  printf 'ERROR: false result mutation unexpectedly proved\n'
  failed=1
fi
if ! rg -q 'WarnStuckClaimState' /audit-output/evidence/07_non_vacuity.raw.log; then
  printf 'ERROR: expected stuck-claim diagnostic was absent\n'
  failed=1
fi
if ! rg -q '0 \|-> list \( \.ValSeq \)' /audit-output/evidence/07_non_vacuity.raw.log; then
  printf 'ERROR: expected concrete empty-result residual was absent\n'
  failed=1
fi
if ! rg -q 'INPUT|\.IntSeq' /audit-output/evidence/07_non_vacuity.raw.log; then
  printf 'ERROR: expected satisfying empty-input path condition was absent\n'
  failed=1
fi

exit "$failed"
