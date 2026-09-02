#!/usr/bin/env bash
set +e

WORK=/tmp/audit-work/57-monotonic

run() {
  printf '\n$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return 0
}

run cp /audit-output/evidence/04_fixed_equal_lists_spec.k "$WORK/fixed-equal-lists-spec.k"
run cp /audit-output/evidence/04_extended_equal_lists_spec.k "$WORK/extended-equal-lists-spec.k"

run kprove "$WORK/fixed-equal-lists-spec.k" \
  --definition "$WORK/verification-no-bridge-kompiled" \
  --spec-module FIXED-EQUAL-LISTS-SPEC

run kprove "$WORK/extended-equal-lists-spec.k" \
  --definition "$WORK/verification-kompiled" \
  --spec-module EXTENDED-EQUAL-LISTS-SPEC

run python3 /audit-output/evidence/04_claim_witnesses.py
