#!/usr/bin/env bash
set -euo pipefail

review=/audit-output/REVIEW.md

echo 'COMMAND: validate exact terminal verdict markers'
tail -n 2 "${review}"
test "$(tail -n 2 "${review}")" = $'VERDICT: FAIL\nLEGITIMACY: NOT_LEGIT'
test "$(rg -c '^VERDICT:' "${review}")" = 1
test "$(rg -c '^LEGITIMACY:' "${review}")" = 1
echo 'VERDICT_MARKERS: PASS'

echo 'COMMAND: validate required evidence artifacts'
for path in \
  evidence/stage1_integrity.log \
  evidence/stage2_fidelity.log \
  evidence/stage3_reconstruct.log \
  evidence/stage3_claims_individual.log \
  evidence/rule_inventory.tsv \
  evidence/stage4_constructor_retry.log \
  evidence/stage4_body_sensitivity.log \
  evidence/stage4_claim_adequacy_retry.log \
  evidence/spec-vacuity.k \
  evidence/stage6_nonvacuity_retry.log
do
  test -s "/audit-output/${path}"
  echo "PRESENT: ${path}"
done
echo 'REQUIRED_EVIDENCE: PASS'

echo 'COMMAND: validate successful corrected proof/non-vacuity signals'
rg -n '#Top|RECORDED_PIPELINE_EXIT_STATUS: 0' \
  /audit-output/evidence/stage3_claims_individual.log
rg -n 'WarnStuckClaimState|false ~> \\.K|EXIT_STATUS \\(false proof, expected nonzero\\): 1' \
  /audit-output/evidence/stage6_nonvacuity_retry.log
echo 'SIGNAL_CHECKS: PASS'
