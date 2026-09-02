#!/usr/bin/env bash
set -uo pipefail

REVIEW=/audit-output/REVIEW.md

printf '%s\n' 'COMMAND: test required evidence and completed REVIEW.md structure'
for artifact in \
  "$REVIEW" \
  /audit-output/evidence/01_integrity_check.log \
  /audit-output/evidence/02_fidelity_run.log \
  /audit-output/evidence/03a_concrete_build_run.log \
  /audit-output/evidence/03b_proof_rebuild.log \
  /audit-output/evidence/04_pinning_and_witnesses.log \
  /audit-output/evidence/04b_body_sensitivity_run.log \
  /audit-output/evidence/05_rule_inventory.tsv \
  /audit-output/evidence/05_inventory_checks.log \
  /audit-output/evidence/06_false_mutation_run.log \
  /audit-output/evidence/audit-false-result.k
do
  test -s "$artifact" || exit 1
done

for stage in 1 2 3 4 5 6 7; do
  rg -q "^## ${stage}\\." "$REVIEW" || exit 1
done

rg -q '^#Top$' /audit-output/evidence/03b_proof_rebuild.log || exit 1
rg -q 'STATUS \[positive target claim SPEC.generate-integers\]: 0' \
  /audit-output/evidence/03b_proof_rebuild.log || exit 1
rg -q 'STATUS \[false mutation proof\]: 1 \(expected nonzero\)' \
  /audit-output/evidence/06_false_mutation_run.log || exit 1
rg -q 'WarnStuckClaimState' \
  /audit-output/evidence/06_false_mutation_run.log || exit 1
rg -q '^# TOTAL_ENTRIES 936$' \
  /audit-output/evidence/05_rule_inventory.tsv || exit 1

actual_tail=$(tail -n 2 "$REVIEW")
expected_tail=$'VERDICT: PASS\nLEGITIMACY: LEGIT'
test "$actual_tail" = "$expected_tail" || exit 1
test "$(rg -c '^VERDICT:' "$REVIEW")" = 1 || exit 1
test "$(rg -c '^LEGITIMACY:' "$REVIEW")" = 1 || exit 1

printf '%s\n' \
  'RESULT: all seven sections, decisive evidence, positive #Top, negative stuck mutation, exhaustive inventory, and exact final markers verified'
