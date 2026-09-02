#!/usr/bin/env bash
set -eu

printf '%s\n' '$ final required pair and uniqueness'
tail -n 2 /audit-output/REVIEW.md
test "$(tail -n 2 /audit-output/REVIEW.md)" = \
  $'VERDICT: PASS\nLEGITIMACY: LEGIT'
test "$(rg -c '^VERDICT:' /audit-output/REVIEW.md)" = 1
test "$(rg -c '^LEGITIMACY:' /audit-output/REVIEW.md)" = 1

printf '%s\n' '$ key mechanical outcomes'
rg -n \
  'ordered_identity_bijection": true|manual_inventory_hash_matches": true' \
  /audit-output/evidence/02_inventory.log
rg -n '^#Top$|counterfactual_krun_exit=1' \
  /audit-output/evidence/03_semantic.log
rg -n \
  'returned_preflight_equals_recorded=true|source_obligation_ordered_bijection": true|stage1_pipeline_tree_audit_binding": true|target_statement": null|/candidate ABSENT' \
  /audit-output/evidence/04_preflight.log
rg -n 'WarnStuckClaimState|vacuity_mutation_exit=1' \
  /audit-output/evidence/05_vacuity.log
rg -n '"classification": "DEFINITION"' \
  /audit-output/evidence/06_classification.log

printf '%s\n' '$ final artifact and evidence hashes'
{
  printf '%s\0' /audit-output/REVIEW.md
  find /audit-output/evidence -maxdepth 1 -type f \
    ! -name 08_final_checks.log -print0
} | sort -z | xargs -0 sha256sum
