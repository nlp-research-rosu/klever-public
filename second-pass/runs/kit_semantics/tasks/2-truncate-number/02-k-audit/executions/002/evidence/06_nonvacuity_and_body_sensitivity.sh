#!/usr/bin/env bash
set -u
set -x

cd /tmp/audit-work/fresh || exit 90

kprove audit-spec-vacuity.k \
  --definition audit-verification-kompiled \
  --spec-module AUDIT-SPEC-VACUITY
vacuity_status=$?
printf 'AUDIT_FALSE_POSTCONDITION_EXIT %s\n' "$vacuity_status"

kprove audit-spec-body-mutation.k \
  --definition audit-verification-kompiled \
  --spec-module AUDIT-SPEC-BODY-MUTATION
body_status=$?
printf 'AUDIT_BODY_MUTATION_EXIT %s\n' "$body_status"

if [[ "$vacuity_status" -eq 0 || "$body_status" -eq 0 ]]; then
  printf 'UNEXPECTED_MUTATION_SUCCESS\n'
  exit 1
fi

printf 'EXPECTED_FAILURES_CONFIRMED\n'
exit 0

