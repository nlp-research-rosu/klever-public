#!/usr/bin/env bash
set -euo pipefail

python3 /audit-output/evidence/stage1_integrity.py >/tmp/audit-work/final-integrity.out
rg -q '^STAGE1_INTEGRITY=PASS$' /tmp/audit-work/final-integrity.out
rg -q '^cases=163 in_domain_mismatches=0 out_domain_divergences=5$' \
  /audit-output/evidence/differential_test.log
test "$(rg -c '^#Top$' /audit-output/evidence/kprove_positive.log)" -eq 1
rg -q '^EXIT_STATUS=0$' /audit-output/evidence/kprove_positive.log
test "$(rg -c '^#Top$' /audit-output/evidence/kprove_ground_witness.log)" -eq 1
rg -q '^EXIT_STATUS=0$' /audit-output/evidence/kprove_ground_witness.log
rg -q '^PROGRAM_TERM_COMPARE=PASS$' /audit-output/evidence/program_term_compare.log
rg -q '^PRECONDITION_WITNESS=PASS$' /audit-output/evidence/precondition_witness.log
rg -q '^# RULE_INVENTORY=PASS$' /audit-output/evidence/rule_inventory.tsv
rg -q '^# TOTAL_RULE=695$' /audit-output/evidence/rule_inventory.tsv
rg -q '^# ATTRIBUTE_SIMPLIFICATION=0$' /audit-output/evidence/rule_inventory.tsv
rg -q 'WarnStuckClaimState' /audit-output/evidence/kprove_false_result.log
rg -q '^    8 ~> .K$' /audit-output/evidence/kprove_false_result.log
rg -q '^EXIT_STATUS=1$' /audit-output/evidence/kprove_false_result.log
rg -q 'WarnStuckClaimState' /audit-output/evidence/kprove_body_sensitivity.log
rg -q '^    20 ~> .K$' /audit-output/evidence/kprove_body_sensitivity.log
rg -q '^EXIT_STATUS=1$' /audit-output/evidence/kprove_body_sensitivity.log
cmp -s /tmp/audit-work/fruit67/solution.regenerated.mpy /candidate/solution.mpy
review_tail=$(tail -n 2 /audit-output/REVIEW.md)
test "$review_tail" = $'VERDICT: CONCERNS\nLEGITIMACY: LEGIT'
test "$(rg -c '^VERDICT:' /audit-output/REVIEW.md)" -eq 1
test "$(rg -c '^LEGITIMACY:' /audit-output/REVIEW.md)" -eq 1

echo "FINAL_CHECKS=PASS"
