#!/usr/bin/env bash
set -euo pipefail

scratch=/tmp/audit-work/candidate
definition=/tmp/audit-work/fresh-build/verification-kompiled
raw=/tmp/audit-work/nonvacuity.raw.log

cp /audit-output/evidence/spec-vacuity-review.k "$scratch/spec-vacuity-review.k"

printf 'WITNESS: VS = vCons(1, vCons(2, .ValSeq)); nondecreasing(VS) = true; Python result = true; mutated result = false\n'
printf 'COMMAND: kprove %s --definition %s --spec-module MONOTONIC-SPEC-VACUITY-REVIEW --dry-run\n' \
  "$scratch/spec-vacuity-review.k" "$definition"
kprove "$scratch/spec-vacuity-review.k" \
  --definition "$definition" \
  --spec-module MONOTONIC-SPEC-VACUITY-REVIEW \
  --dry-run >/tmp/audit-work/nonvacuity-dry-run.kore
printf 'EXIT_STATUS=0\n'

printf 'COMMAND: kprove %s --definition %s --spec-module MONOTONIC-SPEC-VACUITY-REVIEW\n' \
  "$scratch/spec-vacuity-review.k" "$definition"
set +e
kprove "$scratch/spec-vacuity-review.k" \
  --definition "$definition" \
  --spec-module MONOTONIC-SPEC-VACUITY-REVIEW \
  >"$raw" 2>&1
status=$?
set -e
sed -n '1,110p' "$raw"
rg -n -m 80 'WarnStuckClaimState|true|false|implication check|\\[Error\\]' "$raw" || true
tail -25 "$raw"
printf 'EXIT_STATUS=%s\n' "$status"
if [ "$status" -eq 0 ]; then
  printf 'FALSE_MUTATION_UNEXPECTEDLY_CLOSED\n'
  exit 1
fi
if ! rg -q 'WarnStuckClaimState' "$raw"; then
  printf 'EXPECTED_STUCK_CLAIM_NOT_FOUND\n'
  exit 1
fi
if ! rg -q 'true' "$raw" || ! rg -q 'false' "$raw"; then
  printf 'EXPECTED_TRUE_FALSE_RESIDUAL_NOT_FOUND\n'
  exit 1
fi
printf 'NONVACUITY_TEST=PASS\n'
