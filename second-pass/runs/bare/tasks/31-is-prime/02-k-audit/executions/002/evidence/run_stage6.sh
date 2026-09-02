#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/review-31
candidate="$scratch/candidate"
definition="$scratch/verification-proof-kompiled"
overall=0

cd "$candidate" || exit 2

printf 'WITNESS: N=2 satisfies the entry source; trusted canonical is_prime(2)=True.\n'
printf 'MUTATION: replace required final Bool(prime(2))=Bool(true) with Bool(false).\n'

printf 'COMMAND: kprove spec-audit-vacuity.k --definition %q --spec-module SPEC-AUDIT-VACUITY --dry-run\n' \
  "$definition"
kprove spec-audit-vacuity.k \
  --definition "$definition" \
  --spec-module SPEC-AUDIT-VACUITY \
  --dry-run
build_rc=$?
printf 'EXIT: %d\n' "$build_rc"
if [[ "$build_rc" -ne 0 ]]; then
  overall=1
fi

printf 'COMMAND (expected proof failure): kprove spec-audit-vacuity.k --definition %q --spec-module SPEC-AUDIT-VACUITY\n' \
  "$definition"
kprove spec-audit-vacuity.k \
  --definition "$definition" \
  --spec-module SPEC-AUDIT-VACUITY
proof_rc=$?
printf 'EXIT: %d\n' "$proof_rc"
if [[ "$proof_rc" -eq 0 ]]; then
  overall=1
fi

printf 'BUILD_EXIT=%d EXPECTED_PROOF_FAILURE_EXIT=%d STAGE6_OVERALL=%d\n' \
  "$build_rc" "$proof_rc" "$overall"
exit "$overall"
