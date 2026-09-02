#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/135-can-arrange
overall=0

echo 'COMMAND: exhaustive source-level declaration and rule inventory'
python3 /audit-output/evidence/rule_inventory.py |
  tee /audit-output/evidence/rule_inventory.txt
status=${PIPESTATUS[0]}
echo "EXIT [rule inventory]: $status"
if test "$status" -ne 0; then overall=1; fi

echo 'COMMAND: fixed-semantics observable continuation'
set +e
kprove /audit-output/evidence/stage5-fixed-context.k \
  --definition "$scratch/connection-audit-kompiled" \
  --spec-module REVIEWER-FIXED-CONTEXT \
  -I "$scratch" \
  2>&1 | tee /audit-output/evidence/stage5_fixed_context.log
status=${PIPESTATUS[0]}
set -e
echo "EXIT [fixed context]: $status"
if test "$status" -ne 0; then overall=1; fi

echo 'COMMAND: bridge-enabled observable continuation'
set +e
kprove /audit-output/evidence/stage5-extended-context.k \
  --definition "$scratch/verification-audit-kompiled" \
  --spec-module REVIEWER-EXTENDED-CONTEXT \
  -I "$scratch" \
  2>&1 | tee /audit-output/evidence/stage5_extended_context.log
status=${PIPESTATUS[0]}
set -e
echo "EXIT [extended context]: $status"
if test "$status" -ne 0; then overall=1; fi

echo 'COMMAND: fixed semantics must reject the opposite comparison value'
set +e
kprove /audit-output/evidence/stage5-opposite-comparison.k \
  --definition "$scratch/connection-audit-kompiled" \
  --spec-module REVIEWER-OPPOSITE-COMPARISON \
  -I "$scratch" \
  2>&1 | tee /audit-output/evidence/stage5_opposite_comparison.log
status=${PIPESTATUS[0]}
set -e
echo "EXIT [opposite comparison, expected nonzero]: $status"
if test "$status" -eq 0; then
  overall=1
elif ! grep -q 'WarnStuckClaimState' \
  /audit-output/evidence/stage5_opposite_comparison.log
then
  overall=1
fi

echo 'COMMAND: concrete supplied-model NaN witness'
set +e
krun /audit-output/evidence/reviewer_nan_model.mpy \
  --definition "$scratch/runtime-audit-kompiled" \
  2>&1 | tee /audit-output/evidence/stage5_nan_model.log
status=${PIPESTATUS[0]}
set -e
echo "EXIT [K NaN model witness]: $status"
if test "$status" -ne 0; then overall=1; fi

echo 'COMMAND: concrete CPython NaN witness'
python3 /audit-output/evidence/stage5_nan_python.py |
  tee /audit-output/evidence/stage5_nan_python.log
status=${PIPESTATUS[0]}
echo "EXIT [Python NaN witness]: $status"
if test "$status" -ne 0; then overall=1; fi

exit "$overall"
