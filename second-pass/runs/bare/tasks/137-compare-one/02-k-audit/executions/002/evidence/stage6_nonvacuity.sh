#!/usr/bin/env bash
set -uo pipefail

work=/tmp/audit-work/137-compare-one-audit
spec="$work/spec-vacuity-review.k"
definition="$work/proof-kompiled"
raw_log="$work/nonvacuity.raw.log"

printf '%s\n' 'SATISFYING WITNESS: I=2, J=1; real result pyInt(2), mutated destination pyInt(3)'

printf '%s\n' 'COMMAND: kprove spec-vacuity-review.k --definition proof-kompiled --spec-module SPEC-VACUITY-REVIEW --dry-run'
kprove "$spec" \
  --definition "$definition" \
  --spec-module SPEC-VACUITY-REVIEW \
  --dry-run
dry_status=$?
printf 'MUTATION DRY-RUN EXIT: %s\n' "$dry_status"
(( dry_status == 0 )) || exit "$dry_status"

printf '%s\n' 'COMMAND (expected stuck claim): kprove spec-vacuity-review.k --definition proof-kompiled --spec-module SPEC-VACUITY-REVIEW --output pretty'
kprove "$spec" \
  --definition "$definition" \
  --spec-module SPEC-VACUITY-REVIEW \
  --output pretty \
  2>&1 | tee "$raw_log"
statuses=("${PIPESTATUS[@]}")
proof_status=${statuses[0]}
tee_status=${statuses[1]}
printf 'MUTATION KPROVE EXIT: %s (tee=%s)\n' "$proof_status" "$tee_status"

if (( tee_status != 0 )); then
  printf '%s\n' 'FAIL: reviewer logging failed'
  exit "$tee_status"
fi
if (( proof_status == 0 )); then
  printf '%s\n' 'FAIL: false result mutation unexpectedly closed'
  exit 1
fi
if ! rg -q 'WarnStuckClaimState' "$raw_log"; then
  printf '%s\n' 'FAIL: proof failed without the expected stuck-claim diagnostic'
  exit 1
fi
if ! rg -q 'pyInt \( I \)' "$raw_log"; then
  printf '%s\n' 'FAIL: residual does not show the reached original result'
  exit 1
fi

printf '%s\n' 'STAGE6_NONVACUITY_OK'
