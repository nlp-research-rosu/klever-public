#!/usr/bin/env bash
set -euo pipefail

review=/audit-output/REVIEW.md

echo '$ tail -n 2 /audit-output/REVIEW.md'
tail -n 2 "$review"

test "$(tail -n 2 "$review" | head -n 1)" = 'VERDICT: PASS'
test "$(tail -n 1 "$review")" = 'LEGITIMACY: LEGIT'
test "$(rg -c '^## [1-7]\.' "$review")" = 7

for status_file in \
  /audit-output/evidence/01_integrity_checks.exit \
  /audit-output/evidence/01_trace_inspection.exit \
  /audit-output/evidence/02_fidelity.exit \
  /audit-output/evidence/03_tool_versions.exit \
  /audit-output/evidence/03_positive_proofs.exit \
  /audit-output/evidence/04_program_pinning.exit \
  /audit-output/evidence/04_ground_substitution.exit \
  /audit-output/evidence/04_body_sensitivity.exit \
  /audit-output/evidence/05_rule_inventory.exit \
  /audit-output/evidence/06_nonvacuity.exit
do
  test "$(tr -d '\n' < "$status_file")" = 0
done

test "$(head -n 1 /audit-output/evidence/03_positive_all.log)" = '#Top'
test "$(head -n 1 /audit-output/evidence/03_positive_prime_loop.log)" = '#Top'
rg -q 'WarnStuckClaimState' /audit-output/evidence/04_body_sensitivity_kprove.log
rg -q '<k>[[:space:]]*$' /audit-output/evidence/04_body_sensitivity_kprove.log
rg -q 'WarnStuckClaimState' /audit-output/evidence/06_false_kprove.log
rg -q 'true ~> \.K' /audit-output/evidence/06_false_kprove.log
cmp -s /candidate/reference-semantics/semantics.k \
  /reference/reference-semantics/semantics.k

echo 'RESULT=PASS'
