#!/usr/bin/env bash
set -u

scratch=/tmp/audit-work/135-can-arrange
definition="$scratch/verification-audit-kompiled"
overall=0

echo 'COMMAND: mechanical constructor-token comparison'
python3 /audit-output/evidence/stage4_program_identity.py
status=$?
echo "EXIT [constructor identity]: $status"
if test "$status" -ne 0; then overall=1; fi

echo 'COMMAND: concrete satisfying-witness substitutions'
python3 /audit-output/evidence/stage4_claim_checks.py
status=$?
echo "EXIT [claim witnesses]: $status"
if test "$status" -ne 0; then overall=1; fi

echo 'COMMAND: prove ground substitutions of arrangeSeq'
set +e
kprove /audit-output/evidence/stage4-ground-spec.k \
  --definition "$definition" \
  --spec-module REVIEWER-GROUND-SPEC \
  -I "$scratch" \
  2>&1 | tee /audit-output/evidence/stage4_ground_kprove.log
status=${PIPESTATUS[0]}
set -e
echo "EXIT [ground substitutions]: $status"
if test "$status" -ne 0; then overall=1; fi

echo 'COMMAND: body-sensitivity mutation must be rejected'
set +e
kprove /audit-output/evidence/stage4-body-sensitivity.k \
  --definition "$definition" \
  --spec-module REVIEWER-BODY-SENSITIVITY \
  -I "$scratch" \
  2>&1 | tee /audit-output/evidence/stage4_body_sensitivity.log
status=${PIPESTATUS[0]}
set -e
echo "EXIT [body sensitivity, expected nonzero]: $status"
if test "$status" -eq 0; then
  overall=1
elif ! grep -q 'WarnStuckClaimState' \
  /audit-output/evidence/stage4_body_sensitivity.log
then
  overall=1
fi

exit "$overall"
