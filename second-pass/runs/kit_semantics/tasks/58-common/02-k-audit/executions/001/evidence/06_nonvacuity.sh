#!/usr/bin/env bash
set -uo pipefail

cd /tmp/audit-work/58-common
cp /audit-output/evidence/spec-audit-vacuity.k spec-audit-vacuity.k

echo 'SATISFYING_INPUT: left=[1], right=[1]; the entry claim has no requires clause.'
echo 'FALSE_OBLIGATION: heap locations 0 and 1 are demanded empty although the real result is [1].'
echo 'COMMAND: kprove spec-audit-vacuity.k --definition verification-audit-kompiled --spec-module SPEC-AUDIT-VACUITY'
kprove spec-audit-vacuity.k \
  --definition verification-audit-kompiled \
  --spec-module SPEC-AUDIT-VACUITY \
  2>&1 | tee vacuity-raw.log
proof_status=${PIPESTATUS[0]}
echo "KPROVE_EXIT: ${proof_status}"

rg -q 'WarnStuckClaimState' vacuity-raw.log
stuck_marker_status=$?
echo "WARN_STUCK_PRESENT: $([[ ${stuck_marker_status} -eq 0 ]] && echo yes || echo no)"

rg -q 'vCons \( 1 , \.ValSeq \)' vacuity-raw.log
actual_one_status=$?
echo "ACTUAL_ONE_RESIDUAL_PRESENT: $([[ ${actual_one_status} -eq 0 ]] && echo yes || echo no)"

if [[ ${proof_status} -eq 0 || ${stuck_marker_status} -ne 0 || ${actual_one_status} -ne 0 ]]; then
  echo 'NONVACUITY_RESULT: invalid'
  exit 1
fi
echo 'NONVACUITY_RESULT: expected unmet result obligation'
