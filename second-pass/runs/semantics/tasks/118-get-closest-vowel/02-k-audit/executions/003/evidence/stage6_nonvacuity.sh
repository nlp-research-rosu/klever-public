#!/usr/bin/env bash
set -uo pipefail

cd /tmp/audit-work/reconstruction || exit 90

printf '%s\n' 'MUTATION: concrete satisfying input "bab" postcondition str("a") -> str("")'
printf '%s\n' 'WITNESS: canonical.py("bab") == solution.py("bab") == "a"'

printf '%s\n' 'COMMAND: kprove spec-vacuity.k --definition audit-proof-kompiled --spec-module SPEC-VACUITY --dry-run'
kprove spec-vacuity.k \
  --definition audit-proof-kompiled \
  --spec-module SPEC-VACUITY \
  --dry-run
dry_status=$?
printf 'DRY_RUN_EXIT: %s\n' "$dry_status"

printf '%s\n' 'COMMAND: kprove spec-vacuity.k --definition audit-proof-kompiled --spec-module SPEC-VACUITY'
set +e
kprove spec-vacuity.k \
  --definition audit-proof-kompiled \
  --spec-module SPEC-VACUITY 2>&1 |
  tee /tmp/audit-work/reconstruction/vacuity-proof.raw.log
proof_status=${PIPESTATUS[0]}
set -e
printf 'KPROVE_EXIT: %s\n' "$proof_status"

rg -n \
  -e 'WarnStuckClaimState' \
  -e 'cannot be rewritten further' \
  -e 'str \( iCons \( 97' \
  /tmp/audit-work/reconstruction/vacuity-proof.raw.log
residual_status=$?
printf 'EXPECTED_RESIDUAL_SEARCH_EXIT: %s\n' "$residual_status"

if (( dry_status == 0 && proof_status != 0 && residual_status == 0 )); then
  printf '%s\n' 'NONVACUITY_RESULT: PASS (well-formed false mutation rejected for the expected unmet result)'
  exit 0
fi

printf '%s\n' 'NONVACUITY_RESULT: FAIL'
exit 1
