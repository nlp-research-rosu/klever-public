#!/usr/bin/env bash
set -uo pipefail

printf '%s\n' \
  'SATISFYING_WITNESS: BS = lbr lbr rbr rbr .BString ("[[]]"), functions=.Map, env=.Map, result=noResult'
printf '%s\n' \
  'ORACLES: trusted canonical=True, submitted Python=True, fresh concrete K result=boolVal(true)'
printf '%s\n' \
  'MUTATED_OBLIGATION: result must be boolVal(false)'

mutation_output=$(
  kprove spec-vacuity-fresh.k \
    --definition audit-verification-kompiled \
    --spec-module SPEC-VACUITY-FRESH 2>&1
)
mutation_status=$?
printf '%s\n' "$mutation_output"
printf 'vacuity_inner_kprove_exit=%s\n' "$mutation_status"

if [[ $mutation_status -eq 0 ]]; then
  printf 'ERROR: false postcondition unexpectedly closed\n'
  exit 1
fi
if [[ "$mutation_output" != *"WarnStuckClaimState"* ]]; then
  printf 'ERROR: expected unmet-obligation stuck state was absent\n'
  exit 1
fi
printf 'EXPECTED_FALSE_POSTCONDITION_FAILURE_CONFIRMED\n'
