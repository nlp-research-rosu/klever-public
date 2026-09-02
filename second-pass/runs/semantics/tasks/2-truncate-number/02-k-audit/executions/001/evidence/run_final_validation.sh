#!/usr/bin/env bash
set -u

run() {
  printf '$'
  printf ' %q' "$@"
  printf '\n'
  "$@"
  status=$?
  printf '[exit %d]\n' "$status"
  return "$status"
}

printf '[seven ordered stage headings]\n'
run rg -n '^## [1-7]\.' /audit-output/REVIEW.md

printf '[exact terminal verdict markers]\n'
run tail -n 2 /audit-output/REVIEW.md
run bash -c "test \"\$(rg -c '^VERDICT: (PASS|CONCERNS|FAIL)$|^LEGITIMACY: (LEGIT|NOT_LEGIT)$' /audit-output/REVIEW.md)\" -eq 2"

printf '[key independent outcomes]\n'
run rg -n 'CANONICAL_GENERATED_MISMATCHES=0|IN_DOMAIN_ORACLE_MISMATCHES=0' \
  /audit-output/evidence/stage2_fidelity.log
run rg -n -e '^#Top' -e '\[exit 0\]' \
  /audit-output/evidence/stage3_reconstruction.log
run rg -n 'WarnStuckClaimState|0\\.0.*#Equals|floatMod' \
  /audit-output/evidence/stages4_6_ground_and_vacuity.log
run rg -n 'AST_MACRO_MATCH=True|WarnStuckClaimState' \
  /audit-output/evidence/stage5_body_sensitivity.log

printf '[artifact sizes and hashes]\n'
run find /audit-output/evidence -maxdepth 1 -type f -printf '%s %f\n'
run sha256sum /audit-output/REVIEW.md \
  /audit-output/evidence/rule_inventory.md \
  /audit-output/evidence/differential_test.py \
  /audit-output/evidence/spec-vacuity.k
