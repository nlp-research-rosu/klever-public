#!/usr/bin/env bash

# Final consistency check for the reviewer-authored report and evidence.
set -euo pipefail

review=/audit-output/REVIEW.md
evidence=/audit-output/evidence

expected_tail=$'VERDICT: FAIL\nLEGITIMACY: NOT_LEGIT'
actual_tail=$(tail -n 2 "$review")
[[ "$actual_tail" == "$expected_tail" ]]

required=(
  "$evidence/stage1-provenance-complete.log"
  "$evidence/stage1-untrusted-generation-summary.log"
  "$evidence/stage2-translation-identity.log"
  "$evidence/stage2-differential.log"
  "$evidence/differential_cases.json"
  "$evidence/stage3-kompile-semantic-llvm.log"
  "$evidence/stage3-concrete-semantics.log"
  "$evidence/stage3-kompile-verification-haskell.log"
  "$evidence/stage3-positive-claims-summary.log"
  "$evidence/stage4-program-pinning.log"
  "$evidence/stage4-claim-witnesses.log"
  "$evidence/stage4-intended-universal-dry-run.log"
  "$evidence/stage4-intended-universal-kprove.log"
  "$evidence/rule-inventory.md"
  "$evidence/stage5-unsound-empty-empty-witness.log"
  "$evidence/spec-vacuity-audit.k"
  "$evidence/stage6-vacuity-dry-run.log"
  "$evidence/stage6-vacuity-kprove.log"
)
for artifact in "${required[@]}"; do
  [[ -f "$artifact" ]]
done

grep -q '^OVERALL_EXIT_STATUS: 0$' \
  "$evidence/stage3-positive-claims-summary.log"
[[ $(grep -c ' exit=0 top_count=1 ' \
  "$evidence/stage3-positive-claims-summary.log") -eq 6 ]]
grep -q '^mismatches=0$' "$evidence/stage2-differential.log"
grep -q '^FALSE_CONCLUSION_WITNESSED: true$' \
  "$evidence/stage5-unsound-empty-empty-witness.log"
grep -q '^EXIT_STATUS: 0$' "$evidence/stage6-vacuity-dry-run.log"
grep -q 'WarnStuckClaimState' "$evidence/stage6-vacuity-kprove.log"
grep -q '^EXIT_STATUS: 1$' "$evidence/stage6-vacuity-kprove.log"

echo "review_tail_ok=true"
echo "required_artifacts_ok=true"
echo "positive_claims_ok=true"
echo "differential_zero_mismatches=true"
echo "unsound_witness_ok=true"
echo "non_vacuity_expected_failure_ok=true"
