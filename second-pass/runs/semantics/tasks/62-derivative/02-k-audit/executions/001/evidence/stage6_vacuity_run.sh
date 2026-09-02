#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/62-derivative
raw=/tmp/audit-work/stage6-kprove.raw
cp --no-dereference \
  /audit-output/evidence/spec-vacuity-audit.k \
  "$scratch/spec-vacuity-audit.k"
cd "$scratch" || exit 70

printf '%s\n' 'SATISFYING_WITNESS: xs=[] in the exact entry-empty initial configuration'
printf '%s\n' 'FALSE_MUTATION: required result changed from [] to [1]'
printf '%s\n' 'KPROVE_COMMAND: timeout 300 kprove spec-vacuity-audit.k --definition verification-kompiled --spec-module SPEC-VACUITY-AUDIT --claims false-empty-result'

timeout 300 kprove spec-vacuity-audit.k \
  --definition verification-kompiled \
  --spec-module SPEC-VACUITY-AUDIT \
  --claims false-empty-result \
  > "$raw" 2>&1
kprove_status=$?

sed -n '1,500p' "$raw"
printf 'KPROVE_EXIT_STATUS: %d\n' "$kprove_status"

if (( kprove_status == 0 )); then
  printf '%s\n' 'MUTATION_ASSESSMENT: INVALID; false mutation unexpectedly closed'
  exit 1
fi
if (( kprove_status == 124 )); then
  printf '%s\n' 'MUTATION_ASSESSMENT: INVALID; timeout is not non-vacuity evidence'
  exit 1
fi
if ! rg -q 'WarnStuckClaimState' "$raw"; then
  printf '%s\n' 'MUTATION_ASSESSMENT: INVALID; expected stuck-claim diagnostic absent'
  exit 1
fi
if ! rg -q 'cannot be rewritten further|implication check' "$raw"; then
  printf '%s\n' 'MUTATION_ASSESSMENT: INVALID; expected unmet-obligation residual absent'
  exit 1
fi

printf '%s\n' 'MUTATION_ASSESSMENT: VALID EXPECTED FAILURE'
exit 0
