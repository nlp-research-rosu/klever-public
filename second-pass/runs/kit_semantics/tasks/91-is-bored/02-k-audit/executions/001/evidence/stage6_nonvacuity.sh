#!/usr/bin/env bash
set -uo pipefail

scratch=/tmp/audit-work/case91
spec=stage6-false-result-spec.k
overall=0

printf 'COMMAND: cp /audit-output/evidence/%s %s/%s\n' "$spec" "$scratch" "$spec"
cp "/audit-output/evidence/$spec" "$scratch/$spec"
copy_ec=$?
printf 'COPY_EXIT=%d\n' "$copy_ec"
if [[ $copy_ec -ne 0 ]]; then overall=1; fi

printf 'SATISFYING_WITNESS: input=\"I work\"; candidate=1; canonical=1; positive ground K claim=1 (#Top)\n'
printf 'MUTATION: same exact entry state and body, postcondition changed from 1 to 2\n'
printf 'COMMAND: cd %s && kprove %s --definition audit-verification-kompiled --spec-module STAGE6-FALSE-RESULT-SPEC\n' \
  "$scratch" "$spec"
(
  cd "$scratch"
  kprove "$spec" \
    --definition audit-verification-kompiled \
    --spec-module STAGE6-FALSE-RESULT-SPEC
)
kprove_ec=$?
printf 'KPROVE_EXIT=%d (expected nonzero)\n' "$kprove_ec"
if [[ $kprove_ec -eq 0 ]]; then
  overall=1
elif ! rg -q 'WarnStuckClaimState' /audit-output/evidence/stage6_nonvacuity.raw.log; then
  printf 'EXPECTED_RESIDUAL_MARKER_MISSING\n'
  overall=1
fi

printf 'FINAL_STATUS=%d\n' "$overall"
exit "$overall"
