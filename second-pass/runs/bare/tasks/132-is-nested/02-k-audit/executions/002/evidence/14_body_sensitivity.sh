#!/usr/bin/env bash
set -uo pipefail

body_output=$(
  kprove pin-check.k \
    --definition body-mutant-verification-kompiled \
    --spec-module PIN-CHECK 2>&1
)
body_status=$?
printf '%s\n' "$body_output"
printf 'mutant_pin_check_inner_exit=%s\n' "$body_status"

if [[ $body_status -eq 0 ]]; then
  printf 'ERROR: body-mutant pin claim unexpectedly closed\n'
  exit 1
fi
if [[ "$body_output" != *"WarnStuckClaimState"* ]]; then
  printf 'ERROR: expected stuck-claim residual was absent\n'
  exit 1
fi
printf 'EXPECTED_BODY_SENSITIVITY_FAILURE_CONFIRMED\n'
