#!/usr/bin/env bash
set -u

work=/tmp/audit-work/87-get-row-review
cd "$work" || exit 1

printf '%s\n' \
  'WITNESS: input lst=[], x=1 satisfies the claim start state; canonical and generated Python both return [].'
printf '%s\n' \
  'MUTATION: require returned [(0,0)] instead of returned [].'

printf '%s\n' \
  'COMMAND: kprove spec-vacuity.k --definition proof-kompiled --spec-module SPEC-VACUITY --dry-run'
kprove spec-vacuity.k \
  --definition proof-kompiled \
  --spec-module SPEC-VACUITY \
  --dry-run
dry_status=$?
printf 'DRY-RUN EXIT: %d\n' "$dry_status"
if [ "$dry_status" -ne 0 ]; then
  printf '%s\n' 'ERROR: mutation did not parse/build successfully'
  exit 1
fi

printf '%s\n' \
  'COMMAND: kprove spec-vacuity.k --definition proof-kompiled --spec-module SPEC-VACUITY'
kprove spec-vacuity.k \
  --definition proof-kompiled \
  --spec-module SPEC-VACUITY \
  > vacuity-proof.raw.log 2>&1
proof_status=$?
sed -n '1,240p' vacuity-proof.raw.log
printf 'PROOF EXIT: %d\n' "$proof_status"
if [ "$proof_status" -eq 0 ]; then
  printf '%s\n' 'ERROR: false mutation unexpectedly proved'
  exit 1
fi
if ! rg -q 'WarnStuckClaimState|cannot be rewritten further|StuckClaim' \
  vacuity-proof.raw.log; then
  printf '%s\n' 'ERROR: expected stuck-claim evidence was absent'
  exit 1
fi
printf '%s\n' 'EXPECTED_NONZERO_WITH_STUCK_OBLIGATION: true'
exit 0
