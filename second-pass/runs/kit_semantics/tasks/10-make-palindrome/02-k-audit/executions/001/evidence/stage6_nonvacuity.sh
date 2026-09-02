#!/usr/bin/env bash
set -euo pipefail

work=/tmp/audit-work/candidate-clean
evidence=/audit-output/evidence

echo 'AUDIT COMMAND: bash /audit-output/evidence/stage6_nonvacuity.sh'
cp "$evidence/fresh_nonvacuity.k" "$work/fresh-nonvacuity.k"
sha256sum "$evidence/fresh_nonvacuity.k" "$work/fresh-nonvacuity.k"
cmp "$evidence/fresh_nonvacuity.k" "$work/fresh-nonvacuity.k"

echo 'BUILD COMMAND: kprove fresh-nonvacuity.k --definition verification-audit-kompiled --spec-module FRESH-NONVACUITY --dry-run'
set +e
(
  cd "$work"
  kprove \
    fresh-nonvacuity.k \
    --definition verification-audit-kompiled \
    --spec-module FRESH-NONVACUITY \
    --dry-run
) 2>&1 | tee "$evidence/stage6_nonvacuity_dry_run.log"
status=${PIPESTATUS[0]}
set -e
echo "nonvacuity_build_exit=$status"
test "$status" -eq 0

echo 'PROOF COMMAND: kprove fresh-nonvacuity.k --definition verification-audit-kompiled --spec-module FRESH-NONVACUITY'
set +e
(
  cd "$work"
  kprove \
    fresh-nonvacuity.k \
    --definition verification-audit-kompiled \
    --spec-module FRESH-NONVACUITY
) 2>&1 | tee "$evidence/stage6_nonvacuity_kprove.log"
status=${PIPESTATUS[0]}
set -e
echo "nonvacuity_kprove_exit=$status"
test "$status" -ne 0
grep -q 'WarnStuckClaimState' "$evidence/stage6_nonvacuity_kprove.log"
grep -q 'str ( iCons ( 99 , iCons ( 97 , iCons ( 116 , iCons ( 97 , iCons ( 99' \
  "$evidence/stage6_nonvacuity_kprove.log"
echo 'expected_actual_catac_residual=true'
echo 'STAGE6_NONVACUITY_EXIT=0'
