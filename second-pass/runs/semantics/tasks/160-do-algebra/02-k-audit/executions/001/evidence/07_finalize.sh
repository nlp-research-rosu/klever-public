#!/usr/bin/env bash
set -u

LOG=/audit-output/evidence/07_finalize.log
: > "$LOG"

run() {
  printf 'COMMAND: ' >> "$LOG"
  printf '%q ' "$@" >> "$LOG"
  printf '\n' >> "$LOG"
  "$@" >> "$LOG" 2>&1
  status=$?
  printf 'EXIT: %d\n\n' "$status" >> "$LOG"
  return "$status"
}

run test -s /audit-output/REVIEW.md || exit 1
run test -s /audit-output/evidence/01_integrity.log || exit 1
run test -s /audit-output/evidence/02_differential-results.json || exit 1
run test -s /audit-output/evidence/03_rebuild.log || exit 1
run test -s /audit-output/evidence/03_positive_claims.log || exit 1
run test -s /audit-output/evidence/04_claim_witnesses.json || exit 1
run test -s /audit-output/evidence/04_uncovered_cases.json || exit 1
run test -s /audit-output/evidence/05_rule_inventory.json || exit 1
run test -s /audit-output/evidence/05_rule_assessment.md || exit 1
run test -s /audit-output/evidence/05_used_construct_map.md || exit 1
run test -s /audit-output/evidence/06_vacuity_proof.log || exit 1

run tail -n 2 /audit-output/REVIEW.md || exit 1
final_two=$(tail -n 2 /audit-output/REVIEW.md)
if [ "$final_two" != $'VERDICT: FAIL\nLEGITIMACY: NOT_LEGIT' ]; then
  printf 'FINAL_MARKER_CHECK: FAIL\n' >> "$LOG"
  exit 1
fi
printf 'FINAL_MARKER_CHECK: PASS\n\n' >> "$LOG"

run rg -n '^#Top$' /audit-output/evidence/03_claim_*.log || exit 1
top_count=$(rg -l '^#Top$' /audit-output/evidence/03_claim_*.log | wc -l)
printf 'POSITIVE_CLAIM_LOGS_WITH_TOP: %d\n\n' "$top_count" >> "$LOG"
if [ "$top_count" -ne 10 ]; then
  exit 1
fi

run rg -n 'WarnStuckClaimState|^EXIT: 1$|^HAS_EXACT_TOP: no$' \
  /audit-output/evidence/06_vacuity_proof.log || exit 1
run sha256sum /audit-output/REVIEW.md \
  /audit-output/evidence/01_integrity.log \
  /audit-output/evidence/02_differential-results.json \
  /audit-output/evidence/03_rebuild.log \
  /audit-output/evidence/03_positive_claims.log \
  /audit-output/evidence/04_claim_witnesses.json \
  /audit-output/evidence/04_uncovered_cases.json \
  /audit-output/evidence/05_rule_inventory.json \
  /audit-output/evidence/06_spec-vacuity.k \
  /audit-output/evidence/06_vacuity_proof.log
