#!/usr/bin/env bash
set -u

definition=/tmp/audit-work/review-19/candidate/verification-audit-kompiled
spec=/tmp/audit-work/review-19/candidate/spec.k
runner=/audit-output/evidence/run_logged.sh
overall_status=0

for label in \
  number-value-one \
  number-value-two \
  number-value-three \
  number-value-four \
  number-value-five \
  number-value-six \
  number-value-seven \
  number-value-eight \
  number-value-nine \
  sort-numbers-symbolic
do
  "$runner" "/audit-output/evidence/kprove-${label}.log" \
    kprove "$spec" \
    --definition "$definition" \
    --spec-module SORT-NUMBERS-SPEC \
    --claims "SORT-NUMBERS-SPEC.${label}"
  claim_status=$?
  if ((claim_status != 0)); then
    overall_status=$claim_status
  fi
done

exit "$overall_status"
